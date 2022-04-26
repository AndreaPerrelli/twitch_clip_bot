#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

# bot.py
import asyncio
import os  # for importing env vars for the bot to use
from twitchio.ext import commands
import twitch
import time
import utility
import discord_bot

twitch_message_user = ""
temp_initial_channels = str(os.environ['CHANNEL_NAME'])
TOKEN = os.getenv('DISCORD_TOKEN')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.environ['TWITCH_PASS'],
                         client_id=os.environ['CLIENT_ID'],
                         nick=os.environ['TWITCH_NICK'],
                         prefix=os.environ['TWITCH_PREFIX'],
                         initial_channels=[temp_initial_channels])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        global twitch_message_user
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)
        if message.content == "!clip":
            twitch_message_user = str(message.author.name)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def clip(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
#        if ctx.author.is_mod or ctx.author.is_subscriber:
        print("hello")
        await create_clip(ctx)
#        else:
#            print("l'utente " + ctx.author.name + " non ha i permessi per usare questo comando")


async def create_clip(ctx):
    channel_id = twitch.get_channel_id(temp_initial_channels)
    clip_object = await twitch.create_clip(channel_id)
    if clip_object != 0:
        clip_id = clip_object["id"]
        clip_edit_url = clip_object["edit_url"]
        await process_clip(ctx, clip_id, clip_edit_url)
    else:
        print("Errore nel creare la clip")
        message_to_the_chat = "Mi dispiace, " + twitch_message_user + ", non è stato possibile creare la clip"
        message_to_discord = "Non è stato possibile creare la clip"
        await ctx.channel.send(message_to_the_chat)
        #await send_clip_to_discord_channel(message_to_discord)


#	Thread for proccessing clip after X time
async def process_clip(ctx, clip_id, clip_edit_url):
    time.sleep(2)
    if await twitch.is_there_clip(clip_id):
        clip_url = "https://clips.twitch.tv/" + clip_id
        message_to_the_chat = "Clip di " + twitch_message_user + " " + clip_url
        message_to_the_user = "Ciao! Questo è il link per editare la tua clip " + clip_edit_url
        await ctx.channel.send(message_to_the_chat)
        await ctx.author.send(message_to_the_user)
        utility.write_tofile(clip_url + "\n")
        await send_clip_to_discord_channel(clip_url)

    else:
        time.sleep(5)
        if await twitch.is_there_clip(clip_id):
            clip_url = "https://clips.twitch.tv/" + clip_id
            message_to_the_chat = "Clip di " + twitch_message_user + " " + clip_url
            message_to_the_user = "Ciao! Questo è il link per editare la tua clip " + clip_edit_url
            await ctx.channel.send(message_to_the_chat)
            await ctx.author.send(message_to_the_user)
            utility.write_tofile(clip_url + "\n")
            await send_clip_to_discord_channel(clip_url)
        else:
            time.sleep(10)
            if await twitch.is_there_clip(clip_id):
                clip_url = "https://clips.twitch.tv/" + clip_id
                message_to_the_chat = "Clip di " + twitch_message_user + " " + clip_url
                message_to_the_user = "Ciao! Questo è il link per editare la tua clip " + clip_edit_url
                await ctx.channel.send(message_to_the_chat)
                await ctx.author.send(message_to_the_user)
                utility.write_tofile(clip_url + "\n")
                await send_clip_to_discord_channel(clip_url)
            else:
                await ctx.channel.send("Non è stato possibile creare la clip")

async def send_clip_to_discord_channel(message):
    twitch_clips_channel_id = 968465401140895794
    await discord.wait_until_ready()
    channel = discord.get_channel(twitch_clips_channel_id)
    await channel.send(message)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("init bot")
    twitch_bot = Bot()
    discord = discord_bot.DiscordClient()
    loop = asyncio.get_event_loop()
    print("init discord bot")
    loop.create_task(discord.start(TOKEN))
    print("init twitch bot")
    loop.create_task(twitch_bot.run())
    loop.run_forever()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
    print("init bot")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
