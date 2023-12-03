import threading
from time import sleep

import schedule
from telebot import util

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.commands.admin import (cmd_fwdoff, cmd_fwdon,
                                            cmd_settopic,
                                            cmd_unsettopic)
from fatoshistoricos.commands.fotoshist import cmd_photo_hist
from fatoshistoricos.commands.help import cmd_help
from fatoshistoricos.commands.send import cmd_sendoff, cmd_sendon
from fatoshistoricos.commands.start import cmd_start
from fatoshistoricos.commands.sudo import (cmd_add_sudo, cmd_sudo, cmd_group,
                                           cmd_broadcast_chat,
                                           cmd_broadcast_pv, cmd_list_devs,
                                           cmd_stats, cmd_rem_sudo)
from fatoshistoricos.config import *
from fatoshistoricos.core.poll_channel import *
from fatoshistoricos.core.poll_chats import *
from fatoshistoricos.database.db import *
from fatoshistoricos.handlers.birth_of_day import *
from fatoshistoricos.handlers.curiosity_channel import *
from fatoshistoricos.handlers.death_of_day import *
from fatoshistoricos.handlers.event_hist_channel import *
from fatoshistoricos.handlers.event_hist_chats import *
from fatoshistoricos.handlers.event_hist_users import *
from fatoshistoricos.handlers.holiday import *
from fatoshistoricos.handlers.holiday_brazil import *
from fatoshistoricos.handlers.image_hist_events_channel import *
from fatoshistoricos.handlers.image_hist_events_chat import *
from fatoshistoricos.handlers.prase_channel import *
from fatoshistoricos.handlers.presidents import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.welcome import *

# bot.add_message_handler(cmd_start)
# bot.add_message_handler(cmd_help)
# bot.add_message_handler(cmd_photo_hist)
# bot.add_message_handler(cmd_add_sudo)
# bot.add_message_handler(cmd_rem_sudo)
# bot.add_message_handler(cmd_group)
# bot.add_message_handler(cmd_stats)
# bot.add_message_handler(cmd_broadcast_pv)
# bot.add_message_handler(cmd_broadcast_chat)
# bot.add_message_handler(cmd_list_devs)
# bot.add_message_handler(cmd_sudo)
# bot.add_message_handler(cmd_sendon)
# bot.add_message_handler(cmd_sendoff)
# bot.add_message_handler(cmd_fwdon)
# bot.add_message_handler(cmd_fwdoff)
# bot.add_message_handler(cmd_settopic)
# bot.add_message_handler(cmd_unsettopic)


def sudos(user_id):
    user = search_user(user_id)
    if user and user.get('sudo') == 'true':
        return True
    return False


def set_my_configs():
    try:
        bot.set_my_commands(
            [
                types.BotCommand('/start', 'Iniciar'),
                types.BotCommand('/fotoshist', 'Fotos de fatos históricos 🙂'),
                types.BotCommand('/help', 'Ajuda'),
                types.BotCommand(
                    '/sendon', 'Receberá às 8 horas a mensagem diária'
                ),
                types.BotCommand(
                    '/sendoff', 'Não receberá às 8 horas a mensagem diária'
                ),
            ],
            scope=types.BotCommandScopeAllPrivateChats(),
        )
    except Exception as ex:
        logger.error(ex)

    sudo_list = sudos()

    for sudo in sudo_list:
        try:
            bot.set_my_commands(
                [
                    types.BotCommand('/sys', 'Uso do servidor'),
                    types.BotCommand('/sudo', 'Elevar usuário'),
                    types.BotCommand('/ban', 'Banir usuário do bot'),
                    types.BotCommand('/sudolist', 'Lista de usuários sudo'),
                    types.BotCommand('/banneds', 'Lista de usuários banidos'),
                    types.BotCommand(
                        '/bcusers', 'Enviar msg broadcast para usuários'
                    ),
                    types.BotCommand(
                        '/bcgps', 'Enviar msg broadcast para grupos'
                    ),
                ],
                scope=types.BotCommandScopeChat(chat_id=sudo),
            )

        except Exception as ex:
            logger.error(ex)

    try:
        bot.set_my_commands(
            [
                types.BotCommand('/fotoshist', 'Fotos de fatos históricos 🙂'),
            ],
            scope=types.BotCommandScopeAllGroupChats(),
        )
    except Exception as ex:
        logger.error(ex)
    try:
        bot.set_my_commands(
            [
                types.BotCommand(
                    '/settopic',
                    'definir um chat como tópico para receber as mensagens diárias',
                ),
                types.BotCommand(
                    '/unsettopic',
                    'remove um chat como tópico para receber as mensagens diárias (retorna para o General)',
                ),
                types.BotCommand('/fotoshist', 'Fotos de fatos históricos 🙂'),
                types.BotCommand('/fwdon', 'ativa o encaminhamento no grupo'),
                types.BotCommand(
                    '/fwdoff', 'desativa o encaminhamento no grupo'
                ),
            ],
            scope=types.BotCommandScopeChatAdministrators(),
        )
    except Exception as ex:
        logger.error(ex)


