import json
import os

import discord
from discord import Intents
from discord.ext.commands.bot import Bot


class EwkBot(Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = self._load_config()

    def _load_config(self):
        with open('config.json') as file:
            return json.load(file)

    async def on_connect(self):
        extensions = os.listdir("extensions/")
        for extension in extensions:
            await self.load_extension(f"extensions.{extension}")

    async def on_ready(self):
        guild = discord.Object(self.config['guild_id'])
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
