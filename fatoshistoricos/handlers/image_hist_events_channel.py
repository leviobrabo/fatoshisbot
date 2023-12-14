import random
from datetime import datetime

import pytz
import requests
from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def send_historical_events_channel_image(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://pt.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])
        events_with_photo = [
            event
            for event in events
            if event.get('pages') and event['pages'][0].get('thumbnail')
        ]

        if events:
            random_event = random.choice(events)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

        if not events_with_photo:

            logger.info('Não há eventos com fotos para enviar hoje.')

            return

        random_event = random.choice(events_with_photo)
        caption = f'<b>🖼 | História ilustrada </b>\n\nEm <b>{day} de {get_month_name(month)} de {event_year}</b>\n\n<code>{event_text}</code>\n\n💬 Você sabia? Siga o @hoje_na_historia.'

        options = {'parse_mode': 'HTML'}

        photo_url = random_event['pages'][0]['thumbnail']['source']
        bot.send_photo(CHANNEL, photo_url, caption=caption, **options)

        logger.success(
            f'Evento histórico em foto enviado com sucesso para o canal ID {CHANNEL}.'
        )

    except Exception as e:

        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_channel_imgs():
    try:
        send_historical_events_channel_image(CHANNEL)

        logger.success(f'Mensagem enviada o canal {CHANNEL}')

    except Exception as e:

        logger.error('Erro ao enviar o trabalho imgs:', str(e))
