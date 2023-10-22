import { v4 as uuid4 } from 'https://jspm.dev/uuid'

var allRequirementsId = [];

function addRequirement(requirement) {
    let head = document.querySelector('head');
    if (requirement.endsWith('.css')) {
        let sheet = document.createElement("link")

        sheet.rel = "stylesheet"
        sheet.href = requirement
        sheet.type = "text/css"
        sheet.id = uuid4()

        head.appendChild(sheet);
        allRequirementsId.push(sheet.id);
    } else {
        let scr = document.createElement('script')

        scr.type = "module"
        scr.src = requirement
        scr.id = uuid4()

        head.appendChild(scr);
        allRequirementsId.push(scr.id);
    }
}

function parseMapping(mapping) {
    if (typeof mapping == 'string') {
        let paragraph = document.createElement("p");
        paragraph.textContent = mapping;
        return paragraph;

    } else if (Array.isArray(mapping)) {
        let fragment = new DocumentFragment();

        mapping.forEach((item) => {
            fragment.appendChild(
                parseMapping(item)
            )
        })

        return fragment

    } else if (typeof mapping == 'object') {
        let element = document.createElement(mapping.tag);
        element.appendChild(
            parseMapping(mapping.children)
        )
        for (const attr in mapping.attrs) {
            element[attr] = mapping.attrs[attr]
        }

        return element
    }
}

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
            if (!data.initial)
                return window.location.reload();

            // first call
            console.log("[pagable] call")
            console.table(data)

            if (data.ctyp == "md") {
                root.innerHTML = data.ctnt;

                if (
                    data.meta.theme && 
                    data.meta.theme.toLowerCase() !== "none"
                ) {
                    let sheet = document.createElement("link");
                    let themes = {
                        auto: "https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css",
                        light: "https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css",
                        dark: "https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css"
                    };
                    sheet.rel = "stylesheet";
                    sheet.href = themes[data.meta.theme.toLowerCase()];
                    sheet.type = "text/css"
                    document.head.appendChild(sheet);
                }

                if (data.meta.title) {
                    document.title = data.meta.title;
                }
            } else if (data.ctyp == "py") {
                data.requires.forEach((requirement) => {
                    addRequirement(requirement)
                })

                root.appendChild(
                    parseMapping(data.ctnt)
                );
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
        setTimeout(() => {
            connect();
        }, 1000)
    }
}
connect();
