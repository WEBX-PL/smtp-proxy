import os


from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from modules.db import mark_as_sent


async def send_notification(email):
    print("send notification", email['id'], email['mail_from'], email['rcpt_tos'], email['content'])

    slack_token = os.environ["SLACK_BOT_TOKEN"]
    client = WebClient(token=slack_token)

    try:
        client.chat_postMessage(
            channel=os.environ["SLACK_CHANNEL_ID"],
            text="You have a new email to verify",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "You have a new email to verify"
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
                        "text": email['message']
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
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Send it!",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "url": "http://164.90.161.12:8080/send/" + str(email['id']) + "?pass=" + os.getenv(
                                'PASSWORD'),
                            "action_id": "button-action"
                        }
                    ]
                }
            ]
        )
        await mark_as_sent(email['id'])
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
