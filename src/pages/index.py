from pagable import alert, html, Requires

requires: Requires = [
    "styles/index.css",
    "scripts/index.js"
]

async def handle():
    return [
        html.div(
            "hi"
        ),
        html.h1(
            "i love chocolate!"
        )
    ]
