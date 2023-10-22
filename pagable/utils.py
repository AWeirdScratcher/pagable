import os
import traceback
from typing import Any, Callable, Dict, List

requirements: List[str] = []

def clear_requirements():
    """(interal) clear all requirements."""
    requirements.clear()

def require(file: str):
    """Requires a JS or CSS file from the ``src/scripts`` or ``src/styles`` folder.
    
    Args:
        file (str): The file.
    """
    if not file.endswith('js') and not file.endswith('css'):
        raise NotImplementedError(
            f"{file.split('.')[-1]!r} is not yet implemented."
        )

    dest = os.path.join(
        os.getcwd(), 
        "scripts" if file.endswith('js') else "css", 
        file
    )

    requirements.append(dest)
