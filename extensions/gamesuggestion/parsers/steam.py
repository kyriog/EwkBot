from bs4 import BeautifulSoup
from yarl import URL

from .abstract import AbstractParser
from ..description import GameSuggestionDescription


class SteamParser(AbstractParser):
    HOST = "store.steampowered.com"

    async def parse_content(self, content: str) -> GameSuggestionDescription:
        bs = BeautifulSoup(content, features="html.parser")
        game = GameSuggestionDescription()
        game.url = self.url
        game.title = bs.find("div", id="appHubAppName").text
        game.description = bs.find("div", attrs={"class":"game_description_snippet"}).text
        game.image_url = URL(bs.find("div", attrs={"class":"highlight_screenshot"}).find("a")["href"])
        return game
