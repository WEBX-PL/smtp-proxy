import asyncio
import logging
import os

from modules.http_server import start_http_server
from modules.smtp_server import start_smtp_server
from dotenv import load_dotenv


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await asyncio.gather(
        start_http_server(os.getenv('HTTP_HOST', '0.0.0.0'), os.getenv('HTTP_PORT', 80)),
        start_smtp_server(os.getenv('SMTP_HOST', '0.0.0.0'), os.getenv('SMTP_PORT', 9999)),
        return_exceptions=True
    )

    try:
        while True:
            await asyncio.sleep(3600)  # Wait for an hour before checking again
    except KeyboardInterrupt:
        print("Shutting down servers...")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
