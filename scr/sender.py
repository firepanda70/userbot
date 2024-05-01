import asyncio
import logging
from datetime import datetime

from scr.core.db import AsyncSessionMaker
from scr.repo import ChatDataRepo
from scr.models import Status, State
from scr.const import DURATION_BY_STATE, MESSAGE_BY_STATE
from scr.client import client


async def process_chats():
    while True:
        async with AsyncSessionMaker() as session:
            repo = ChatDataRepo(session)
            chats = await repo.get_many(status=Status.ALIVE)
            now = datetime.now()
            for chat in chats:
                try:
                    state = State(chat.state)
                    duration = DURATION_BY_STATE.get(state, None)
                    if not duration:
                        logging.error(f'Duration for state `{state}` not set')
                        continue
                    if (now - chat.state_updated_at) >= duration:
                        message = MESSAGE_BY_STATE.get(state, None)
                        if not message:
                            logging.error(f'Message for state `{state}` not set')
                            continue
                        await client.send_message(chat.id, message)
                        logging.info(f'Message for chat `{chat.id}` with state `{state}` was send')
                        updated = await repo.set_next_state(chat)
                        logging.info(f'State for chat `{chat.id}` was updated to `{State(updated.state)}`')
                except Exception as e:
                    logging.exception(f'Exeption during chat `{chat.id}` processing occured')
                    await repo.kill(chat, str(e))
                    logging.warning(f'Chat `{chat.id}` killed')
        await asyncio.sleep(5)
