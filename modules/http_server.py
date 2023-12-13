from aiohttp import web

from config import HOSTNAME


async def start_http_server():
    app = web.Application()

    async def hello(request):
        return web.Response(text="Hello, world")

    # Add routes
    app.router.add_get('/', hello)

    # Start the web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOSTNAME, 8888)
    await site.start()

    print("WEB server started:", site._host, site._port)
