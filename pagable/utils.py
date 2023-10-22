import os
import traceback
from typing import Any, Callable, Dict, List

requirements: List[str] = []

def clear_requirements(fn: str):
    requirements.clear()

def require(file: str):
    dest = os.path.join(os.getcwd(), "scripts", file)

    requirements.append(dest)
