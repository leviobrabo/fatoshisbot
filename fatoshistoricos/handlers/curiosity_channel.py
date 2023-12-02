import json
from datetime import datetime

import pytz

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_curiosity(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month
        print(f'{month}-{day}')
        with open(
            './fatoshistoricos/data/curiosidade.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosidade = json_events.get(f'{month}-{day}', {}).get(
                'curiosidade', []
            )
            if curiosidade:
                info = curiosidade[0].get('texto', '')

                # Para 2025 (descomente esta linha e comente a linha acima)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Curiosidades Históricas 📜</b>\n\n{info}\n\n💬 Você sabia? Siga o @hoje_na_historia.'
                bot.send_message(CHANNEL, message)
                print(info)
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
