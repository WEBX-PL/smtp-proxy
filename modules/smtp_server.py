from aiosmtpd.controller import Controller

from config import HOSTNAME


class SMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        return '250 Message accepted for delivery'


async def start_smtp_server():
    controller = Controller(SMTPHandler(), hostname=HOSTNAME, port=9999)
    controller.start()

    print("SMTP server started:", controller.hostname, controller.port)
