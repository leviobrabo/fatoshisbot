from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger


@bot.message_handler(commands=['help'])
def cmd_help(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        text = 'Olá! Eu sou um bot programado para enviar fatos históricos todos os dias nos horários pré-determinados de 8h. \n\nAlém disso, tenho comandos incríveis que podem ser úteis para você. Fique à vontade para interagir comigo e descobrir mais sobre o mundo que nos cerca! \n\n<b>Basta clicar em um deles:</b>'

        markup = types.InlineKeyboardMarkup()
        commands = types.InlineKeyboardButton(
            'Lista de comandos', callback_data='commands'
        )
        suppport = types.InlineKeyboardButton(
            'Suporte', url='https://t.me/updatehist'
        )
        projeto = types.InlineKeyboardButton(
            '💰 Doações', url='https://t.me/updatehist'
        )

        markup.add(commands)
        markup.add(suppport, projeto)

        photo = 'https://i.imgur.com/j3H3wvJ.png'
        bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=text,
            reply_markup=markup,
        )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao enviar o help: {e}')
        logger.info('-' * 50)
