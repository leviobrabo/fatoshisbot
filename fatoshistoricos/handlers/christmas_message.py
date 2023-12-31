from datetime import datetime

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def christmas_message():
    try:
        photo_url = 'https://i.imgur.com/0znRX8g.png'

        caption = f'O canal Hoje na história lhes deseja um feliz natal! 🎊❤️🎉\n\nO Natal é mais que uma comemoração, é uma nova chance que temos de nos reinventarmos e sermos pessoas melhores. Um Feliz e lindo Natal para todos!\n\nE vamos aprender mais informações sobre a história!'

        bot.send_photo(CHANNEL, photo_url, caption=caption)

    except Exception as e:

        logger.error('Erro ao enviar mensagem de natal:', str(e))
