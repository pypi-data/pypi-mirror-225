from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import yaml
import asyncio

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

async def get_entity(client, source):
    credential['id_map'] = credential.get('id_map', {})
    if source not in credential['id_map']:
        entity = await client.get_entity(source)
        credential['id_map'][source] = entity.id
        with open('credential', 'w') as f:
            f.write(yaml.dump(credential, sort_keys=True, indent=2, allow_unicode=True))
    return await client.get_entity(credential['id_map'][source])

async def findLinksAsync(source):
    client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
    await client.start(password=credential['password'])
    await client.get_dialogs()
    channel_entity=await get_entity(client, source)
    posts = await client(GetHistoryRequest(peer=channel_entity, limit=30, # change to 30
        offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
    await client.disconnect()
    return posts

def findLinks(source):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(findLinksAsync(source))
    loop.close()
    links = {}
    for message in r.messages:
        try:
            message.media.webpage
            message.media.webpage.title
        except:
            continue
        keys = []
        for item in message.entities:
            try:
                keys.append(item.url)
            except:
                print('no item.url', item, message)
        if not keys:
            continue
        links[tuple(keys)] = (message.media.webpage.title[11:]).strip()
        if len(links) == 8:
            return links
    return links
    