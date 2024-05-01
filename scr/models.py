from datetime import datetime
from enum import Enum

from sqlalchemy.orm import mapped_column, Mapped
from scr.core.db import BaseDBModel


class Status(str, Enum):
    ALIVE = 'alive'
    DEAD = 'dead'
    FINISHED = 'finished'


class State(int, Enum):
    INITIAL = 0
    FIRST = 1
    SECOND = 2
    FINAL = -1

    @classmethod
    def get_next(cls, state: int) -> 'State':
        cls(state)
        if state == -1:
            raise ValueError('It is final state')
        try:
            return cls(state + 1)
        except ValueError:
            return cls(-1)


class ChatData(BaseDBModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    status_updated_at: Mapped[datetime]
    status: Mapped[str]
    state: Mapped[int]
    state_updated_at: Mapped[datetime]
    kill_reason: Mapped[str | None]
