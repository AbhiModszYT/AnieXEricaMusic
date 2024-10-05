import random
import asyncio
from datetime import date
from typing import Dict, List, Union
from AnieXEricaMusic import userbot, app
from AnieXEricaMusic.core.mongo import mongodb
from pyrogram import Client, enums, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant, ChatAdminRequired
from pyrogram.types import Message, ChatPrivileges
from typing import Optional
from random import randint
from datetime import datetime, timedelta
from AnieXEricaMusic.misc import SUDOERS
from AnieXEricaMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)

pros = mongodb.pro


async def add_pro_user(user_id: int, duration: int, added_by: int):
    expiration_date = datetime.now() + timedelta(days=duration)
    added_time = datetime.now()
    await pros.update_one(
        {'user_id': user_id},
        {'$set': {'expires': expiration_date, 'added_time': added_time, 'added_by': added_by}},
        upsert=True  
    )


async def is_pro(user_id: int) -> bool:
    user = await pros.find_one({'user_id': user_id})
    if user:
        expires = user.get('expires')
        if expires and expires > datetime.now():
            return True
    return False


async def remove_pro_user(user_id: int):
    await pros.delete_one({'user_id': user_id})


async def extract_user(message: Message) -> Optional[Message]:
    if message.reply_to_message: 
        return message.reply_to_message.from_user
    elif len(message.command) >= 2:  
        AMBOT = message.command[1]
        user = await app.get_users(AMBOT)
        return user
    else:
        return None


@app.on_message(filters.command("addpro") & SUDOERS)
async def addpro_handler(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Provide a user ID or reply to a message to add a user as pro.")
    user = await extract_user(message)
    if not user:
        return await message.reply_text("Could not find the user.")
    if user.id == message.from_user.id:
        return await message.reply_text("You cannot add yourself to pro.")
    elif user.id == app.id:
        return await message.reply_text("You cannot add the bot to pro.")
    if len(message.command) >= 3:
        try:
            duration = int(message.command[2]) 
        except ValueError:
            return await message.reply_text("Invalid duration. Please provide the number of days.")
    else:
        duration = 1 
    
    is_pro_user = await is_pro(user.id)
    if is_pro_user:
        return await message.reply_text(f"{user.mention} is already a pro user.")
    await add_pro_user(user.id, duration, message.from_user.id) 
    return await message.reply_text(f"{user.mention} has been added to pro for {duration} days.")


@app.on_message(filters.command("rmpro") & SUDOERS)
async def rmpro_handler(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Provide a user ID or reply to a message to remove the user from pro.")
    user = await extract_user(message)
    if not user:
        return await message.reply_text("Could not find the user.")
    if user.id == message.from_user.id:
        return await message.reply_text("You cannot remove yourself from pro.")
    elif user.id == app.id:
        return await message.reply_text("The bot cannot be a pro user.")
    is_pro_user = await is_pro(user.id)
    if not is_pro_user:
        return await message.reply_text(f"{user.mention} is not a pro user.")
    await remove_pro_user(user.id)
    return await message.reply_text(f"{user.mention} has been removed from pro status.")

@app.on_message(filters.command("prolists") & SUDOERS)
async def prolists_handler(client: Client, message: Message):
    pro_users = pros.find()  
    if not await pro_users.to_list(length=1):
        return await message.reply_text("No users have pro status.")
    pro_list_text = "Pro Users List:\n\n"
    async for pro_user in pro_users:
        user_id = pro_user['user_id']
        expires = pro_user.get('expires', 'Unknown')
        added_time = pro_user.get('added_time', 'Unknown')
        added_by = pro_user.get('added_by', 'Unknown')
        if isinstance(expires, datetime):
            expires = expires.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(added_time, datetime):
            added_time = added_time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            user = await app.get_users(user_id)
            added_by_user = await app.get_users(added_by)
            pro_list_text += f"• [{user.first_name}](tg://user?id={user_id}) (ID: {user_id})\n"
            pro_list_text += f"  - Expires: {expires}\n"
            pro_list_text += f"  - Added on: {added_time}\n"
            pro_list_text += f"  - Added by: [{added_by_user.first_name}](tg://user?id={added_by})\n\n"
        except Exception:
            pro_list_text += f"• User ID: {user_id}\n"
            pro_list_text += f"  - Expires: {expires}\n"
            pro_list_text += f"  - Added on: {added_time}\n"
            pro_list_text += f"  - Added by: {added_by}\n\n"
    
    await message.reply_text(pro_list_text, disable_web_page_preview=True)
