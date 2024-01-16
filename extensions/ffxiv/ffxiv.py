from io import BytesIO
from math import ceil
from typing import List, Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext.commands import Cog

from botewk import EwkBot
from .utils import generate_kweh, quote_emet

class FFXIVCog(Cog):
    group = app_commands.Group(name="ffxiv", description="FFXIV Commands")

    def __init__(self, bot: EwkBot, config: dict) -> None:
        self.bot = bot
        self.config = config

    @group.command(name="mascotte", description="Compare les possessions de mascottes")
    @app_commands.rename(item="nom_de_mascotte", hidden="masqué")
    @app_commands.describe(item="Peut être précédé de la langue de recherche (ex \"fr_G'raha\")", hidden="Masque la réponse aux autres membres")
    async def minions(self, interaction: discord.Interaction, item: int, hidden: Optional[bool] = False):
        await interaction.response.defer(ephemeral=hidden)
        lang = interaction.locale.value[0:2]
        embed = discord.Embed()
        embed.url = f"https://ffxivcollect.com/minions/{item}"
        async with aiohttp.ClientSession() as session:
            url = f"https://ffxivcollect.com/api/minions/{item}?language={lang}"
            async with session.get(url) as response:
                json = await response.json()
                item_id = json["item_id"]
                embed.title = json["name"]
                embed.set_thumbnail(url=json["image"])
            lines = []
            for character_id in self.config['characters_ids']:
                url = f"https://ffxivcollect.com/api/characters/{character_id}?ids=true&latest=true"
                async with session.get(url) as response:
                    json = await response.json()
                    has_minion = item in json["minions"]["ids"]
                    lines.append(f"{'✓' if has_minion else '✗'} {json['name']}")
            if item_id:
                try:
                    url = f"https://universalis.app/api/v2/{self.config['world']}/{item_id}"
                    async with session.get(url) as response:
                        json = await response.json()
                        average_price = ceil(json['averagePrice'])
                        lines.append(f"[Prix moyen](https://universalis.app/market/{item_id}) : {average_price:n} gils")
                except aiohttp.ContentTypeError:
                    lines.append(f"[Prix moyen](https://universalis.app/market/{item_id}) : indisponible")
            embed.description = "\n".join(lines)
        await interaction.followup.send(embed=embed)

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
        embed = discord.Embed()
        embed.set_author(name="Alpha", icon_url="https://i.imgur.com/9iCJwkN.jpeg")
        embed.description = generate_kweh()
        await interaction.response.send_message(embed=embed)

    @group.command(description="Que peut bien en penser Emet-Selch ?")
    async def emet(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.set_author(name="Emet-Selch", icon_url="https://i.imgur.com/VoJgNx4.jpeg")
        embed.description = quote_emet()
        await interaction.response.send_message(embed=embed)

    
    @group.command(description="Exprimez-vous comme dans Final Fantasy XIV !")
    @app_commands.describe(speaker="Le nom de la personne s’exprimant", text="Le texte dans la bulle de dialogue")
    async def text(self, interaction: discord.Interaction, speaker: str, text: str):
        async with aiohttp.ClientSession() as session:
            data = {
                "speaker": speaker,
                "text": text
            }
            async with session.post('https://textboxiv.kyriog.fr', data=data) as resp:
                file = discord.File(BytesIO(await resp.read()), 'text.png')
                await interaction.response.send_message(file=file)

async def setup(bot: EwkBot):
    await bot.add_cog(FFXIVCog(bot, bot.config['ffxiv']))
