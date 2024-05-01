import logging
import asyncio
import subprocess

from scr.client import client
from scr.sender import process_chats


def main():
    subprocess.run(['alembic', 'upgrade', 'head'])
    logging.basicConfig(level='INFO')
    # while True:
    #     time.sleep(5)
    loop = asyncio.get_event_loop()
    client.start()
    loop.run_until_complete(process_chats())
    client.stop()

if __name__ == '__main__':
    main()
