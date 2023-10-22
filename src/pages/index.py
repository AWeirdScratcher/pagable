from pagable import alert, html


async def handle():
    return [
        html.div(
            "hi"
        ),
        html.h1(
            "i love chocolate!"
        )
    ]
