from pagable import alert, html, LocalStorage

requires = [
    "styles/index.css"
]

async def handle():
    storage = LocalStorage()
    await storage.clear()
    return [
        html.div(
            "hi"
        ),
        html.h1(
            "i love chocolate!"
        )
    ]
