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
        with open('./fatoshistoricos/data/curiosidade.json', 'r', encoding='utf-8') as file:
            json_events = json.load(file)
            curiosidade = json_events.get(f'{month}-{day}', {})
            if curiosidade:
                info = curiosidade.get('texto', '')  

                message = f'<b>Curiosidades Históricas 📜</b>\n\n{info}\n\n💬 Você sabia? Siga o @hoje_na_historia.'
                bot.send_message(CHANNEL, message)
            else:
                logger.info('-' * 50)
                logger.info('Não há informações para o dia de hoje.')
                logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro ao obter informações:', str(e))
        logger.info('-' * 50)


def hist_channel_curiosity():
    try:
        get_curiosity(CHANNEL)
        logger.info('-' * 50)
        logger.success(f'Curiosidade enviada o canal {CHANNEL}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro ao enviar o trabalho curiosidade:', str(e))
        logger.info('-' * 50)
