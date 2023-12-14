from datetime import datetime

import pytz
import requests

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_holidays_of_the_day(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://pt.wikipedia.org/api/rest_v1/feed/onthisday/holidays/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            holidays = data.get('holidays', [])

            if len(holidays) > 0:
                holiday_messages = []

                for index, holiday in enumerate(holidays[:5], start=1):
                    name = f"<b>{holiday.get('text', '')}</b>"
                    info = holiday.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )

                    holiday_message = f'<i>{index}.</i> <b>Nome:</b> {name}\n<b>Informações:</b> {info}'
                    holiday_messages.append(holiday_message)

                message = f'<b>📆 | Datas comemorativas neste dia: {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(holiday_messages)
                message += '\n\n💬 Você sabia? Siga o @hoje_na_historia.'

                bot.send_message(CHANNEL, message)
            else:

                logger.info(
                    'Não há informações sobre feriados mundiais para o dia atual.'
                )

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:

        logger.error('Erro ao obter informações:', str(e))


def hist_channel_holiday():
    try:
        get_holidays_of_the_day(CHANNEL)

        logger.success(f'Feriados enviada o canal {CHANNEL}')

    except Exception as e:

        logger.error('Erro ao enviar o trabalho feriados:', str(e))
