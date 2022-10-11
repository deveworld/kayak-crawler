import asyncio
import time
import discord
from discord.ext import commands, tasks
from settings import *
from spider import Spider
from support import log


class TravelBot(commands.Bot):
    def __init__(self, command_prefix) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

        self.add_commands()

        self.spider = Spider()
        self.crawling_power = False
    
    async def on_ready(self):
        await commands.Bot.change_presence(
            self,
            status=discord.Status.online,
            activity=discord.Game('Travel Bot alpha v1')
        )

        log("Bot Start!")
        await self.sendMessage("Bot(with Crawling) Start!")

        self.crawling_task = self.loop.create_task(self.crawling())
        self.crawling_power = True

    async def sendMessage(self, msg, color = 0x00ff00, channel=None):
        if channel == None:
            channel = self.get_channel(CHANNEL_ID)

        await channel.send(
            embed = discord.Embed(
            title = "TravelBot", 
            description = msg, 
            color = color)
        )

    async def crawling(self):
        while True:
            (result, price) = await self.spider.check_price()
            if not result:
                await self.sendMessage(price, 0xff0000)
                await asyncio.sleep(WAIT)
                continue
            await self.sendMessage(price)
            await asyncio.sleep(WAIT)
    
    def add_commands(self) -> None:
        @self.command(name="on", pass_context=True)
        async def on_command(context: commands.Context):
            if self.crawling_power:
                await self.sendMessage("Already crawling running")
                return

            log("Crawling On")
            await self.sendMessage("Crawling on")
            self.crawling_task = self.loop.create_task(self.crawling())
            self.crawling_power = True

        @self.command(name="off", pass_context=True)
        async def off_command(context: commands.Context):
            if not self.crawling_power:
                await self.sendMessage("Already crawling not running")
                return

            log("Crawling Off")
            await self.sendMessage("Crawling Off")
            self.crawling_task.cancel()
            self.crawling_power = False

        @self.command(name="stop", pass_context=True)
        async def stop_command(context: commands.Context):
            log("Bot Stop")
            await self.sendMessage("Bot Stop")
            await self.close()

def exit_gracefully():
    log("Stopped Script")

if __name__ == '__main__':
    log("Started Script")
    try:
        bot = TravelBot("!")
        bot.run(DISCORD_BOT_KEY, log_handler=None)
    except BaseException as e:
        raise e
    finally:
        exit_gracefully()