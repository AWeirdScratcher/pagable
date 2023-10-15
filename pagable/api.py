import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional

from .exceptions import PageError

FunctionComponent = Callable[..., Any]

class Component(object):
    """Represents a component."""
    __slots__ = (
        "render",
        "states",
        "_next_states",
        "__ws__",
        "first_rendered",
        "pending_data"
    )
    render: FunctionComponent
    states: Dict[str, Any]
    _next_states: Dict[str, Any]
    __ws__: Any
    first_rendered: bool
    pending_data: Optional[dict]
    
    def __init__(self, func):
        self.first_rendered = False
        self.render = func
        self.states = self._next_states = {}

    async def __call__(self):
        """Calls the rendering function."""
        self.forward_state_updates()
        return await self.render()

    def update_state(self, key: str, value: Any):
        """Updates a state for next the next render.

        .. warning ::

            This does not really affect the value from ``use_state``. 
            Instead, it's stored into the ``_next_states`` attribute.

        Args:
            key (str): The (state) key.
            value (Any): Any value.
        """
        self._next_states.update({ key: value })

    def forward_state_updates(self):
        """Forwards previously cached state updates."""
        self.states.update(self._next_states)

    async def add_scripting(self, script: str) -> Any:
        """Adds a scripting. (coroutine)"""
        await self.__ws__.send_json({
            "type": 2,
            "ctnt": script
        })
        if not self.first_rendered:
            data = None

            while not data:
                d = await self.__ws__.receive_json()
            
                if d['type'] == 2:
                    data = d
                elif d['type'] == 2.1:
                    raise PageError(d)

            return data['ctnt']

        else:
            self.pending_data = None
            while not self.pending_data:
                await asyncio.sleep(0.01)

            return self.pending_data['ctnt']


def get_component() -> Component:
    """Gets the (nearest) function component.

    Raises:
        TypeError: This wasn't called from a component (origin).
    """
    for stack in inspect.stack()[1:]:
        _locals = stack[0].f_locals
        if 'self' in _locals and isinstance(_locals['self'], Component):
            return _locals['self']

    raise TypeError(
        "`get_component()` wasn't made from a component."
    )
