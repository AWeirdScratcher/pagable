import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload

from .elements import Element
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
        self.process_args()

    def process_args(self):
        params = inspect.signature(self.render).parameters

        for param in params:
            name = str(param)
            if params[name].kind not in (
                inspect.Parameter.POSITIONAL_ONLY, 
                inspect.Parameter.POSITIONAL_OR_KEYWORD
            ):
                continue

            if name.startswith("use_") and name.endswith("_state"):
                self.states[name] = params[name].default

    def _get_content(self, data):
        if isinstance(data, Element):
            return data.mapping

        elif isinstance(data, List):
            return [self._get_content(item) for item in data]

        else:
            return str(data)

    async def __call__(self):
        """Calls the rendering function."""
        self.forward_state_updates()
        data = await self.render()
        return self._get_content(data)

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
