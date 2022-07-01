#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

# bot.py
import asyncio
import os  # for importing env vars for the bot to use

from twitchio.ext import commands

import LeagueOfLegends
import twitch
import time
import utility
import discord_bot
import random

from dateutil import parser

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

    @commands.command()
    async def roll(self, ctx: commands.Context, arg):
        result = random.randint(0, int(arg))
        await ctx.channel.send('The user ' + ctx.author.name + ' rolled ' + str(result) + ' point(s)')

    @commands.command()
    async def followage(self, ctx: commands.Context):
        message = await get_user_followage_relationship(ctx)
        await ctx.channel.send(message)

    @commands.command()
    async def lolrank(self, ctx: commands.Context):
        summoner = LeagueOfLegends.get_summoner_by_summoner_name()
        rank_stats = LeagueOfLegends.get_rank_by_summoner(summoner)
        message_summmoner_stats = LeagueOfLegends.output_summoner_stats(rank_stats)
        await ctx.channel.send(message_summmoner_stats)

    async def event_usernotice_subscription(self, metadata):
        channel = metadata.channel
        if channel.name == "niniel_tv":
            user_name = metadata.user.name
            months = metadata.cumulative_months
            if months == 1:
                months_message = "1 mese!"
            else:
                months_message = f"{months} mesi!"
            if months_message != "":
                message_for_subs = f"Grazie per la sub @{user_name}! Hai supportato il canale per {months_message}! Per ricevere il link per il gruppo telegram dedicato usa !sub in chat"
            else:
                message_for_subs = f"Grazie per la sub @{user_name}! Per ricevere il link per il gruppo telegram dedicato usa !sub in chat"
            await channel.send(message_for_subs)


    # @commands.command()
    # async def quack(self, ctx: commands.Context):
    #     if ctx.channel.name == "kittenniniel":
    #         niniel_telegram_link = "https://t.me/+d4TXs3A4Vn84ZTg0"
    #         message_for_subs = "Ciao! ecco a te il link per unirti al nostro gruppo telegram solo per sub! uwu " + niniel_telegram_link
    #         if ctx.author.is_subscriber:
    #             await ctx.author.send(message_for_subs)


async def create_clip(ctx):
    channel_id = twitch.get_channel_id(temp_initial_channels)
    error_message_to_the_chat = "Non è possibile creare la clip poichè il canale è offline."
    if twitch.is_stream_live(channel_id):
        clip_object = await twitch.create_clip(channel_id)
        if clip_object != 0:
            clip_id = clip_object["id"]
            clip_edit_url = clip_object["edit_url"]
            await process_clip(ctx, clip_id, clip_edit_url)
        else:
            print("Errore nel creare la clip")
            # message_to_the_chat = "Mi dispiace, " + twitch_message_user + ", non è stato possibile creare la clip"
            # message_to_discord = "Non è stato possibile creare la clip"
            # await ctx.channel.send(message_to_the_chat)
            # await send_clip_to_discord_channel(message_to_discord)
    else:
        await ctx.channel.send(error_message_to_the_chat)


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
                await create_clip(ctx)


async def send_clip_to_discord_channel(message):
    twitch_clips_channel_id = int(os.environ['DISCORD_CHANNEL'])
    await discord.wait_until_ready()
    channel = discord.get_channel(twitch_clips_channel_id)
    await channel.send(message)


async def get_user_followage_relationship(ctx):
    from_id = twitch.get_channel_id(ctx.channel.name)
    to_id = twitch.get_channel_id(ctx.author.name)
    followed_at = await twitch.get_user_followage(from_id, to_id)

    if followed_at != 0:
        followed_time = parser.parse(followed_at)
        diff = utility.getDuration(followed_time)
        if diff.years == 0:
            string_years = ""
        elif diff.years == 1:
            string_years = str(diff.years) + " anno "
        else:
            string_years = str(diff.years) + " anni "

        if diff.months == 0:
            string_months = ""
        elif diff.months == 1:
            string_months = str(diff.months) + " mese "
        else:
            string_months = str(diff.months) + " mesi "

        if diff.days == 0:
            string_days = ""
        elif diff.days == 1:
            string_days = str(diff.days) + " giorno "
        else:
            string_days = str(diff.days) + " giorni "

        if diff.hours == 0:
            string_hours = ""
        elif diff.hours == 1:
            string_hours = str(diff.hours) + " ora "
        else:
            string_hours = str(diff.hours) + " ore "

        if diff.minutes == 0:
            string_minutes = ""
        elif diff.minutes == 1:
            string_minutes = str(diff.minutes) + " minuto "
        else:
            string_minutes = str(diff.minutes) + " minuti "

        if diff.seconds == 0:
            string_seconds = ""
        elif diff.seconds == 1:
            string_seconds = str(diff.seconds) + " secondo"
        else:
            string_seconds = str(diff.seconds) + " secondi"

        message = "@" + ctx.author.name + " ha seguito " + ctx.channel.name + " per " + string_years + string_months + string_days + string_hours + string_minutes + string_seconds
    else:
        message = "@" + ctx.author.name + " non segue " + ctx.channel.name

    return message


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

