from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger


@bot.message_handler(commands=['sendon'])
def commands_sendon(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        if user:
            if user.get('msg_private') == 'true':
                bot.reply_to(
                    message,
                    'Você já ATIVOU a função de receber mensagens no chat privado.',
                )
            else:
                update_msg_private(user_id, 'true')
                bot.reply_to(
                    message,
                    '<b>Mensagens privadas ATIVADAS</b>. Você receberá fatos históricos todos os dias às 8 horas.',
                )
        else:
            add_user_db(message)
            bot.reply_to(message, 'Envie o comando novamente.')

    except Exception as e:
        logger.info('-' * 50)
        print(f'Erro ao ativar o recebimento dos eventos históricos: {str(e)}')
        logger.info('-' * 50)


@bot.message_handler(commands=['sendoff'])
def commands_sendff(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        if user:
            if user.get('msg_private') == 'false':
                bot.reply_to(
                    message,
                    'Você já DESATIVOU a função de receber mensagens no chat privado.',
                )
            else:
                update_msg_private(user_id, 'false')
                bot.reply_to(
                    message,
                    '<b>Mensagens privadas DESATIVADAS</b>. Você receberá fatos históricos todos os dias às 8 horas.',
                )
        else:
            add_user_db(message)
            bot.reply_to(message, 'Envie o comando novamente.')

    except Exception as e:
        logger.info('-' * 50)
        print(
            f'Erro ao desativar o recebimento dos eventos históricos: {str(e)}'
        )
        logger.info('-' * 50)
