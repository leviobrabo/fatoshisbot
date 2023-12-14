from datetime import datetime

import pytz
import requests

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_births_of_the_day(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://pt.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            births = data.get('births', [])

            if len(births) > 0:
                birth_messages = []

                for index, birth in enumerate(births[:5], start=1):
                    name = f"<b>{birth.get('text', '')}</b>"
                    info = birth.get('pages', [{}])[0].get(
                        'extract', 'Informações não disponíveis.'
                    )
                    date = birth.get('year', 'Data desconhecida.')

                    birth_message = f'<i>{index}.</i> <b>Nome:</b> {name}\n<b>Informações:</b> {info}\n<b>Data de nascimento:</b> {date}'
                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Nascimentos neste dia: {day} de {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n💬 Você sabia? Siga o @hoje_na_historia.'

                bot.send_message(CHANNEL, message)
            else:

                logger.info('Não há informações sobre nascidos hoje.')

        else:

            logger.warning('Erro ao obter informações:', response.status_code)

    except Exception as e:

        logger.error('Erro ao obter informações:', str(e))


def hist_channel_birth():
    try:
        get_births_of_the_day(CHANNEL)

        logger.success(f'Nascidos enviada o canal {CHANNEL}')

    except Exception as e:

        logger.error('Erro ao enviar o trabalho nascido:', str(e))
