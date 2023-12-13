import json

from aiohttp import web

from config import HOSTNAME
from modules.db import get_emails


async def start_http_server():
    app = web.Application()

    async def emails_list(request):
        emails = await get_emails()
        return web.Response(text=json.dumps({"emails": emails}))

    app.router.add_get('/', emails_list)
    app.router.add_get('/send/{id}', emails_list)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOSTNAME, 80)
    await site.start()

    print("WEB server started:", site._host, site._port)
