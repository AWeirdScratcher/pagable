from typing import Dict, Iterable

class Head:
    """Represents the HTML ``<head>``.

    It has the first priority to be rendered in page, which it will be added to the 
    html directly instead of WebSocket completions.
    """
    def __init__(self, contents: Iterable[str]):
        pass

BlankDict = {}

class Meta:
    """Represents a ``<meta>`` tag.

    Args:
        kwargs_dict (optional): Kwargs from dict.
        **kwargs: Keys and values.
    """
    def __init__(
        self,
        kwargs_dict: Dict[str, str] = BlankDict,
        **kwargs: str
    ):
        pass
