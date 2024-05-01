import re
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from scr.core.db import AsyncSessionMaker
from scr.core.settings import get_config
from scr.repo import ChatDataRepo
from scr.const import MAIN_TRIGGER, TRIGGER_BY_STATE
from scr.models import Status, State

config = get_config()
client = Client('client', api_id=config.api_id, api_hash=config.api_hash)


@client.on_message(filters.private & filters.text)
async def process_message(client: Client, message: Message):
    async with AsyncSessionMaker() as session:
        repo = ChatDataRepo(session)
        db_chat = await repo.get(message.from_user.id)
        if not db_chat:
            await repo.create(message.from_user.id)
            logging.info(f'New chat created, user `{message.from_user.id}`')
        elif db_chat.status == Status.ALIVE:
            if re.match(MAIN_TRIGGER, message.text):
                await repo.kill(db_chat, 'Main trigger match found')
                logging.info(f'Chat killed by main trigger, user `{message.from_user.id}`')
            else:
                state = State(db_chat.state)
                trigger = TRIGGER_BY_STATE.get(state, None)
                if trigger and re.match(trigger, message.text):
                    updated = await repo.set_next_state(db_chat)
                    logging.info(f'Skipped state `{state}` by state trigger, user `{message.from_user.id}`')
                    logging.info(f'State for chat `{updated.id}` was updated to `{State(updated.state)}`')
        else:
            logging.info(f'Got `{Status(db_chat.status)}` status chat, user `{message.from_user.id}`, kill reason `{db_chat.kill_reason}`')
