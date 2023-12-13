import json
import uuid

import aiosqlite

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
            content TEXT
        );
        """
    )

    return db


async def create_email(mail_from, rcpt_tos, content):
    db = await connect()
    email = ("email_" + str(uuid.uuid4()), mail_from, json.dumps(rcpt_tos), content)

    await db.execute('INSERT INTO email (id, mail_from, rcpt_tos, content) VALUES (?, ?, ?, ?)', email)
    await db.commit()
    await db.close()


async def get_emails():
    db = await connect()
    cursor = await db.execute('SELECT * FROM email ORDER BY created_at DESC LIMIT 50')
    rows = await cursor.fetchall()
    data = []
    for id, created_at, updated_at, mail_from, rcpt_tos, content in rows:
        data.append(dict(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            mail_from=mail_from,
            rcpt_tos=json.loads(rcpt_tos),
            content=content,
        ))
    await cursor.close()
    await db.close()

    return data
