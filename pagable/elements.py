from __future__ import annotations

from typing import Dict, Iterable, Self, Union

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
        'attrs'
    )

    def __init__(
        self, 
        tag: str
    ) -> None:
        self.tag = tag

    def __call__(
        self,
        children: Union[Element, str, Iterable[Element]] = "",
        attrs: Dict[str, str] = BlankDict,
        **attrs_kwargs
    ) -> Self:
        """Appends attributes and children to this element.

        Args:
            children (Element | str | Iterable[Element]): The children.
            attrs (Dict[str, str]): Attributes, if any.
            **attrs_kwargs: Attrs kwargs for Pythonic references.
        """
        self.children = children
        self.attrs = attrs
        self.attrs |= {
            k.replace('_', '-'): v
            for k, v in attrs_kwargs.items()
        }

        return self
    

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
        children: Union[Element, str, Iterable[Element]] = "",
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
