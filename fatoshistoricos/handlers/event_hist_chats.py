import json
from datetime import datetime

from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *


def send_historical_events_group(chat_id):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        chat = search_group(chat_id)
        topic = chat.get('thread_id')
        events = get_historical_events()

        markup = types.InlineKeyboardMarkup()
        channel_ofc = types.InlineKeyboardButton(
            'Canal Oficial 🇧🇷', url='https://t.me/hoje_na_historia'
        )
        markup.add(channel_ofc)

        if events:
            message = f'<b>HOJE NA HISTÓRIA</b>\n\n📅 | Acontecimento em <b>{day}/{month}</b>\n\n{events}'
            bot.send_message(
                chat_id,
                message,
                parse_mode='HTML',
                reply_markup=markup,
                message_thread_id=topic,
            )

            logger.success(
                f'Eventos históricos enviada com sucesso para o grupo {chat_id}'
            )

        else:
            bot.send_message(
                chat_id,
                '<b>Não há eventos históricos para hoje.</b>',
                parse_mode='HTML',
                reply_markup=markup,
                message_thread_id=topic,
            )

            logger.warning(
                f'Nenhum evento histórico para hoje no grupo {chat_id}'
            )

    except Exception as e:

        logger.error('Erro ao enviar fatos históricos para os chats:', str(e))

        remove_chat_db(chat_id)

        logger.warning(
            f'Chat {chat_id} removido do banco de dados devido a erro ao enviar mensagem de eventos históricos.'
        )


def hist_chat_job():
    try:
        chat_models = get_all_chats()
        for chat_model in chat_models:
            chat_id = chat_model['chat_id']
            if chat_id != GROUP_LOG:
                try:
                    send_historical_events_group(chat_id)
                except Exception as e:

                    logger.error(
                        f'Error sending historical events to group {chat_id}: {str(e)}'
                    )

    except Exception as e:

        logger.error('Erro ao fazer o envio para chats:', str(e))
