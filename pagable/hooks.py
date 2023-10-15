from inspect import isfunction
from typing import Any, Callable, Tuple, Union

from .api import Component, get_component

StateUpdateField = Union[Any, Callable[[Any], Any]]

def _state_updater(
    comp: Component, 
    key: str
) -> Callable[[StateUpdateField], None]:
    def updater(
        value_or_callback: StateUpdateField
    ) -> None:
        """Represents an updater."""
        if isfunction(value_or_callback):
            val = value_or_callback(comp.states[key])
        else:
            val = value_or_callback

        comp.update_state(key, val)

    return updater

def use_state(
    name: str,
    default_value: Any
) -> Tuple[Any, Callable[[StateUpdateField], None]]:
    """State management."""
    component = get_component()

    if name not in component.states:
        component.states[name] = default_value
    
    return (
        component.states[name],
        _state_updater(component, name)
    )
