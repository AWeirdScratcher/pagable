import os
import pickle
import uuid
from importlib.machinery import SourceFileLoader
from inspect import iscoroutinefunction as iscoro
from types import ModuleType
from typing import Any, Dict, Tuple, Union

import markdown2
from rich.console import Optional

from ._const import console, instance_id

Mapping = Dict[str, Dict[str, str]]
ModuleMapping = Dict[str, ModuleType]


def load(path: str) -> ModuleType:
    """(Re)loads a (file) module from a file path.

    Usually used for ``src/<file>``.

    Args:
        path (str): The file path.
    """
    return SourceFileLoader(str(uuid.uuid4()), path).load_module()


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def map_source(
    source: str = "./src/",
    *,
    only: Optional[str] = None,
    save: bool = True,
) -> Tuple[Mapping, ModuleMapping]:
    """Maps source files for later use.

    Args:
        source (str): The source path. Usually ``./src/``.
        only (str): Only for a specific file (e.g., ``src/pages/index.py``)
        save (bool, optional): Whether to save to cache.

    Returns:
        Tuple[Mapping, ModuleMapping]: Returns a mapping dictionary and a module 
            mapping. It's generated when loading python files.
    """
    mapped: Mapping = get_mapped() if only else {
        "$instance": {
            "id": instance_id
        }
    }
    module_mapping: ModuleMapping = {}
    absp = os.path.abspath(source)
    abspl = len(absp)  # abs path length

    for base, _, filenames in os.walk(absp):
        if base.endswith('__pycache__'):
            continue

        for filename in filenames:
            if "." not in filename:
                continue

            fp: str = normalize(os.path.join(base, filename))

            if only and not os.path.samefile(fp, only):
                continue

            ext: str = fp.split(".")[-1]

            if ext in ("md", "py"):
                route: str = fp[abspl:][len("/pages"):][:-3]
                route = route[:-5] if route.endswith("/index") else (route +
                                                                     "/")

                if not only and route in mapped:
                    console.print(f"[red b]duplicate route {route}[/]")
                    raise FileExistsError

                if only:
                    mapped["$new"] = {
                        "route": route
                    }

                if ext == "md":
                    with open(fp, "r", encoding="utf-8") as f:
                        mapped[route] = {
                            "type": "md",
                            "file": fp,
                            "ctnt": markdown2.markdown(
                                f.read(),
                                extras=["metadata", "spoiler"]
                            )
                        }

                else:
                    mod = load(fp)
                    route = getattr(mod, "__route__", route)
                    cnt = getattr(mod, "handle", None)

                    if not cnt:
                        console.print(
                            f"[red b]Cannot find coro handle() for {route}[/] "
                            f"[white d u]{fp}[/]"
                        )
                        raise AttributeError

                    elif not iscoro(cnt):
                        console.print(
                            "[red b]export handle() is not coroutine[/]"
                        )
                        raise TypeError

                    module_mapping[route] = mod

                    mapped[route] = {
                        "type": "py",
                        "file": fp,
                        "ctnt": "<load>"
                    }

    if save:
        with open("_pagable.cache", "wb") as f:
            pickle.dump(mapped, f)

    return mapped, module_mapping


def get_mapped(*, expired_then_generate: bool = True) -> Mapping:
    """Gets previously generated mapping.

    .. warning ::

        You cannot retrieve (loaded) modules with this method.

    Args:
        expired_then_generate (bool): Generate one if expired? Default true.

    Returns:
        Mapping: The mapping.
    """
    if not os.path.exists("_pagable.cache"):
        raise FileNotFoundError("Cannot find most recent cache")

    with open("_pagable.cache", "rb") as f:
        mapping: Mapping = pickle.load(f)

        if mapping['$instance']['id'] != instance_id:
            if expired_then_generate:
                return map_source()[0]

            else:
                raise TimeoutError("instance expired for this cache")

        else:
            return mapping
