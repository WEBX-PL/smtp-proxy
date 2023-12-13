from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult

from config import HOSTNAME
from modules.db import create_email


class SMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        await create_email(envelope.mail_from, envelope.rcpt_tos, str(envelope.content))
        return '250 Message accepted for delivery'

class Authenticator:
    def __call__(self, server, session, envelope, mechanism, auth_data):
        return AuthResult(success=True)

async def start_smtp_server():
    controller = Controller(SMTPHandler(), hostname=HOSTNAME, port=9999, authenticator=Authenticator())
    try:
        controller.start()
        print("SMTP server started:", controller.hostname, controller.port)
    finally:
        controller.stop()


