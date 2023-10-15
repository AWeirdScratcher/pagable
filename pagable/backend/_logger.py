from datetime import datetime
from typing import Literal

from ._const import console


class _Time:
    def __format__(
        self, 
        __type: Literal['colored', 'plain']
    ) -> str:
        return (
            "{s}{now:%b %d / %H:%M:%S}{e}"
        ).format(
            now=datetime.now(),
            s={"colored": "[d white]", "plain": ""}[__type],
            e={"colored": "[/]", "plain": ""}[__type]
        )

now = _Time()

class logger:
    @staticmethod
    def log(*data):
        console.print(f"{now:colored}", *data)
