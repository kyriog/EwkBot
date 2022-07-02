import inspect

import discord
from discord import app_commands
from discord.ext.commands import Cog
from yarl import URL

from botewk import EwkBot
from .modal import GameSuggestionModal
from .description import GameSuggestionDescription
from . import parsers


class GameSuggestionCog(Cog):
    def __init__(self, bot: EwkBot) -> None:
        self.bot = bot
    
    @app_commands.command(name="jeu", description="Suggérez un jeu")
    @app_commands.describe(url="Supporte automatiquement les liens Steam et Xbox")
    async def suggest_game(self, interaction: discord.Interaction, url: str):
        game: GameSuggestionDescription = None
        real_url = URL(url)
        try:
            assert real_url.is_absolute()
        except:
            message = "L’URL indiquée n’est pas valide."
            await interaction.response.send_message(message, ephemeral=True)
            return
        for (_, cls) in inspect.getmembers(parsers, inspect.isclass):
            try:
                parser = cls(real_url)
                game = await parser.parse()
                break
            except:
                pass
        if game:
            embed = game.to_embed()
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_modal(GameSuggestionModal(real_url))


async def setup(bot: EwkBot):
    await bot.add_cog(GameSuggestionCog(bot))
