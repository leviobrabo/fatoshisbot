import json
from datetime import datetime

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_curiosity(CHANNEL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        with open(
            './fatoshistoricos/data/curiosidade.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosidade = json_events.get(f'{month}-{day}', {})
            if curiosidade:
                info = curiosidade.get('texto', '')

                message = f'<b>Curiosidades Históricas 📜</b>\n\n<code>{info}</code>\n\n💬 Você sabia? Siga o @hoje_na_historia.'
                bot.send_message(CHANNEL, message)
            else:

                logger.info('Não há informações para o dia de hoje.')

    except Exception as e:

        logger.error('Erro ao obter informações:', str(e))


def hist_channel_curiosity():
    try:
        get_curiosity(CHANNEL)

        logger.success(f'Curiosidade enviada o canal {CHANNEL}')

    except Exception as e:

        logger.error('Erro ao enviar o trabalho curiosidade:', str(e))
