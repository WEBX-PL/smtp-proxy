import mysql.connector
from mysql.connector import Error
from postmarker.core import PostmarkClient

from modules.db import mark_as_sent

TOKEN = "029ca801-e6d8-45ba-a1f1-948cf3cf1809"


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


def send_email(to_email, subject, body):
    postmark = PostmarkClient(server_token=TOKEN)
    from_email = "application@kettlo.com"

    try:
        print(postmark.emails.send(
            Subject=subject,
            From=from_email,
            To=to_email,
            HtmlBody=body
        ))
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)


async def s_email(email):
    if check_email_exists(email['rcpt_tos'][0]):
        send_email(
            to_email=email['rcpt_tos'],
            subject=email['subject'],
            body=email['body']
        )
        await mark_as_sent(email['id'])
        return True
    return False
