import asyncio
from pathlib import Path

from pyrogram import Client

from scr.core.settings import get_config


env_file = Path('./infra/.env')
config = get_config(env_file)
client = Client('client', api_id=config.api_id, api_hash=config.api_hash)

async def main():
    async with client:
        print(client.me)


if __name__ == '__main__':
    client.run(main())
