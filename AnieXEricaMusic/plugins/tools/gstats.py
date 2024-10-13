import os
import time
from asyncio import sleep
from blackpink import blackpink as bp
from pyrogram import enums, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.types import Message
from AnieXEricaMusic import app
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant, ChatAdminRequired

@app.on_message(~filters.private & filters.command(["gstat"], ["/","!"]))
async def instatus(client, message):
    start_time = time.perf_counter()
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    count = await client.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("GETTING INFORMATION...")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for member in client.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(f"""
➖➖➖➖➖➖➖
➲ NAME : {message.chat.title}
➲ MEMBERS : [ {count} ]
➖➖➖➖➖➖➖
➲ BOTS : {bot}
➲ ZOMBIES : {deleted_acc}
➲ BANNED : {banned}
➲ PREMIUM USERS : {premium_acc}
➖➖➖➖➖➖➖
TIME TAKEN : {timelog} S""")
    else:
        sent_message = await message.reply_text("ONLY ADMINS CAN USE THIS !")
        await sleep(5)
        await sent_message.delete()
