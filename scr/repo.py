from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scr.models import ChatData, Status, State


class ChatDataRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> ChatData | None:
        expr = select(ChatData).where(ChatData.id == id)
        return (await self.session.execute(expr)).scalar_one_or_none()

    async def get_many(self, status: Status | None = None) -> Sequence[ChatData]:
        expr = select(ChatData)
        if status:
            expr = expr.where(ChatData.status == status.value)
        return (await self.session.execute(expr)).scalars().all()

    async def create(self, id: int) -> ChatData:
        now = datetime.now()
        obj = ChatData(
            id=id, status=Status.ALIVE.value, state=State.INITIAL.value,
            created_at=now, status_updated_at=now, state_updated_at=now
        )
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def kill(self, obj: ChatData, kill_reason: str):
        obj.status = Status.DEAD.value
        obj.kill_reason = kill_reason
        obj.status_updated_at = datetime.now()
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def set_next_state(self, obj: ChatData):
        next_state = State.get_next(obj.state)
        now = datetime.now()
        obj.state = next_state.value
        obj.state_updated_at = now
        if next_state is State.FINAL:
            obj.status = Status.FINISHED.value
            obj.status_updated_at = now
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
