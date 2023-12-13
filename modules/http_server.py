import json

from aiohttp import web

from config import HOSTNAME
from modules.db import get_emails, get_email


async def start_http_server(host, port):
    app = web.Application()

    async def emails_list(request):
        emails = await get_emails()
        return web.Response(text=json.dumps({"emails": emails}))

    async def send_email_item(request):
        id = request.match_info.get('id', None)
        if id:
            email = await get_email(id)
            if email:
                print('sending...', email)
                return web.Response(text="OK")

        return web.Response(text="NOT")

    app.router.add_get('/', emails_list)
    app.router.add_get('/send/{id}', send_email_item)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    print("WEB server started:", site._host, site._port)
