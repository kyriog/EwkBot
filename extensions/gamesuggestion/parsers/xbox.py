import json
import re

from bs4 import BeautifulSoup
from yarl import URL

from .abstract import AbstractParser
from ..description import GameSuggestionDescription


class XboxParser(AbstractParser):
    HOST = "www.xbox.com"

    async def parse_content(self, content: str) -> GameSuggestionDescription:
        bs = BeautifulSoup(content, features="html.parser")
        game = GameSuggestionDescription()
        game.url = self.url
        game.title = bs.find("h1").contents[0]
        game.description = bs.find("meta", attrs={"name":"description"})["content"]
        js = bs.find("script", src="").string
        screenshots = json.loads(re.search('"screenshots":(\[[^\]]+\])', js)[1])
        game.image_url = URL(screenshots[0]['url'])
        game.gamepass = bool(bs.find("svg", class_=re.compile("^ProductLogos-module__gamePassLogo")))
        return game
