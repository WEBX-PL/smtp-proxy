import os


from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from modules.db import mark_as_sent
from modules.send_email import s_email


async def send_notification(email):
    print("send notification", email)

    slack_token = os.environ["SLACK_BOT_TOKEN"]
    client = WebClient(token=slack_token)
    sent = False
    try:
        sent = await s_email(email)
    except Exception as e:
        pass

    client.chat_postMessage(
        channel=os.environ["SLACK_CHANNEL_ID"],
        text="Mail sent!" if sent else "You have a new email to verify",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Mail sent!" if sent else "You have a new email to verify"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*ID:*\n" + str(email['id'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*From:*\n" + str(email['mail_from'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Recipients:*\n" + '; '.join(email['rcpt_tos'])
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Subject:*\n" + str(email['subject'])
                    },
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": email['body']
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "See full message",
                            "emoji": True
                        },
                        "value": "click_me_123",
                        "url": "http://164.90.161.12:8080/email/" + str(email['id']) + "?pass=" + os.getenv(
                            'PASSWORD'),
                        "action_id": "button-action"
                    },
                ]
            }
        ]
    )
