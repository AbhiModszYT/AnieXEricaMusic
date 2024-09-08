import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import Message
from TeamSuperBan import app
from TeamSuperBan.misc import SUDOERS
from TeamSuperBan.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from TeamSuperBan.utils.decorators.language import language
from TeamSuperBan.utils.formatters import alpha_to_int
from config import adminlist
from pyrogram.enums import ChatMemberStatus
from TeamSuperBan.utils import get_readable_time
from datetime import datetime
import os

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


def get_args(message: Message):
    try:
        message = message.text
    except AttributeError:
        pass
    if not message:
        return False
    message = message.split(maxsplit=1)
    if len(message) <= 1:
        return []
    message = message[1]
    try:
        split = shlex.split(message)
    except ValueError:
        return message
    return list(filter(lambda x: len(x) > 0, split))

@app.on_message(filters.command("gcast") & SUDOERS)
async def gcast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        broadcast_message = message.reply_to_message if message.reply_to_message else get_arg(message)
        Man = await message.reply_text("`» sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...`")
    else:
        return await message.reply_text("ɢɪᴠᴇ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴏʀ ʀᴇᴘʟʏ")

    served_chats = []
    chats = await get_served_chats()

    for chat in chats:
        served_chats.append(int(chat["chat_id"]))

    time_expected = get_readable_time(len(served_chats))
    await Man.edit(f"sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ {app.mention}\n\nTime to take: {time_expected}")
    
    admin_chats = []
    non_admin_chats = []
    failed_chats = []
    
    for chat_id in served_chats:
        try:
            member = await app.get_chat_member(chat_id, app.me.id)
            if member.status == ChatMemberStatus.ADMINISTRATOR:
                admin_chats.append(chat_id)
            else:
                non_admin_chats.append(chat_id)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception as e:
            failed_chats.append(chat_id)
    
    sent_count = 0
  
    for chat_id in admin_chats:
        try:
            if message.reply_to_message:
                x = message.reply_to_message.id
                y = message.chat.id
                await app.forward_messages(chat_id, y, x)
            else:
                await app.send_message(chat_id, broadcast_message)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send message to admin chat_id {chat_id}: {e}")
    
    for chat_id in non_admin_chats:
        try:
            if message.reply_to_message:
                x = message.reply_to_message.id
                y = message.chat.id
                await app.forward_messages(chat_id, y, x)
            else:
                await app.send_message(chat_id, broadcast_message)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send message to non-admin chat_id {chat_id}: {e}")
    await Man.edit(f"Broadcast completed. Messages sent to {sent_count} chats.")
