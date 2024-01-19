import json
from datetime import datetime

import pytz

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_frase(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        with open(
            './fatoshistoricos/data/frases.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            frase = json_events.get(f'{month}-{day}')
            if frase:
                quote = frase.get('quote', '')
                author = frase.get('author', '')

                message = f'<b>💡 Citação para refletir</b>\n\n"<i>{quote}"</i> - <b>{author}</b>\n\n<blockquote>💬 Você sabia? Siga o @hoje_na_historia.</blockquote>'
                bot.send_message(CHANNEL, message)
            else:

                logger.info('Não há informações para o dia de hoje.')

    except Exception as e:

        logger.error('Erro ao obter informações:', str(e))


def hist_channel_frase():
    try:
        get_frase(CHANNEL)

        logger.success(f'Frase enviada o canal {CHANNEL}')

    except Exception as e:

        logger.error('Erro ao enviar o trabalho curiosidade:', str(e))
