import discord
from discord import ui
from yarl import URL


class GameSuggestionModal(ui.Modal, title="Suggestion de jeu"):
    game_name = ui.TextInput(label="Nom du jeu", required=True)
    description = ui.TextInput(label="Description", required=True)
    url = ui.TextInput(label="Lien vers le jeu", required=True)
    image_url = ui.TextInput(label="Lien vers une image", required=False)
    
    def __init__(self, url: URL, *args, **kwargs) -> None:
        self.url.default = str(url)
        super().__init__(*args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed()
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.title = self.game_name.value
        embed.description = self.description.value
        embed.url = self.url.value
        try:
            image_url = URL(self.image_url.value)
            assert image_url.is_absolute()
            embed.set_image(url=image_url)
        except:
            pass
        await interaction.response.send_message(embed=embed)
