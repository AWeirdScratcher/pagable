from pagable import alert, html


async def handle():
    return html.div([
        html.h1("hi"),
        html.div([
            html.h1('inside!')
        ], style="color: red")
    ], style="background: green")
