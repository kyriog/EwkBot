from abc import ABC, abstractmethod
import aiohttp
from yarl import URL

from ..description import GameSuggestionDescription


class AbstractParser(ABC):
    def __init__(self, url: URL) -> None:
        if url.host != self.HOST:
            raise
        self.url = url

    async def parse(self) -> None:
        content = await self.get_content()
        return await self.parse_content(content)
    
    async def get_content(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.text()
    
    @abstractmethod
    async def parse_content(self, content: str) -> GameSuggestionDescription:
        pass
