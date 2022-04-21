#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

# bot.py
import os  # for importing env vars for the bot to use
from twitchio.ext import commands
import twitch
import time
import utility

twitch_message_user = ""
temp_initial_channels = str(os.environ['CHANNEL_NAME'])


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
        print("hello")
        await create_clip(ctx)

    @commands.command()
    async def niniel(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        print("hello")
        await ctx.send(f'è un poco scema')


async def create_clip(ctx):
    channel_id = twitch.get_channel_id(temp_initial_channels[0])
    clip_object = await twitch.create_clip(channel_id)
    if clip_object != 0:
        clip_id = clip_object["id"]
        await proccess_clip(ctx, clip_id)
    else:
        print("Errore nel creare la clip")
        await ctx.channel.send("Mi dispiace, " + twitch_message_user + ", non è stato possibile creare la clip")


#	Thread for proccessing clip after X time
async def proccess_clip(ctx, clip_id):
    time.sleep(5)
    if await twitch.is_there_clip(clip_id):
        clip_url = "https://clips.twitch.tv/" + clip_id

        await ctx.channel.send("Clip di " + twitch_message_user + " " + clip_url)
        utility.write_tofile(clip_url + "\n")

    else:
        await ctx.channel.send("Sorry " + twitch_message_user + ", Twitch couldn't make the clip.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("init bot")
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
    print("init bot")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
