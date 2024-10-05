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
from AnieXEricaMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from config import adminlist
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from AnieXEricaMusic.utils.decorators.language import language
from AnieXEricaMusic.utils.formatters import alpha_to_int
from config import OWNER_ID

pros = mongodb.pro
protimes = mongodb.protime
IS_BROADCASTING = False

async def log_pro_broadcast_usage(user_id):
    current_time = datetime.utcnow()
    user_data = await protimes.find_one({"user_id": user_id})
    if user_data:
        last_broadcast = user_data.get('last_broadcast', current_time)
        broadcast_count = user_data.get('broadcast_count', 0)
        if current_time - last_broadcast >= timedelta(hours=5):
            await protimes.update_one(
                {"user_id": user_id},
                {
                    "$set": {"broadcast_count": 1, "last_broadcast": current_time}
                }
            )
            return True  
        elif broadcast_count < 2:
            await protimes.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"broadcast_count": 1},
                    "$set": {"last_broadcast": current_time}
                }
            )
            return True
        else:
            time_until_next_broadcast = (last_broadcast + timedelta(hours=5)) - current_time
            return False, time_until_next_broadcast  
    else:
        await protimes.insert_one({
            "user_id": user_id,
            "broadcast_count": 1,
            "last_broadcast": current_time
        })
        return True 
        
@app.on_message(filters.command("gcast"))
async def broadcast(client: Client, message: Message):
    global IS_BROADCASTING
    user = message.from_user
    is_pro_user = await is_pro(user.id)
    if not is_pro_user:
        return await message.reply_text(f"{user.mention}, you don't have pro access for paid broadcast.")
    if IS_BROADCASTING:
        return await message.reply_text("A broadcast is already in progress. Please wait until it finishes.")
    broadcast_result = await log_pro_broadcast_usage(user.id)
    can_broadcast = await log_pro_broadcast_usage(user.id)
    if isinstance(broadcast_result, tuple):
        can_broadcast, remaining_time = broadcast_result
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return await message.reply_text(
            f"{user.mention}, you have already used the /gcast command.\n\n"
            f"It only works 1 times in a 5-hour period. Try again after {int(hours)} hours and {int(minutes)} minutes."
            )
    if not can_broadcast:
        return await message.reply_text(f"{user.mention} can only use /gcast 2 times in a 3-hour period. Your daily broadcasts are finished. Try again tomorrow.")
    if "-wfchat" in message.text or "-wfuser" in message.text:
        if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.text):
            return await message.reply_text("Please reply to a text or image message for broadcasting.")
        if message.reply_to_message.photo:
            content_type = 'photo'
            file_id = message.reply_to_message.photo.file_id
        else:
            content_type = 'text'
            text_content = message.reply_to_message.text
        caption = message.reply_to_message.caption
        reply_markup = message.reply_to_message.reply_markup if hasattr(message.reply_to_message, 'reply_markup') else None
        IS_BROADCASTING = True
        await message.reply_text("Starting the broadcast...")
        if "-wfchat" in message.text or "-wfuser" in message.text:
            sent_chats = 0
            chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
            for i in chats:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=i, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=i, text=text_content, reply_markup=reply_markup)
                    sent_chats += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except:
                    continue
            await message.reply_text(f"Broadcast to chats completed! Sent to {sent_chats} chats.")
        if "-wfuser" in message.text:
            sent_users = 0
            users = [int(user["user_id"]) for user in await get_served_users()]
            for i in users:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=i, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=i, text=text_content, reply_markup=reply_markup)
                    sent_users += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.value)
                except:
                    continue
            await message.reply_text(f"Broadcast to users completed! Sent to {sent_users} users.")
        IS_BROADCASTING = False
        return
    if len(message.command) < 2:
        return await message.reply_text("Please provide a message to broadcast or reply to a message.")
    broadcast_message = message.text.split(None, 1)[1]
    IS_BROADCASTING = True
    await message.reply_text("Starting the text broadcast...")
    sent_chats = 0
    chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    for chat_id in chats:
        try:
            await app.send_message(chat_id, broadcast_message)
            sent_chats += 1
            await asyncio.sleep(0.2)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except:
            continue
    await message.reply_text(f"Text broadcast completed! Sent to {sent_chats} chats.")
    IS_BROADCASTING = False
    await log_pro_broadcast_usage(user.id)
    
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

@app.on_message(filters.command("addpro") & filters.user(OWNER_ID))
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
        ask_update = await message.reply_text(
            f"{user.mention} is already a pro user. Do you want to update the expiration and add more 1 days?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes", callback_data=f"update_pro:{user.id}:{duration}")],
                [InlineKeyboardButton("No", callback_data="cancel_update")]
            ])
        )
        return
    await add_pro_user(user.id, duration, message.from_user.id)
    return await message.reply_text(f"{user.mention} has been added to pro for {duration} days.")

@app.on_callback_query(filters.regex("cancel_update") & filters.user(OWNER_ID))
async def cancel_update_callback(client: Client, callback_query):
    await callback_query.message.edit_text("Update action cancelled.")
    
@app.on_callback_query(filters.regex(r"update_pro:(\d+):(\d+)") & filters.user(OWNER_ID))
async def update_pro_callback(client: Client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    additional_days = int(callback_query.matches[0].group(2))
    user_data = await pros.find_one({'user_id': user_id})
    if not user_data:
        return await callback_query.message.edit_text("Could not find the pro user.")
    current_expiration = user_data.get('expires', datetime.now())
    if isinstance(current_expiration, datetime):
        new_expiration = current_expiration + timedelta(days=additional_days)
    else:
        new_expiration = datetime.now() + timedelta(days=additional_days)
    await pros.update_one(
        {'user_id': user_id},
        {'$set': {'expires': new_expiration}}
    )
    await callback_query.message.edit_text(
        f"Pro status for user ID {user_id} has been updated. New expiration: {new_expiration.strftime('%Y-%m-%d %H:%M:%S')}."
    )


@app.on_message(filters.command("rmpro") & filters.user(OWNER_ID))
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

@app.on_message(filters.command("prolists"))
async def prolists_handler(client: Client, message: Message):
    pro_users = await pros.find().to_list(length=None)  
    if not pro_users:
        return await message.reply_text("No users have pro status.")
    pro_list_text = "Pro Users List:\n\n"
    for pro_user in pro_users:
        user_id = pro_user.get('user_id')
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
            pro_list_text += (
                f"{user.mention}\n"
                f"ID: <code>{user_id}</code>\n"
                f"Expires • <code>{expires}</code>\n"
                f"Added on • <code>{added_time}</code>\n"
                f"Added by • {added_by_user.mention}\n\n"
            )
        except Exception:
            pro_list_text += (
                f"User ID • {user_id}\n"
                f"Expires • {expires}\n"
                f"Added on • {added_time}\n"
                f"Added by • {added_by}\n\n"
            )
    await message.reply_text(pro_list_text, disable_web_page_preview=True)
