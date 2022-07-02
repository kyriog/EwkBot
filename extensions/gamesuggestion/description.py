from discord import Embed
from yarl import URL

class GameSuggestionDescription:
    GAME_PASS_ICON = "https://i.imgur.com/aPmaUUb.png"

    url: URL
    title: str
    description: str
    image_url: URL
    gamepass: bool = False

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.url = str(self.url)
        embed.title = self.title
        embed.description = self.description
        embed.set_image(url=self.image_url)
        if self.gamepass:
            embed.set_thumbnail(url=self.GAME_PASS_ICON)
        return embed
