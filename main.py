import asyncio

from modules.http_server import start_http_server
from modules.smtp_server import start_smtp_server


async def main():
    await asyncio.gather(
        start_http_server(),
        start_smtp_server(),
        return_exceptions=True
    )

    try:
        while True:
            await asyncio.sleep(3600)  # Wait for an hour before checking again
    except KeyboardInterrupt:
        print("Shutting down servers...")


if __name__ == "__main__":
    asyncio.run(main())
