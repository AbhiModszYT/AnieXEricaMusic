from AnieXEricaMusic import app 
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
import asyncio
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from AnieXEricaMusic.misc import SUDOERS

@app.on_message(filters.command("leave") & SUDOERS)
async def leave(_, message):
    if len(message.command) != 2:
        return await message.reply_text("Please provide a group ID. Use like: `/leave chat_id`.")
    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text(f"Invalid chat ID. Please enter a numeric ID.")
    SKY = await message.reply_text(f"Leaving chat... {app.me.mention}")
    try:
        await app.send_message(chat_id, f"{app.me.mention} Lefting chat Bye...")
        await app.leave_chat(chat_id)
        await SKY.edit(f"{app.me.mention} Left chat {chat_id}.")
    except Exception as e:
        pass
