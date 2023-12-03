from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger


@bot.message_handler(commands=['fwdoff'])
def cmd_fwdoff(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_name = message.chat.title
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup', 'channel']:
            if chat_member.status not in ('administrator', 'creator'):
                bot.reply_to(
                    message,
                    'Você precisa ser um administrador para executar esta ação.',
                )
                return

            existing_chat = search_group(chat_id)
            if not existing_chat:
                add_chat_db(chat_id, chat_name)
                send_new_group_message(message.chat)
                return

            if existing_chat.get('forwarding') == 'false':
                bot.reply_to(
                    message,
                    f'O encaminhamento do <b>{chat_name}</b> já estão desativadas.',
                )
                return

        update_forwarding_status(chat_id, 'false')
        markup = types.InlineKeyboardMarkup()
        report_bugs = types.InlineKeyboardButton(
            'Relatar bugs', url='https://t.me/kylorensbot'
        )
        markup.add(report_bugs)
        bot.reply_to(
            message,
            f'<b>⚠️ O encaminhamento do <b>{chat_name}</b> foi DESATIVADA com sucesso</b>.\n\nAgora o chat não receberá:\n\n• Imagens históricas\nEncaminhamentos do canal oficial\nQuiz de história',
            reply_markup=markup,
        )
        bot.send_message(
            GROUP_LOG,
            f'<b>#{BOT_USERNAME} #Fwdoff</b>\n\<b>Chat</b>: {chat_name}\n<b>ID:</b> <code>{chat_id}</code>',
        )

    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao desativar o encaminhamento do chat: {str(e)}')
        logger.info('-' * 50)


@bot.message_handler(commands=['fwdon'])
def cmd_fwdon(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_name = message.chat.title
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup', 'channel']:
            if chat_member.status not in ('administrator', 'creator'):
                bot.reply_to(
                    message,
                    'Você precisa ser um administrador para executar esta ação.',
                )
                return

            existing_chat = search_group(chat_id)
            if not existing_chat:
                add_chat_db(chat_id, chat_name)
                send_new_group_message(message.chat)
                return

            if existing_chat.get('forwarding') == 'true':
                bot.reply_to(
                    message,
                    f'As notificações do {chat_name} já estão ativadas.',
                )
                return

        update_forwarding_status(chat_id, 'true')
        markup = types.InlineKeyboardMarkup()
        report_bugs = types.InlineKeyboardButton(
            'Relatar bugs', url='https://t.me/kylorensbot'
        )
        markup.add(report_bugs)
        bot.reply_to(
            message,
            f'<b>O encaminhamento do {chat_name} foi ATIVADA com sucesso.</b>\n\nAgora o chat receberá:\n\n• Imagens históricas\nEncaminhamentos do canal oficial\nQuiz de história',
            reply_markup=markup,
        )
        bot.send_message(
            GROUP_LOG,
            f'<b>#{BOT_USERNAME} #Fwdon</b>\n\<b>Chat</b>: {chat_name}\n<b>ID:</b> <code>{chat_id}</code>',
        )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao ativar o encaminhamento do chat: {str(e)}')
        logger.info('-' * 50)


@bot.message_handler(commands=['settopic'])
def cmd_settopic(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if (
            message.reply_to_message
            and message.reply_to_message.message_thread_id
        ):
            thread_id = message.reply_to_message.message_thread_id
        else:
            bot.reply_to(
                message,
                'Este comando deve ser uma resposta a uma mensagem com um tópico.',
            )
            return

        if chat_type in ['group', 'supergroup']:
            if chat_member.status not in ('creator'):
                bot.reply_to(
                    message,
                    'Você precisa ser o dono do chat para executar esta ação.',
                )
                return

            update_thread_id(chat_id, thread_id)

            bot.reply_to(
                message,
                f'O Tópico foi atualizado com sucesso!\n\nThread_id= <code>{thread_id}</code>\n\nAgora você receberá os fatos históricos aqui',
            )

    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao definir o tópico: {str(e)}')
        logger.info('-' * 50)


# unsettopic


@bot.message_handler(commands=['unsettopic'])
def cmd_unsettopic(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup']:
            if chat_member.status not in ('creator'):
                bot.reply_to(
                    message,
                    'Você precisa ser o dono do chat para executar esta ação.',
                )
                return

            update_thread_id(chat_id, '')

            bot.reply_to(
                message,
                f'O envio das mensagems no tópico foi removido com sucesso!',
            )

    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao remover o tópico: {str(e)}')
        logger.info('-' * 50)


def send_new_group_message(chat):
    if chat.username:
        chatusername = f'@{chat.username}'
    else:
        chatusername = 'Private Group'
    bot.send_message(
        GROUP_LOG,
        text=f'#{BOT_USERNAME} #New_Group\n'
        f'<b>Chat:</b> {chat.title}\n'
        f'<b>ID:</b> <code>{chat.id}</code>\n'
        f'<b>Link:</b> {chatusername}',
        parse_mode='html',
        disable_web_page_preview=True,
    )
