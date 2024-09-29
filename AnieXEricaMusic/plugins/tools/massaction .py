from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPermissions, Message
from AnieXEricaMusic import app

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Yes", callback_data="banall_yes"),
     InlineKeyboardButton("No", callback_data="banall_no")]
])

@app.on_message(filters.command("banall"))
async def banall(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    owner_id = None
    async for admin in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if admin.status == enums.ChatMemberStatus.OWNER:
            owner_id = admin.user.id
    
    if user_id != owner_id:
        await message.reply_text(f"Hey {message.from_user.mention}, 'banall' can only be executed by the group owner.")
        return
    confirm_msg = await message.reply(
        f"{message.from_user.mention}, are you sure you want to ban all group members?",
        reply_markup=keyboard
    )
@app.on_callback_query(filters.regex(r"^banall_(yes|no)$"))
async def handle_callback(client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    owner_id = None
    async for admin in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if admin.status == enums.ChatMemberStatus.OWNER:
            owner_id = admin.user.id
    if user_id != owner_id:
        await callback_query.answer("Only the group owner can confirm this action.", show_alert=True)
        return
    if callback_query.data == "banall_yes":
        await callback_query.message.edit("Banall process started...")
        bot = await app.get_chat_member(chat_id, app.me.id)
        if not bot.privileges.can_restrict_members:
            await callback_query.message.edit("I don't have permission to restrict members in this group.")
            return
        banned = 0
        async for member in app.get_chat_members(chat_id):
            if member.status in ['administrator', 'creator'] or member.user.id == app.me.id:
                continue 
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                banned += 1
            except Exception as e:
                print(f"Failed to ban {member.user.id}: {e}")
        await callback_query.message.edit(f"Banned {banned} members successfully.")
    elif callback_query.data == "banall_no":
        await callback_query.message.edit("Banall process canceled.")

