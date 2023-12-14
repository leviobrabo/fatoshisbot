import json
from datetime import datetime

from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *


def send_historical_events_user(user_id):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        user = search_user(user_id)
        events = get_historical_events()

        markup = types.InlineKeyboardMarkup()
        channel_ofc = types.InlineKeyboardButton(
            'Canal Oficial 🇧🇷', url='https://t.me/hoje_na_historia'
        )
        markup.add(channel_ofc)

        if events:
            message = f'<b>HOJE NA HISTÓRIA</b>\n\n📅 | Acontecimento em <b>{day}/{month}</b>\n\n{events}'
            sent_message = bot.send_message(
                user_id, message, parse_mode='HTML', reply_markup=markup
            )
            message_id = sent_message.message_id

            set_user_message_id(user_id, message_id)
        else:
            bot.send_message(
                user_id,
                '<b>Não há eventos históricos para hoje.</b>',
                parse_mode='HTML',
                reply_markup=markup,
            )

            logger.warning(
                f'Nenhum evento histórico para hoje no grupo {user_id}'
            )

    except Exception as e:

        logger.error(
            'Erro ao enviar fatos históricos para os usuários:', str(e)
        )


def hist_user_job():
    try:
        user_models = get_all_users({'msg_private': 'true'})
        for user_model in user_models:
            user_id = user_model['user_id']
            message_id = user_model['message_id']

            if message_id:
                try:
                    bot.delete_message(user_id, message_id)
                except Exception as e:

                    logger.warning(f'Não foi possível deletar {user_id}')

                    pass

            send_historical_events_user(user_id)

            logger.success(f'Mensagem enviada ao usuário {user_id}')

    except Exception as e:

        logger.error('Erro ao enviar para os usuários:', str(e))
