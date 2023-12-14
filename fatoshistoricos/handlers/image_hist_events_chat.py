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


def send_historical_events_group_image(chat_id):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://pt.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])

        if events:
            random_event = random.choice(events)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

            caption = f'<b>Você sabia?</b>\n\nEm <b>{day} de {get_month_name(month)} de {event_year}</b>\n\n<code>{event_text}</code>'
            inline_keyboard = types.InlineKeyboardMarkup()
            inline_keyboard.add(
                types.InlineKeyboardButton(
                    text='📢 Canal Oficial', url='https://t.me/hoje_na_historia'
                )
            )

            if random_event.get('pages') and random_event['pages'][0].get(
                'thumbnail'
            ):
                photo_url = random_event['pages'][0]['thumbnail']['source']
                bot.send_photo(
                    chat_id,
                    photo_url,
                    caption,
                    parse_mode='HTML',
                    reply_markup=inline_keyboard,
                )
            else:
                bot.send_message(
                    chat_id,
                    caption,
                    parse_mode='HTML',
                    reply_markup=inline_keyboard,
                )

            logger.success(
                f'Evento histórico em foto enviado com sucesso para o chat ID {chat_id}.'
            )

        else:

            logger.info('Não há eventos históricos para o dia atual.')

    except Exception as e:

        logger.error(f'Falha ao enviar evento histórico: {e}')


def hist_image_chat_job():
    try:
        chat_models = get_all_chats({'forwarding': 'true'})
        for chat_model in chat_models:
            chat_id = chat_model['chat_id']
            if chat_id != GROUP_LOG:
                try:
                    send_historical_events_group_image(chat_id)
                except Exception as e:

                    logger.error(
                        f'Error sending imgs historical events to group {chat_id}: {str(e)}'
                    )

    except Exception as e:

        logger.error('Erro ao fazero envio das imgs para chats:', str(e))
