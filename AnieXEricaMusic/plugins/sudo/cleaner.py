import os
from pyrogram import filters
from pyrogram.types import Message
from AnieXEricaMusic.misc import SUDOERS
from AnieXEricaMusic import app

@app.on_message(filters.command(["clearcache", "rmdownloads","rm"]) & SUDOERS)
async def clear_misc(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    downloads = os.path.realpath("downloads")
    down_dir = os.listdir(downloads)
    pth = os.path.realpath(".")
    os_dir = os.listdir(pth)

    if down_dir:
        for file in down_dir:
            os.remove(os.path.join(downloads, file))
    if os_dir:
        for lel in os.listdir(pth):
            os.system("rm -rf *.webm *.jpg *.png")
    await message.reply_text("𝘼𝙡𝙡 𝙏𝙚𝙢𝙥 𝘿𝙞𝙧𝙚𝙘𝙩𝙤𝙧𝙞𝙚𝙨 𝙘𝙡𝙚𝙖𝙣𝙚𝙙.")