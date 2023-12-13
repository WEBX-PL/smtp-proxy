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


if __name__ == "__main__":
    main()
