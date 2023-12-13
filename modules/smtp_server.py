from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult

from modules.db import create_email
from modules.slack import send_notification


class SMTPHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        email = await create_email(envelope.mail_from, envelope.rcpt_tos, str(envelope.content))
        await send_notification(email)
        return '250 Message accepted for delivery'


class Authenticator:
    def __call__(self, server, session, envelope, mechanism, auth_data):
        return AuthResult(success=True)


async def start_smtp_server(host, port):
    controller = Controller(SMTPHandler(), hostname=host, port=port, authenticator=Authenticator(),
                            auth_require_tls=False)
    controller.start()

    print("SMTP server started:", controller.hostname, controller.port)
