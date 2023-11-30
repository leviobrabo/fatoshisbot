import json
from datetime import datetime

import pytz
from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_holiday_br_of_the_day(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        with open(
            './fatoshistoricos/data/holidayBr.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            births = json_events.get(f'{month}-{day}', {}).get('births', [])

            if births:
                message_parts = []
                for index, birth in enumerate(births, start=1):
                    name = birth.get('name', '')
                    bullet = '•'
                    birth_message = f'<i>{bullet}</i> {name}'
                    message_parts.append(birth_message)

                message = f'<b>🎊 | Data comemorativa do dia 🇧🇷</b> \n\n<b><i>{day} de {get_month_name(month)}</i></b>\n\n💬 Você sabia? Siga o @hoje_na_historia.'
                message += '\n'.join(message_parts)
                bot.send_message(CHANNEL, message)
            else:
                logger.info('-' * 50)
                logger.warning('Não há informações sobre nascidos hoje.')
                logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro ao obter informações:', str(e))
        logger.info('-' * 50)


def hist_channel_holiday_br():
    try:
        get_holiday_br_of_the_day(CHANNEL)
        logger.info('-' * 50)
        logger.success(f'Feriados brasileiro enviada o canal {CHANNEL}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Erro ao enviar o trabalho feriados:', str(e))
        logger.info('-' * 50)
