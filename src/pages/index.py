from pagable import html


async def handle():
    return [
        html.h1("Welcome!"),
        html.p([,
            html.a("Click me!", href="https://google.com")
        ]),
    ]