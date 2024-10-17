from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import config
from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message
from AnieXEricaMusic import app
from AnieXEricaMusic.utils import help_pannel
from AnieXEricaMusic.utils.database import get_lang
from AnieXEricaMusic.utils.decorators.language import LanguageStart, languageCB
from AnieXEricaMusic.utils.inline.help import help_back_markup, private_help_panel
from strings import get_string, helpers


@app.on_message(filters.command("privacy"))
async def privacy(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("View Privacy Policy", callback_data="view_privacy")],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="settings_back_helper")],
        ]
    )
    TEXT = f"""
🔒 Privacy Policy for {client.me.mention} !

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy]({config.BOT_PRIVACY}).

If you have any questions or concerns, feel free to reach out to our [Support Team](https://t.me/AM_YTSupport).
    """

    await message.reply_text(
        TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("view_privacy"))
async def on_view_privacy(client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"🔒 You can view our Privacy Policy here: [Privacy Policy]({config.BOT_PRIVACY})",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Back to Privacy", callback_data="back_to_privacy")],
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="settings_back_helper")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("back_to_privacy"))
async def on_back_to_privacy(client, callback_query: CallbackQuery):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("View Privacy Policy", callback_data="view_privacy")],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="settings_back_helper")],
        ]
    )
    TEXT = f"""
🔒 Privacy Policy for {client.me.mention} !

Your privacy is important to us. To learn more about how we collect, use, and protect your data, please review our Privacy Policy here: [Privacy Policy]({config.BOT_PRIVACY}).

If you have any questions or concerns, feel free to reach out to our [Support Team](https://t.me/AM_YTSupport).
    """
    await callback_query.message.edit_text(
        TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
