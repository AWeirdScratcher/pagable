import os
import sys

APP_PY = b"""from pagable import alert


async def handle():
    await alert("Welcome to pagable!")
    return "Welcome!"
"""

APP_MD = b"""---
theme: auto
title: My Markdown Page
---

# My Markdown Page

Do you think Markdown is cool? I think it is!

Here's a button:

<button onclick="alert('Hi, Mom!')">Click me!</button>

Some details:

<details>
    <summary>Click to reveal</summary>
    <p>Hi, Mom!</p>
</details>
"""

APP_MAIN = b"""from pagable.backend.core import App

app = App()

app.run()
"""

def main():
    args = sys.argv[1:]
    
    if not args or args[0] != 'create' or len(args) > 2:
        print("Usage: pagable create [dir]")
        exit(0)

    base = "".join(args[1:]) or os.path.join(os.getcwd(), "my-app")
    registers = (
        "src/api/",
        "src/pages/",
        "src/scripts/",
        "src/api/",
        "src/styles/",
    )

    for entry in registers:
        create(base, entry)

    write(base, "src/pages/index.py", APP_PY)
    write(base, "src/pages/markdown.md", APP_MD)
    write(base, "main.py", APP_MAIN)

    print(f"created app ({base!r})")

def write(base, path: str, content: bytes):
    with open(
        os.path.join(base, path),
        "wb"
    ) as f:
        f.write(content)

def create(base: str, path: str):
    os.makedirs(os.path.join(base, path), exist_ok=True)