# Envio das poll channel


schedule.every().day.at('09:30').do(send_question)
schedule.every().day.at('11:30').do(send_question)
schedule.every().day.at('14:10').do(send_question)
schedule.every().day.at('18:30').do(send_question)

# Envio das poll chats

schedule.every().day.at('10:30').do(send_question_chat)
schedule.every().day.at('13:30').do(send_question_chat)
schedule.every().day.at('16:30').do(send_question_chat)
schedule.every().day.at('18:00').do(send_question_chat)

# Remove polls do banco de dados

# schedule.every().day.at('00:00').do(remove_all_poll)


# Envio eventos histórico no chats

schedule.every().day.at('08:00').do(hist_chat_job)

# Envio eventos histórico no users

schedule.every().day.at('08:30').do(hist_user_job)

# Envio eventos histórico no channel

schedule.every().day.at('05:00').do(hist_channel_events)

# Envio dos mortos do dia no canal

schedule.every().day.at('15:30').do(hist_channel_death)

# Envio dos nascidos do dia no canal

schedule.every().day.at('01:00').do(hist_channel_birth)

# Envio dos feriados do dia no canal

schedule.every().day.at('00:00').do(hist_channel_holiday)

# Envio de feriados brasileiros no canal

schedule.every().day.at('06:30').do(hist_channel_holiday_br)

# Envio de Fotos históricas no grupo


schedule.every().day.at('15:00').do(hist_image_chat_job)

# Envio de Fotos históricas no canal

schedule.every().day.at('17:00').do(hist_channel_imgs)

# Envio de curiosidade no canal

schedule.every().day.at('10:00').do(hist_channel_curiosity)

# Envio de frases no canal

schedule.every().day.at('21:30').do(hist_channel_frase)

# Enivo dos presidentes no canal

