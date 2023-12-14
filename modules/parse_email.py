import email
from email.header import decode_header


def parse_email(raw_email):
    # Decode bytes to string
    email_str = raw_email.decode('unicode_escape')

    # Parse the email content
    message = email.message_from_string(email_str)

    # Decode and get the subject
    subject = decode_header(message['Subject'])[0]
    if isinstance(subject[0], bytes):
        subject = subject[0].decode(subject[1] or 'utf-8')
    else:
        subject = subject[0]

    # Get the message body
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # Skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = message.get_payload(decode=True)

    return subject, body.decode('utf-8')
