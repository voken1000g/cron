import os
import json
from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid, PeerIdInvalid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

TG_API_ID = os.environ['TG_API_ID']
TG_API_HASH = os.environ['TG_API_HASH']

PYRO_GET_CHAT_MEMBERS_LIMIT = 200
PYRO_MONITOR_CHAI_IDS = os.environ['PYRO_MONITOR_CHAT_IDS']

app = Client(session_name='monitor',
             workdir=DATA_DIR,
             api_id=TG_API_ID,
             api_hash=TG_API_HASH)


async def main():
    deleted = []
    chats = []

    # verify `PYRO_MONITOR_CHAI_IDS`
    monitor_chat_ids = list()
    for monitor_chat_id in PYRO_MONITOR_CHAI_IDS.split(','):
        monitor_chat_id = monitor_chat_id.strip()
        if monitor_chat_id:
            monitor_chat_ids.append(monitor_chat_id)
    if monitor_chat_ids:
        # launch Telegram client
        async with app:
            # verify chat type
            for monitor_chat_id in monitor_chat_ids:
                try:
                    chat = await app.get_chat(monitor_chat_id)
                    if chat.type in ['supergroup', 'group']:
                        chats.append(chat)
                except PeerIdInvalid:
                    continue
                except UsernameInvalid:
                    continue
                except ValueError:
                    continue

            # chats
            if chats:
                for chat in chats:
                    try:
                        count = await app.get_chat_members_count(chat.id)
                    except PeerIdInvalid:
                        continue
                    except UsernameInvalid:
                        continue
                    except ValueError:
                        continue

                    # count > 0
                    if count:
                        user_ids = []
                        offset = 0
                        while offset < count:
                            members = await app.get_chat_members(chat_id=chat.id,
                                                                 offset=offset,
                                                                 limit=PYRO_GET_CHAT_MEMBERS_LIMIT)
                            if members:
                                for member in members:
                                    if member.user.is_deleted:
                                        user_ids.append(member.user.id)
                            offset += PYRO_GET_CHAT_MEMBERS_LIMIT

                        if user_ids:
                            print('{} `Deleted Account` founded in Chat({})'.format(len(user_ids), chat.id))
                            deleted.append(dict(
                                id=chat.id,
                                username=chat.username,
                                user_ids=user_ids
                            ))

    with open(os.path.join(DATA_DIR, 'deleted.json'), 'w') as f:
        json.dump(deleted, f)


if __name__ == "__main__":
    app.run(main())
