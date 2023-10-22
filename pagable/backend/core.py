import asyncio
import os
import uuid
from contextlib import asynccontextmanager
from typing import List, Union

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.routing import APIRoute, Optional
from fastapi.staticfiles import StaticFiles
from watchfiles import Change, awatch

from ..api import Component
from ._const import here
from ._logger import logger
from .load import Mapping, ModuleMapping, map_source
from .utils import get_extension


class App:
    """Represents a Pagable application."""

    __slots__ = (
        "app",
        "mapping",
        "module_mapping",
        "ws_route",
        "ws_handlers"
    )
    app: FastAPI
    mapping: Mapping
    module_mapping: ModuleMapping
    ws_route: str
    ws_handlers: dict

    def __init__(self):
        self.app = FastAPI(
            docs_url=None, 
            redoc_url=None,
            lifespan=self._lifespan
        )
        self.app.mount(
            "/scripts", 
            StaticFiles(directory="src/scripts"), 
            name="scripts"
        )
        self.app.mount(
            "/styles", 
            StaticFiles(directory="src/styles"), 
            name="styles"
        )
        self.app.mount(
            "/",
            StaticFiles(directory="public"),
            name="public"
        )
        self.ws_route = "/__WS__"
        self.app.router.add_api_websocket_route(
            self.ws_route,
            self._ws_handler
        )
        self.ws_handlers = {}
        
        self.app.router.add_api_route(
            "/app.js",
            self._js_delivery,
        )
        self.app.router.add_api_route(
            "/{full_path:path}",
            self._app_handler
        )
        self.load_files()

    async def _app_handler(self, _: Optional[str] = None):
        with open(
            "index.html", 
            "r", 
            encoding="utf-8"
        ) as f:
            return HTMLResponse(f.read())

    async def _js_delivery(self):
        with open(
            os.path.join(here, "script.js"),
            "r", 
            encoding="utf-8"
        ) as f:
            return Response(
                f.read().replace("${WS_URL}", self.ws_route),
                headers={
                    "Content-Type": "application/javascript"
                }
            )

    async def _ws_handler(self, ws: WebSocket):
        await ws.accept()
        c = await ws.receive_json()
        route = c['path']
        state: List[Union[str, Component]] = []

        def set_ctnt(val):
            state.clear()
            state.append(val)

        async def update(route: str, *, initial: bool = False):
            #logger.log("[blue]UPDATE[/]")
            typ = self.mapping[route]['type']
            data = {
                "type": 1,
                "meta": {},
                "initial": initial
            }

            if typ == "md":
                contents = self.mapping[route]['ctnt']
                set_ctnt(contents)

                await ws.send_json(
                    data | {
                        "ctyp": "md",
                        "ctnt": contents,
                        "meta": contents.metadata # type: ignore
                    }
                )

            elif typ == "py":
                mod = self.module_mapping[route]
                comp = Component(mod.handle)
                comp.__ws__ = ws
                set_ctnt(comp)

                await ws.send_json(
                    data | {
                        "ctyp": "py",
                        "ctnt": await comp(),
                        "requires": getattr(mod, "requires", [])
                    }
                )

        try:
            await update(route, initial=True)
        except Exception as err:
            logger.log(
                f"[red]ERROR[/] {err}"
            )
            raise err
            return
        
        if isinstance(state[0], Component):
            state[0].first_rendered = True

        @self.ws_handle()
        async def handler(next_route: str):
            if next_route == route:
                await update(route)

        try:
            while True:
                data = await ws.receive_json()
                if data['type'] == 2 and isinstance(state[0], Component):
                    print("type 2")
                    print(data)
                    state[0].pending_data = data

                elif data['type'] == 2.1 and isinstance(state[0], Component):
                    raise BaseException

        except WebSocketDisconnect:
            handler.remove()

    async def emit(self, route: str):
        for handler in self.ws_handlers.values():
            await handler(route)

    def ws_handle(self):
        def wrapper(func):
            _id = str(uuid.uuid4())
            self.ws_handlers[_id] = func
    
            class Handler:
                @staticmethod
                def remove():
                    del self.ws_handlers[_id]
    
            return Handler

        return wrapper

    async def _background_runner(self):
        async for changes in awatch(
            "./src/pages", 
            #"index.html",
            poll_delay_ms=500
        ):
            for change in changes:
                if change == Change.deleted:
                    continue

                diff, filename = change
                try:
                    mapped, modules = map_source(only=filename)
                except Exception as err:
                    logger.log(
                        "[red]ERROR (reload failed)[/] " + 
                        str(err)
                    )
                    continue

                route = mapped['$new']['route']

                if filename.endswith(".py"):
                    self.module_mapping[route] = modules[route]

                self.mapping.update(mapped)

                await self.emit(route)
                
                _, emoji = get_extension(filename)
                logger.log(
                    f"{emoji + (' ' if emoji else '')}"
                    f"[blue]update[/] {os.path.relpath(filename)}"
                )

    @asynccontextmanager
    async def _lifespan(self, _: FastAPI):
        asyncio.create_task(self._background_runner())
        logger.log("running app")
        yield

    def load_files(self):
        """Loads files."""
        mapping, modules = map_source()
        self.mapping = mapping
        self.module_mapping = modules

    def run(self):
        uvicorn.run(
            self.app,
            host="0.0.0.0", 
            port=8080,
            #log_level=50 # fatal
        )
