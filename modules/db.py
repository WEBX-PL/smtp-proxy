import json
import uuid

import aiosqlite

from modules.parse_email import parse_email


async def connect():
    db = await aiosqlite.connect(database="db.sqlite")

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS email (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mail_from TEXT,
            rcpt_tos TEXT, -- SQLite does not support array types, so you might need to serialize this field
            content TEXT,
            sent BOOLEAN DEFAULT FALSE
        );
        """
    )

    return db


async def clear_db():
    db = await connect()
    await db.execute("DROP TABLE IF EXISTS email;")
    await db.close()


async def create_email(mail_from, rcpt_tos, content):
    db = await connect()
    email = ("email_" + str(uuid.uuid4()), mail_from, json.dumps(rcpt_tos), content)

    await db.execute('INSERT INTO email (id, mail_from, rcpt_tos, content) VALUES (?, ?, ?, ?)', email)
    await db.commit()
    await db.close()

    id, mail_from, rcpt_tos, content = ("email_" + str(uuid.uuid4()), mail_from, json.dumps(rcpt_tos), content)

    return dict(
        id=id,
        mail_from=mail_from,
        rcpt_tos=json.loads(rcpt_tos),
        content=content,
    )


async def get_emails():
    db = await connect()
    cursor = await db.execute('SELECT * FROM email ORDER BY created_at DESC LIMIT 50')
    rows = await cursor.fetchall()
    data = []
    for id, created_at, updated_at, mail_from, rcpt_tos, content, sent in rows:
        subject, body = parse_email(content)
        data.append(dict(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            mail_from=mail_from,
            rcpt_tos=json.loads(rcpt_tos),
            subject=subject,
            body=body,
            sent=sent
        ))
    await cursor.close()
    await db.close()

    return data


async def get_email(id):
    db = await connect()
    cursor = await db.execute('SELECT * FROM email WHERE id = ?', (id,))
    row = await cursor.fetchone()

    await cursor.close()
    await db.close()

    if not row:
        return None

    id, created_at, updated_at, mail_from, rcpt_tos, content, sent = row
    subject, body = parse_email(content)

    return dict(
        id=id,
        created_at=created_at,
        updated_at=updated_at,
        mail_from=mail_from,
        rcpt_tos=json.loads(rcpt_tos),
        content=content,
        subject=subject,
        body=body,
        sent=sent
    )


async def mark_as_sent(id):
    db = await connect()
    await db.execute('UPDATE email SET sent = true, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    await db.close()
