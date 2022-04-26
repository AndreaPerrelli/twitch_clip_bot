#  Copyright (c)  2022. Andrea Antonio Perrelli.
#   All rights reserved.

import discord


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} bot user is ready to rumble!')

    async def on_message(self, message):
        if self.user == message.author:
            return

        if message.content == "hello":
            await message.channel.send('hello right back at you!')