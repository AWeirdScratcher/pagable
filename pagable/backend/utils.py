from typing import Tuple

from ._const import EXTENSION_EMOJIS


def get_extension(filename: str) -> Tuple[str, str]:
    """Gets file extension and its corresponding emoji (if registered).

    Returns a blank string if no extension is found.

    Args:
        filename (str): The filename.

    Returns:
        Tuple[str, str]: First element is the extension, the second one is the emoji.
    """
    if "." not in filename:
        return ("", "")

    ext = filename.split(".")[-1]

    return (ext, EXTENSION_EMOJIS.get(ext, ""))
