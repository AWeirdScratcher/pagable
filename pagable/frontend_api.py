import json
from typing import Any, Dict, Optional, Union

from .api import Component, get_component


class FrontendAPI:
    """The base frontend API.
    
    Attributes:
        component (:obj:`Component`): The component.
    """
    __slots__ = (
        "component",
    )
    component: Component

    def __init__(self):
        self.component = get_component()

    async def _inject(self, script: str) -> Any:
        return await self.component.add_scripting(script)


class LocalStorage(FrontendAPI):
    """Represents the local storage."""

    async def clear(self) -> None:
        """Clears the local storage."""
        await self._inject("return window.localStorage.clear()")

    async def set_item(
        self, 
        key: str, 
        value: Union[str, Dict[Any, Any]]
    ) -> None:
        """Sets a local storage item.
        
        Args:
            key (str): The key.
            value (str | dict): The value. Accepts dict.
        """
        data: str = value if isinstance(value, str) else json.dumps(value)
        await self._inject(
            f"return window.localStorage.setItem({key!r}, {data!r})"
        )

    async def get_item(
        self,
        key: str
    ) -> Union[str, Dict[Any, Any]]:
        """Gets an item from local storage.

        Args:
            key (str): The key.

        Returns:
            str | Dict[Any, Any]: Returns dict if JSON detected.
                String otherwise.
        """
        d: str = await self._inject(
            f"return window.localStorage.getItem({key!r})"
        )
        
        try:
            return json.loads(d)

        except json.JSONDecodeError:
            return d

class Script(FrontendAPI):
    """Represents a Javascript evaluator."""

    async def run(self, script: str) -> Optional[str]:
        """Runs a script.

        Args:
            script (str): The script.

        .. note ::

            To return a value, use ``return`` in JS.

        Example:
            .. code-block :: python

                async def handle():
                    script = Script()
                    title = await script.run("return document.title")
                    return "Title is {title!r}"

        Returns:
            Optional[str]: Evaluated data.
        """
        return await self._inject(script)

async def throw(t: str):
    """Throws an exception on the frontend.

    Args:
        t (str): The text.
    """
    s =  Script()
    await s.run(f"throw new Error({t!r})")

class Navigator:
    """Represents the window navigator."""

async def alert(*data: Any) -> None:
    script = Script()
    await script.run(
        "window.alert(" + ", ".join((
            f"{str(item)!r}" for item in data
        )) + ")"
    )

async def Window(): # noqa
    """Fetches the window object.

    This function is a coroutine.
    """
    script = Script()
    window = await script.run("return window")
