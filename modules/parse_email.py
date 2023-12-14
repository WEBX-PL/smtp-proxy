import email
from email.header import decode_header


def parse_email(raw_email):
    # Decode bytes to string
    email_str = eval(raw_email).decode('unicode_escape')

    # Parse the email content
    message = email.message_from_string(email_str)

    # Decode the subject
    subject_header = decode_header(message['Subject'])
    subject = ''
    for part, encoding in subject_header:
        if isinstance(part, bytes):
            subject += part.decode(encoding or 'utf-8')
        else:
            subject += part

    # Get the message body
    if message.is_multipart():
        body = ''
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
    else:
        body = message.get_payload(decode=True).decode(message.get_content_charset() or 'utf-8')

    return subject.strip(), body.strip()
