from typing import List, Optional
import aiohttp
import discord
from discord import app_commands
from discord.ext.commands import Cog

from botewk import EwkBot
from .utils import generate_kweh

class FFXIVCog(Cog):
    group = app_commands.Group(name="ffxiv", description="FFXIV Commands")

    def __init__(self, bot: EwkBot, config: dict) -> None:
        self.bot = bot
        self.config = config
        self.ctx_menu = [
            app_commands.ContextMenu(name="Appeler Alpha", callback=self.context_kweh)
        ]
        [self.bot.tree.add_command(ctx) for ctx in self.ctx_menu]
    
    async def cog_unload(self) -> None:
        [self.bot.tree.remove_command(ctx) for ctx in self.ctx_menu]

    @group.command(name="mascotte", description="Compare les possessions de mascottes")
    @app_commands.rename(item="nom_de_mascotte", hidden="masqué")
    @app_commands.describe(item="Peut être précédé de la langue de recherche (ex \"fr_G'raha\")", hidden="Masque la réponse aux autres membres")
    async def minions(self, interaction: discord.Interaction, item: int, hidden: Optional[bool] = False):
        lang = interaction.locale.value[0:2]
        embed = discord.Embed()
        embed.url = f"https://ffxivcollect.com/minions/{item}"
        async with aiohttp.ClientSession() as session:
            url = f"https://ffxivcollect.com/api/minions/{item}?language={lang}"
            async with session.get(url) as response:
                json = await response.json()
                embed.title = json["name"]
                embed.set_thumbnail(url=json["image"])
            lines = []
            for character_id in self.config['characters_ids']:
                url = f"https://ffxivcollect.com/api/characters/{character_id}?ids=true"
                async with session.get(url) as response:
                    json = await response.json()
                    has_minion = item in json["minions"]["ids"]
                    lines.append(f"{'✓' if has_minion else '✗'} {json['name']}")
            embed.description = "\n".join(lines)
        await interaction.response.send_message(embed=embed, ephemeral=hidden)

    @minions.autocomplete('item')
    async def item_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        try:
            [lang, current] = current.split("_")
        except ValueError:
            lang = "en"
        async with aiohttp.ClientSession() as session:
            url = f"https://ffxivcollect.com/api/minions?name_{lang}_cont={current}&limit=25&language={lang}"
            async with session.get(url) as response:
                json = await response.json()
                return [app_commands.Choice(name=result["name"], value=result["id"]) for result in json["results"][0:25]]
    
    @group.command(description="Appelez Alpha à l’aide !")
    async def kweh(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.kweh_embed())
    
    async def context_kweh(self, interaction: discord.Interaction, message: discord.Message):
        await message.reply(embed=self.kweh_embed())

    def kweh_embed(self):
        embed = discord.Embed()
        embed.set_author(name="Alpha", icon_url="https://i.imgur.com/9iCJwkN.jpeg")
        embed.description = generate_kweh()
        return embed

async def setup(bot: EwkBot):
    await bot.add_cog(FFXIVCog(bot, bot.config['ffxiv']))
