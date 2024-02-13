import mysql.connector
from mysql.connector import Error

from modules.db import mark_as_sent

TOKEN = "7e8e8c79-8f88-4ac3-a65d-36437330a4a8"

def check_email_exists(email):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            user="kettlo",
            password="KL+78ef56lm",
            host="app.kettlo.com",
            port="3306",
            database="kettlo"
        )

        cursor = connection.cursor()

        # Execute a SELECT query to check if the email exists in the users table
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))

        # Fetch the result
        count = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return True if the email exists, False otherwise
        return count > 0

    except Error as error:
        print("Error while connecting to MySQL", error)
        return False


from postmark import PMMail


def send_email(from_email, to_email, subject, body):
    message = PMMail(api_key=TOKEN,
                     subject=subject,
                     sender=from_email,
                     to=to_email,
                     text_body=body)

    try:
        message.send()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)


async def s_email(email):
    if check_email_exists(email['rcpt_tos'][0]):
        send_email(
            from_email=email['mail_from'],
            to_email=email['rcpt_tos'],
            subject=email['subject'],
            body=email['body']
        )
        await mark_as_sent(email['id'])
        return True
    return False

