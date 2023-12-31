from datetime import datetime

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def new_year_message():
    try:
        photo_url = 'https://i.imgur.com/yRsKO9J.jpeg'

        caption = f'O canal Hoje na história lhes deseja um Feliz Ano Novo! 🎉🎆✨\n\nQue o ano que se inicia seja repleto de alegria, sucesso e novas conquistas. Que possamos aprender mais e continuar a jornada pelo conhecimento!\n\nE vamos explorar mais sobre a história juntos!'

        bot.send_photo(CHANNEL, photo_url, caption=caption)

    except Exception as e:

        logger.error('Erro ao enviar mensagem de natal:', str(e))
