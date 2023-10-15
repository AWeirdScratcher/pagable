(() => {
    function connect() {
        console.log("[pagable] connecting");

        const _url = `wss://${window.location.hostname}${WS_URL}`
        const ws = new WebSocket(_url);
        const root = document.getElementById("root");
    
        ws.onopen = () => {
            console.log("[pagable] connected")
            let path = window.location.pathname;
            ws.send(
                JSON.stringify({
                    path: path.endsWith('/') ? path : (path + "/")
                })
            )
        }
    
        ws.onmessage = ({ data: plainData }) => {
            const data = JSON.parse(plainData);

            if (data.type == 1) {
                // hmr update
                console.log("[pagable] hmr update")
                root.innerHTML = data.ctnt;

                if (data.meta.theme) {
                    let themes = {
                        auto: "https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css",
                        light: "https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css",
                        dark: "https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css"
                    };

                    document.getElementById("water-stylesheet").href = themes[data.meta.theme];
                }

                if (data.meta.title) {
                    document.title = data.meta.title;
                }
            } else if (data.type == 2) {
                // script interaction
                try {
                    let res = Function(
                        data.ctnt
                    )()
                    ws.send(
                        JSON.stringify({
                          type: 2,
                          ctnt: res || null // prevent undefined
                      })
                    )

                } catch (e) {
                    //throw e
                    ws.send(
                        JSON.stringify({
                          type: 2.1, // error
                          mesg: e.message,
                          name: e.name || null,
                          caus: e.cause || null
                        })
                    )
                }
                
            }
            
        }
        ws.onclose = () => {
            connect();
        }
    }
    connect();
})()