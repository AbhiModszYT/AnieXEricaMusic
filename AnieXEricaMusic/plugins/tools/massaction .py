from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPermissions
from pyrogram import Client, filters
from pyrogram.types import Message
from AnieXEricaMusic import app

@app.on_message(filters.command("banall"))
async def banall(client: Client, message: Message):
    chat_id = message.chat.id
    admins = await app.get_chat_members(chat_id, filter="administrators")
    group_owner = None
    for admin in admins:
        if admin.status == "creator":
            group_owner = admin.user.id
            break
    if message.from_user.id != group_owner:
        await message.reply_text(f"Hey {message.from_user.mention}, 'banall' can only be executed by the group owner.")
        return
    AMBOT = await message.reply(f"{message.from_user.mention}, are you sure you want to ban all group members? Type 'y' for yes or 'n' for no.")
    banall = await app.listen(chat_id)
    check = banall.text.strip().lower()
    if check not in ['y', 'yes']:
        await AMBOT.edit(f"{message.from_user.mention}, banall canceled.")
        return
    await AMBOT.edit(f"Banall started by {message.from_user.mention}...")  
    bot = await app.get_chat_member(chat_id, app.me.id)
    bot_permission = bot.privileges.can_restrict_members
    banned = 0
    if bot_permission:
        async for member in app.get_chat_members(chat_id):
            if member.status in ['administrator', 'creator'] or member.user.id == app.me.id:
                continue
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                banned += 1
            except Exception as e:
                print(f"Failed to ban {member.user.id}: {e}")
        await message.reply_text(f"Banned {banned} members successfully.")
    else:
        await message.reply_text("I either don't have permission to restrict users or you're not the owner of the group.")
