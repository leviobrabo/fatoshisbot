from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger


@bot.message_handler(commands=['start'])
def cmd_start(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)
        first_name = message.from_user.first_name

        if not user:
            add_user_db(message)
            user = search_user(user_id)
            user_info = f"<b>#{BOT_USERNAME} #New_User</b>\n<b>User:</b> {user['first_name']}\n<b>ID:</b> <code>{user['user_id']}</code>\n<b>Username</b>: {user['username']}"
            bot.send_message(GROUP_LOG, user_info)

            logger.info(
                f'novo usuário ID: {user["user_id"]} foi criado no banco de dados'
            )

            return

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
        msg_start = f"Olá, <b>{first_name}</b>!\n\nEu sou <b>Fatos Históricos</b>, sou um bot que envia diariamente mensagens com acontecimentos históricos que ocorreram no dia do envio da mensagem.\n\nO envio da mensagem no chat privado é automático. Se você desejar parar de receber, digite /sendoff. Se quiser voltar a receber, digite /sendon\n\n<b>A mensagem é enviada todos os dias às 8 horas</b>\n\nAdicione-me em seu grupo para receber as mensagens lá.\n\n<b>Comandos:</b> /help\n\n📦<b>Meu código-fonte:</b> <a href='https://github.com/leviobrabo/fatoshisbot'>GitHub</a>"

        bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=msg_start,
            reply_markup=markup,
        )

    except Exception as e:

        logger.error(f'Erro ao enviar o start: {e}')