schedule.every().day.at('20:00').do(enviar_foto_presidente)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.data.startswith('menu_start'):
            if call.message.chat.type != 'private':
                return
            user_id = call.from_user.id
            first_name = call.from_user.first_name
            user = search_user(user_id)

            if not user:
                add_user_db(call.message)
                user = search_user(user_id)
                user_info = f"<b>#{BOT_USERNAME} #New_User</b>\n<b>User:</b> {user['first_name']}\n<b>ID:</b> <code>{user['user_id']}</code>\n<b>Username</b>: {user['username']}"
                bot.send_message(GROUP_LOG, user_info)

            markup = types.InlineKeyboardMarkup()
            add_group = types.InlineKeyboardButton(
                '✨ Adicione-me em seu grupo',
                url='https://t.me/fatoshistbot?startgroup=true',
            )
            update_channel = types.InlineKeyboardButton(
                '⚙️ Atualizações do bot', url='https://t.me/updatehist'
            )
            donate = types.InlineKeyboardButton(
                '💰 Doações', callback_data='donate'
            )
            channel_ofc = types.InlineKeyboardButton(
                'Canal Oficial 🇧🇷', url='https://t.me/hoje_na_historia'
            )
            how_to_use = types.InlineKeyboardButton(
                '⚠️ Como usar o bot', callback_data='how_to_use'
            )
            config_pv = types.InlineKeyboardButton(
                '🪪 Sua conta', callback_data='config'
            )

            markup.add(add_group)
            markup.add(update_channel, channel_ofc)
            markup.add(donate, how_to_use)
            markup.add(config_pv)

            photo = 'https://i.imgur.com/j3H3wvJ.png'
            msg_start = f"Olá, <b>{first_name}</b>!\n\nEu sou <b>Fatos Históricos</b>, sou um bot que envia diariamente mensagens com acontecimentos históricos que ocorreram no dia do envio da mensagem.\n\nO envio da mensagem no chat privado é automático. Se você desejar parar de receber, digite /sendoff. Se quiser voltar a receber, digite /sendon\n\n<b>A mensagem é enviada todos os dias às 8 horas</b>\n\nAdicione-me em seu grupo para receber as mensagens lá.\n\n<b>Comandos:</b> /help\n\n📦<b>Meu código-fonte:</b> <a href='https://github.com/leviobrabo/fatoshistoricos'>GitHub</a>"

            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_start, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('menu_help'):
            if call.message.chat.type != 'private':
                return
            user_id = call.message.from_user.id
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
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )

        elif call.data.startswith('donate'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Voltar', callback_data='menu_start'
            )
            markup.add(back_to_home)
            text_msg = (
                '──❑ D 「 🤝 Doação 」❑──\n\n'
                ' ☆ <b>Pix:</b>\n <code>32dc79d2-2868-4ef0-a277-2c10725341d4</code>\n\n'
                ' ☆ <b>BTC:</b>\n <code>bc1qjxzlug0cwnfjrhacy9kkpdzxfj0mcxc079axtl</code>\n\n'
                ' ☆ <b>ETH/USDT:</b>\n <code>0x1fbde0d2a96869299049f4f6f78fbd789d167d1b</code>'
            )

            photo = 'https://i.imgur.com/j3H3wvJ.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=text_msg, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('how_to_use'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Voltar', callback_data='menu_start'
            )
            markup.add(back_to_home)
            msg_text = 'como usar o bot (Em desenvolvimento)'
            photo = 'https://i.imgur.com/j3H3wvJ.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('config'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Voltar', callback_data='menu_start'
            )
            markup.add(back_to_home)

            user_info = search_user(user_id)
            if user_info:
                msg_text = f'<b>Sua conta</b>\n\n'
                msg_text += f'<b>Nome:</b> {user_info["first_name"]}\n'
                if user_info.get('username'):
                    msg_text += f'<b>Username:</b> @{user_info["username"]}\n'
                msg_text += f'<b>Sudo:</b> {"Sim" if user_info["sudo"] == "true" else "Não"}\n'
                msg_text += f'<b>Recebe mensagem no chat privado:</b>  {"Sim" if user_info["msg_private"] == "true" else "Não"}\n'
                msg_text += (
                    f'<b>Acertos:</b> <code>{user_info["hits"]}</code>\n'
                )
                msg_text += (
                    f'<b>Questões:</b> <code>{user_info["questions"]}</code>\n'
                )

                if user_info['questions'] > 0:
                    percentage = (
                        user_info['hits'] / user_info['questions']
                    ) * 100
                    msg_text += f'<b>Porcentagem de acerto por questões:</b> <code>{percentage:.2f}%</code>\n'
                else:
                    msg_text += f'Porcentagem de acerto por questões: <code>0%</code>\n'
                photo = 'https://i.imgur.com/j3H3wvJ.png'
                bot.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    media=types.InputMediaPhoto(
                        media=photo, caption=msg_text, parse_mode='HTML'
                    ),
                    reply_markup=markup,
                )
        elif call.data.startswith('commands'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Voltar', callback_data='menu_help'
            )
            markup.add(back_to_home)
            msg_text = (
                '<b>Lista de comandos</b>\n\n'
                '/fotoshist - Fotos de fatos históricos 🙂\n'
                '/sendon - Receberá às 8 horas a mensagem diária\n'
                '/sendoff - Não receberá às 8 horas a mensagem diária\n'
                '/fwdoff - desativa o encaminhamento no grupo\n'
                '/fwdon - ativa o encaminhamento no grupo\n'
                '/settopic - definir um chat como tópico para receber as mensagens diárias\n'
                '/unsettpoic - remove um chat como tópico para receber as mensagens diárias (retorna para o General)\n'
            )
            photo = 'https://i.imgur.com/j3H3wvJ.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )

    except Exception as e:
        logger.error(e)


def polling_thread():
    logger.info('-' * 50)
    logger.success('Start polling...')
    logger.info('-' * 50)
    bot.polling(allowed_updates=util.update_types)


def schedule_thread():
    while True:
        schedule.run_pending()

        sleep(1)


polling_thread = threading.Thread(target=polling_thread)
schedule_thread = threading.Thread(target=schedule_thread)


try:
    # set_my_configs()
    polling_thread.start()
    schedule_thread.start()
except Exception as e:
    pass
