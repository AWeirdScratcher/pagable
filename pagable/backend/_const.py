import os
import uuid

from rich.console import Console

instance_id = str(uuid.uuid4())

console = Console()

EXTENSION_EMOJIS = {
    "py": "🐍",
    "md": "🔥"
}

here = os.path.abspath(os.path.dirname(__file__))
