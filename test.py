import logging
from smtplib import SMTP as Client

host = "127.0.0.1"
# host = "164.90.161.12"
def main():
    client = Client(host, 9999)
    client.login("asdad", "bbbb")
    r = client.sendmail('a@example.com', ['b@example.com'], "b'Content-Type: text/plain; charset=\"utf-8\"\\r\\nMIME-Version: 1.0\\r\\nContent-Transfer-Encoding: 8bit\\r\\nSubject: \\r\\n =?utf-8?b?W2V4YW1wbGUuY29tXSBFLW1haWwgeiDFgsSFY3plbSBkbyB6bWlhbnkgaGFzxYJh?=\\r\\nFrom: FixmeApp <None>\\r\\nTo: patient00@fixme.pl\\r\\nDate: Thu, 14 Dec 2023 09:12:46 -0000\\r\\nMessage-ID: <170254516641.7048.11635991546422814767@DESKTOP-T1OMHNC.lan>\\r\\n\\r\\nWitamy z example.com!\\r\\n\\r\\nOtrzymujesz t\\xc4\\x99 wiadomo\\xc5\\x9b\\xc4\\x87, poniewa\\xc5\\xbc Ty lub kto\\xc5\\x9b inny poprosi\\xc5\\x82 o zresetowanie has\\xc5\\x82a do Twojego konta.\\r\\nNiniejsz\\xc4\\x85 wiadomo\\xc5\\x9b\\xc4\\x87 mo\\xc5\\xbcesz spokojnie zignorowa\\xc4\\x87, je\\xc5\\xbceli pro\\xc5\\x9bba nie pochodzi\\xc5\\x82a od Ciebie. Kliknij w link poni\\xc5\\xbcej, aby zresetowa\\xc4\\x87 has\\xc5\\x82o.\\r\\n\\r\\nhttp://127.0.0.1:8000/accounts/password/reset/key/2-bz70da-6d44f74d60e466964e62da934a314013/\\r\\n\\r\\nDzi\\xc4\\x99kujemy za korzystanie z example.com!\\r\\nexample.com\\r\\n'")

# def test2():
#     import smtplib
#     import random
#     import string
#
#     def generate_random_string(length=10):
#         return ''.join(random.choice(string.ascii_letters) for _ in range(length))
#
#     def send_email(server_ip, server_port, sender_email, receiver_email, subject, body, username, password):
#         message = f"Subject: {subject}\n\n{body}"
#         with smtplib.SMTP_SSL(server_ip, server_port) as server:
#             server.login(username, password)
#             server.sendmail(sender_email, receiver_email, message)
#     smtp_server_ip = host
#     smtp_server_port = 9999
#
#     sender_email = generate_random_string() + "@example.com"
#     receiver_email = generate_random_string() + "@example.com"
#     subject = generate_random_string()
#     content = generate_random_string(50)
#
#     username = "your_username"  # Replace with your SMTP server username
#     password = "your_password"  # Replace with your SMTP server password
#
#     send_email(smtp_server_ip, smtp_server_port, sender_email, receiver_email, subject, content, username, password)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # test2()
    main()

