from datetime import timedelta

from scr.models import State


MESSAGE_BY_STATE: dict[State, str] = {
    State.INITIAL: 'Текст1',
    State.FIRST: 'Текст2',
    State.SECOND: 'Текст3',
}

MAIN_TRIGGER = r'(прекрасно)|(ожидать)'
TRIGGER_BY_STATE: dict[State, None | str] = {
    State.INITIAL: None,
    State.FIRST: r'Триггер1',
    State.SECOND: None,
}

DURATION_BY_STATE: dict[State, timedelta] = {
    # State.INITIAL: timedelta(minutes=1),
    # State.FIRST: timedelta(minutes=1),
    # State.SECOND: timedelta(minutes=1),
    State.INITIAL: timedelta(minutes=6),
    State.FIRST: timedelta(minutes=39),
    State.SECOND: timedelta(days=1, hours=2),
}
