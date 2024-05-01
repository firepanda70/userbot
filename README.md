# userbot

## Description
Simple userbot with timed messages for registered users.

## Requirements
 - Docker
 - Python 3.12
 - Poetry 1.7.2

## Installation
1. Clone repository.
```
git clone https://github.com/firepanda70/userbot
```
2. Create and fill ```.env``` file in ```infra``` dir.
```
API_ID=0000000
API_HASH=api_hash_string
DB_URL=docker:docker@pg
COMPOSE_PROJECT_NAME=userbot
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
POSTGRES_DB=docker
```
3. Install venv and run setup actions for project from root project dir
```
poetry install
poetry run python setup.py
```
4. In dialog enter telegram phone number and recieved confirmation code
```
-- // --
Enter phone number or bot token: +12345678901        # Enter phone
Is "+12345678901" correct? (y/N): y                  # Confirm phone
The confirmation code has been sent via Telegram app
Enter confirmation code: 12345                       # Enter confirmation code
{
    "_": "User",  # Logined user data info
    ...
}
```
5. Build docker contaiers
```
cd infra
docker compose up -d --build
```
6. Enjoy!

## Usage
1. App processes text messages from private chats
2. New users register on first recieved message
3. User chat can be in the following states:
  - ```INITIAL``` - starting state. Duration - 6 minutes. Ends with message with text ```Текст1```.
  - ```FIRST``` - state following ```INITIAL```. Duration - 39 minutes. Can be skipped by message with text ```Триггер1```. Ends with message with text ```Текст2```. 
  - ```SECOND``` - state following ```FIRST```. Duration - 1 day 2 hours. Ends with message with text ```Текст3```.
  - ```FINAL``` - state following ```SECOND```. Final state.
4. Also user chat can be in 3 statuses:
  - ```alive``` - default status. Means chat is being processed
  - ```dead``` - this means that either sending the message failed or app recieved trigger to kill chat. Triggers described in 5-th item
  - ```finished``` - this means that chat finished successfully.
5. Chat can be killed by message with text that contains ```прекрасно``` OR ```ожидать``` words. Only for chats with ```alive``` status and ```INITIAL```, ```FIRST``` or ```SECOND``` state.

## Technologies
- Python 3.12
- Poetry
- Pydantic
- asyncio
- Pyrogram
- SQLAlchemy
- alembic
- Docker
- Postgres
