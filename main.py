import locale
import logging
import os

from discord import Intents
from botewk import EwkBot


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
    logging.basicConfig(level=logging.INFO)
    bot = EwkBot(command_prefix="/", intents=Intents.default())
    bot.run(os.getenv("TOKEN"))
