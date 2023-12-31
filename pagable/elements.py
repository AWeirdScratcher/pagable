from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Self

BlankDict = {}

class Element:
    """Represents an HTML element.

    Args:
        tag (str): The initial HTML tag.
    """
    __slots__ = (
        'tag',
        'attrs',
        'children',
        'attrs',
        '_children'
    )

    def __init__(
        self, 
        tag: str
    ) -> None:
        self.tag = tag

    def __call__(
        self,
        children: Union[Element, str, List[Element]] = "",
        attrs: Dict[str, str] = BlankDict,
        **attrs_kwargs
    ) -> Self:
        """Appends attributes and children to this element.

        Args:
            children (Element | str | List[Element]): The children.
            attrs (Dict[str, str]): Attributes, if any.
            **attrs_kwargs: Attrs kwargs for Pythonic references.
        """
        self.children = children
        self.attrs = {
            str(k): str(v) for k, v in attrs.items()
        }
        self.attrs |= {
            k.replace('_', '-'): str(v)
            for k, v in attrs_kwargs.items()
        }
        self._init_children()

        return self

    def _init_children(self):
        if isinstance(self.children, List):
            self._children = [
                item.mapping if isinstance(item, Element) else str(item)
                for item in self.children
            ]

        elif isinstance(self.children, Element):
            self._children = [self.children.mapping]

        else:
            self._children = str(self.children)

    @property
    def mapping(self) -> dict:
        """Returns a mapping for the JS client to understand."""
        return {
            'tag': self.tag,
            'attrs': self.attrs,
            'children': self._children
        }

class _HTML:
    """HTML class for reference.

    Example:
        .. code-block :: python

            html = _HTML()
            html.a("Hello, World!", href="https://google.com")
    """
    def __getattribute__(self, __name: str) -> Element:
        """Gets an element.

        Example:
            .. code-block :: python

                html = _HTML()
                html.a("Hello, World!", href="https://google.com")
                # <a href="https://google.com">Hello, World!</a>
        """
        return Element(__name)

    def __getitem__(self, __name: str) -> Element:
        """Gets an element with slices. Used for custom elements.

        .. warning ::

            It's not recommended to use this method, as it's difficult to read.
            Use the ``__call__`` method instead.

        Args:
            .. code-block :: python

                html = _HTML()
                html['custom-element'](
                    "Hello, World!",
                    data_link="https://google.com"
                )
                # <custom-element data-link="https://google.com">
                #   Hello, World!
                # </custom-element>
        """
        return Element(__name)

    def __call__(
        self,
        tag: str,
        children: Union[Element, str, List[Element]] = "",
        attrs: Dict[str, str] = BlankDict,
        **attrs_kwargs
    ) -> Element:
        """Gets an element with call. Usually used for custom elements.

        Initializes the element as well.

        Args:
            .. code-block :: python

                html = _HTML()
                html(
                    "custom-element",
                    "Hello, World!", 
                    data_link="https://google.com"
                )
                # <custom-element data-link="https://google.com">
                #   Hello, World!
                # </custom-element>
        """
        ele = Element(tag)

        return ele(children, attrs, **attrs_kwargs)


html = _HTML()
