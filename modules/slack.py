async def send_notification(email):
    print("send notification", email.id, email.mail_from, email.rcpt_tos, email.content)
