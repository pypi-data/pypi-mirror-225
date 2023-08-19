#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html_telegraph_poster import TelegraphPoster
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import yaml
import asyncio
import time

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

async def findMessages(channel_id, start_index):
    client = TelegramClient('session_file', credential['api_id'], credential['api_hash'])
    await client.start(password=credential['password'])
    await client.get_dialogs()
    channel_entity=await get_entity(client, channel_id)
    messages = []
    for i in range(1, 4):
        posts = await client(GetHistoryRequest(peer=channel_entity, limit=100,
            offset_date=None, offset_id=start_index + i * 100, max_id=0, min_id=0, add_offset=0, hash=0))
        messages += posts.messages
    await client.disconnect()
    return channel_entity, messages

def getList(db):
    real_index = 0
    raw = 0
    posts = []
    while real_index < len(db):
        raw += 1
        if raw not in db:
            continue
        brief, link = db[raw]
        real_index += 1
        posts.append(
            '<p>%d. <a href="%s">%s</a></p>' % 
            (real_index, link, brief))
    return ''.join(posts)

def post(source, db):
    p = TelegraphPoster()
    if source.username:
        author_url = 'https://t.me/' + source.username
    else:
        author_url = None
    content = getList(db)
    text = '''  
<div>
    <p><strong>【频道简介】</strong></p>
    <p><a href="%s">点此进入频道</a></p>
    <br/>
    <p><strong>【索引】</strong></p>
    %s
</div>
    ''' % (author_url, content)
    r = p.post(
        title = '【频道手册】%s ' % source.title,
        author = source.title, 
        author_url = author_url,
        text = text)
    return r['url']

def genIndex(channel_id, start_index):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    channel, messages = loop.run_until_complete(findMessages(channel_id, start_index))
    loop.close()
    db = {}
    last_filename = ''
    messages = [(message.id, time.time(), message) for message in messages]
    messages.sort()
    for message_id, _, message in messages:
        try:
            message.media.document.attributes[0].file_name
        except:
            continue
        filename = message.media.document.attributes[0].file_name
        filename = filename.split('（')[0].split('.')[0]
        if last_filename == filename:
            continue
        last_filename = filename
        db[message.id] = filename, 'https://t.me/%s/%d' % (channel.username, message.id)
    return post(channel, db)