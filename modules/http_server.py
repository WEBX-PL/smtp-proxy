import json
import os

from aiohttp import web

from modules.db import get_emails, get_email, clear_db
from modules.send_email import s_email


def check_password(request):
    user_password = str(request.rel_url.query['pass'])
    password = str(os.getenv('PASSWORD'))

    if not password or not user_password or user_password != password:
        raise ValueError("Invalid password")


async def start_http_server(host, port):
    app = web.Application()

    async def emails_list(request):
        try:
            check_password(request)
        except Exception as e:
            return web.Response(text=str(e))

        emails = await get_emails()
        return web.Response(text=json.dumps({"emails": emails}))

    async def send_email_item(request):
        try:
            check_password(request)
        except Exception as e:
            return web.Response(text=str(e))

        id = request.match_info.get('id', None)
        if id:
            email = await get_email(id)
            if email:
                print('sending...', email)
                if await s_email(email):
                    return web.Response(text="MAIL: " + email['subject'] + " SENT TO: " + ', '.join(email['rcpt_tos']))
                else:
                    return web.Response(text="MAIL NOT FOUND IN DATABASE OF USERS!")

        return web.Response(text="NOT")

    async def clear(request):
        try:
            check_password(request)
        except Exception as e:
            return web.Response(text=str(e))

        await clear_db()
        return web.Response(text="OK")

    async def email_details(request):
        try:
            check_password(request)
        except Exception as e:
            return web.Response(text=str(e))

        id = request.match_info.get('id', None)
        if id:
            email = await get_email(id)
            if email:
                return web.Response(text=json.dumps(dict(
                    id=email['id'],
                    sent=email['sent'],
                    created_at=email['created_at'],
                    updated_at=email['updated_at'],
                    mail_from=email['mail_from'],
                    rcpt_tos=email['rcpt_tos'],
                    subject=email['subject'],
                    body=email['body'],
                )))

        return web.Response(text="NOT")

    app.router.add_get('/', emails_list)
    app.router.add_get('/clear', clear)
    app.router.add_get('/send/{id}', send_email_item)
    app.router.add_get('/email/{id}', email_details)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    print("WEB server started:", site._host, site._port)
