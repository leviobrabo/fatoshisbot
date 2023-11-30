import json
from datetime import datetime

from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *


def send_historical_events_channel(CHANNEL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>HOJE NA HISTÓRIA</b>\n\n📅 | Acontecimento em <b>{day}/{month}</b>\n\n{events}\n\n💬 Você sabia? Siga o @hoje_na_historia.'
            bot.send_message(CHANNEL, message)
        else:
            bot.send_message(
                CHANNEL,
                '<b>Não há eventos históricos para hoje.</b>',
                parse_mode='HTML',
            )
            logger.info('-' * 50)
            logger.info(
                f'Nenhum evento histórico para hoje no grupo {CHANNEL}'
            )
            logger.info('-' * 50)

    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro ao enviar fatos históricos para o canal:', str(e))
        logger.info('-' * 50)


def hist_channel():
    try:
        send_historical_events_channel(CHANNEL)
        logger.info('-' * 50)
        logger.success(f'Eventos históricos enviada o canal {CHANNEL}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro no trabalho de enviar fatos hist no canal:', str(e))
        logger.info('-' * 50)
