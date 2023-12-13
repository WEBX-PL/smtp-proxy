from smtplib import SMTP as Client


def main():
    client = Client("164.90.161.12", 9999)
    r = client.sendmail('a@example.com', ['b@example.com'], """\
    From: Anne Person <anne@example.com>
    To: Bart Person <bart@example.com>
    Subject: A test
    Message-ID: <ant>

    Hi Bart, this is Anne.
    """)

def test2():
    import smtplib
    import random
    import string

    def generate_random_string(length=10):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def send_email(server_ip, server_port, sender_email, receiver_email, subject, body, username, password):
        message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP_SSL(server_ip, server_port) as server:
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, message)

    if __name__ == "__main__":
        smtp_server_ip = "164.90.161.12"
        smtp_server_port = 9999

        sender_email = generate_random_string() + "@example.com"
        receiver_email = generate_random_string() + "@example.com"
        subject = generate_random_string()
        content = generate_random_string(50)

        username = "your_username"  # Replace with your SMTP server username
        password = "your_password"  # Replace with your SMTP server password

        send_email(smtp_server_ip, smtp_server_port, sender_email, receiver_email, subject, content, username, password)

if __name__ == "__main__":
    main()
    test2()

