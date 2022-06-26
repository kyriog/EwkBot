import logging
import os

from discord import Intents
from botewk import EwkBot


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = EwkBot(command_prefix="/", intents=Intents.default())
    bot.run(os.getenv("TOKEN"))
