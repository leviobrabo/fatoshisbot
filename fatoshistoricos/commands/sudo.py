import psutil
import telebot
from telebot import types

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger

bot.message_handler(commands=['add_sudo'])


def cmd_add_sudo(message):
    try:
        if message.chat.type == 'private':
            if message.from_user.id == OWNER:
                if len(message.text.split()) == 2:
                    user_id = message.from_user.id
                    user = int(message.text.split()[1])
                    user_db = search_user(user)

                    if user_db:
                        if user_db.get('sudo') == 'true':
                            bot.send_message(
                                message.chat.id,
                                'Este usuário já tem permissão de sudo.',
                            )
                        else:
                            result = set_user_sudo(user)
                        if result.modified_count > 0:
                            if message.from_user.username:
                                username = '@' + message.from_user.username
                            else:
                                username = 'Não tem um nome de usuário'
                            updated_user = search_user(user)
                            if updated_user:
                                bot.send_message(
                                    message.chat.id,
                                    f"<b>Novo sudo adicionado com sucesso</b>\n\n<b>ID:</b> <code>{user}</code>\n<b>Nome:</b> {updated_user.get('first_name')}\n<b>Username:</b> {username}",
                                )
                                bot.send_message(
                                    GROUP_LOG,
                                    f"<b>#{BOT_USERNAME} #New_sudo</b>\n<b>ID:</b> <code>{user}</code>\n<b>Name:</b> {updated_user.get('first_name')}\nU<b>sername:</b> {username}",
                                )
                        else:
                            bot.send_message(
                                message.chat.id,
                                'User not found in the database.',
                            )
                    else:
                        bot.send_message(
                            message.chat.id, 'User not found in the database.'
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        'Por favor, forneça um ID de usuário após /add_sudo.',
                    )

    except Exception as e:

        logger.error(f'Erro ao adicionar um usuário sudo: {e}')


# rem_sudo
@bot.message_handler(commands=['rem_sudo'])
def cmd_rem_sudo(message):
    try:
        if message.chat.type == 'private':
            if message.from_user.id == OWNER:
                if len(message.text.split()) == 2:
                    user_id = int(message.text.split()[1])
                    user = search_user(user_id)
                    if user:
                        if user.get('sudo') == 'false':
                            bot.send_message(
                                message.chat.id,
                                'Este usuário já não tem permissão de sudo.',
                            )
                        else:
                            result = un_set_user_sudo(user_id)
                            if result.modified_count > 0:
                                if message.from_user.username:
                                    username = '@' + message.from_user.username
                                else:
                                    username = 'Não tem um nome de usuário'
                                updated_user = search_user(user_id)
                                if updated_user:
                                    bot.send_message(
                                        message.chat.id,
                                        f"<b>User sudo removido com sucesso</b>\n\n<b>ID:</b> <code>{user_id}</code>\n<b>Nome:</b> {updated_user.get('first_name')}\n<b>Username:</b> {username}",
                                    )
                                    bot.send_message(
                                        GROUP_LOG,
                                        f"<b>#{BOT_USERNAME} #Rem_sudo</b>\n<b>ID:</b> <code>{user_id}</code>\n<b>Nome:</b> {updated_user.get('first_name')}\n<b>Username:</b> {username}",
                                    )
                            else:
                                bot.send_message(
                                    message.chat.id,
                                    'Usuário não encontrado no banco de dados.',
                                )
                    else:
                        bot.send_message(
                            message.chat.id,
                            'Usuário não encontrado no banco de dados.',
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        'Por favor, forneça um ID de usuário após /rem_sudo.',
                    )

    except Exception as e:

        logger.error(f'Erro ao remover um usuário sudo: {e}')


# grupos


@bot.message_handler(commands=['grupos'])
def cmd_group(message):
    if message.from_user.id != OWNER:
        if message.chat.type != 'private':
            return
    try:
        chats = get_all_chats().sort('chat_id', 1)

        contador = 1
        chunkSize = 3900 - len(message.text)
        messageChunks = []
        currentChunk = ''

        for chat in chats:
            if chat['chat_id'] < 0:
                groupMessage = f"<b>{contador}:</b> <b>Group=</b> {chat['chat_name']} || <b>ID:</b> <code>{chat['chat_id']}</code>\n"
                if len(currentChunk + groupMessage) > chunkSize:
                    messageChunks.append(currentChunk)
                    currentChunk = ''
                currentChunk += groupMessage
                contador += 1

        messageChunks.append(currentChunk)
        index = 0

        def markup(index):

            types.InlineKeyboardButton(
                f'<< {index + 1}',
                callback_data=f'groups:{index - 1}',
                disabled=index == 0,
            )

            types.InlineKeyboardButton(
                f'>> {index + 2}',
                callback_data=f'groups:{index + 1}',
                disabled=index == len(messageChunks) - 1,
            )

        bot.send_message(
            message.chat.id,
            messageChunks[index],
            reply_markup=markup(index),
            parse_mode='HTML',
        )

        @bot.callback_query_handler(
            func=lambda query: query.data.startswith('groups:')
        )
        def callback_handler(query):
            nonlocal index
            index = int(query.data.split(':')[1])
            markup_inline = markup(index)
            if markup_inline and markup_inline.inline_keyboard:
                markup_inline.inline_keyboard[0][0].disabled = index == 0
                markup_inline.inline_keyboard[0][1].disabled = (
                    index == len(messageChunks) - 1
                )

            bot.edit_message_text(
                chat_id=query.message.chat.id,
                message_id=query.message.message_id,
                text=messageChunks[index],
                reply_markup=markup_inline,
                parse_mode='HTML',
            )
            bot.answer_callback_query(callback_query_id=query.id)

    except Exception as e:

        logger.error(f'Erro ao enviar a lista de grupos: {e}')


# stats


@bot.message_handler(commands=['stats'])
def cmd_stats(message):
    try:
        count_users = sum(1 for _ in get_all_users())
        count_groups = sum(1 for _ in get_all_chats())
        user_stats = f' ☆ {count_users} usuários\n ☆ {count_groups} Grupos'
        bot.reply_to(message, f'\n──❑ 「 Bot Stats 」 ❑──\n\n{user_stats}')
    except Exception as e:

        logger.error(f'Erro ao enviar o stats do bot: {e}')


# broadcast


@bot.message_handler(commands=['bcusers'])
def cmd_broadcast_pv(message):
    try:
        user_id = message.from_user.id
        if message.from_user.id != OWNER:
            return
        if message.chat.type != 'private':
            return

        command_parts = message.text.split(' ')
        sent_message = bot.send_message(
            message.chat.id, '<i>Processing...</i>', parse_mode='HTML'
        )

        if message.reply_to_message:
            reply_msg = message.reply_to_message
            ulist = get_all_users()
            success_br = 0
            no_success = 0
            block_num = 0

            for user in ulist:
                try:
                    if message.text.startswith('/broadcast'):
                        bot.forward_message(
                            user['user_id'],
                            reply_msg.chat.id,
                            reply_msg.message_id,
                        )
                    elif message.text.startswith('/broadcast'):
                        bot.send_message(user['user_id'], reply_msg.text)
                    success_br += 1
                except telebot.apihelper.ApiException as err:
                    if err.result.status_code == 403:
                        block_num += 1
                    else:
                        no_success += 1

            bot.send_message(
                message.chat.id,
                f'╭─❑ 「 <b>Broadcast Concluído</b> 」 ❑──\n'
                f'│- <b>Total usuários:</b> `{sum(1 for _ in ulist)}`\n'
                f'│- <b>Ativos:</b> `{success_br}`\n'
                f'│- <b>Inativos:</b> `{block_num}`\n'
                f'│- <b>Falha:</b> `{no_success}`\n'
                f'╰❑',
            )
        else:
            if len(command_parts) < 2:
                bot.send_message(
                    message.chat.id,
                    '<i>I need text to broadcast.</i>',
                    parse_mode='HTML',
                )
                return

            query = ' '.join(command_parts[1:])
            web_preview = query.startswith('-d')
            query_ = query[2:].strip() if web_preview else query
            ulist = get_all_users()
            success_br = 0
            no_success = 0
            block_num = 0

            for user in ulist:
                try:
                    bot.send_message(
                        user['user_id'],
                        query_,
                        disable_web_page_preview=not web_preview,
                        parse_mode='HTML',
                    )
                    success_br += 1
                except telebot.apihelper.ApiException as err:
                    if err.result.status_code == 403:
                        block_num += 1
                    else:
                        no_success += 1

            bot.edit_message_text(
                chat_id=sent_message.chat.id,
                message_id=sent_message.message_id,
                text=(
                    f'╭─❑ 「 <b>Broadcast Concluído</b> 」 ❑──\n'
                    f'│- <b>Total usuários:</b> `{sum(1 for _ in ulist)}`\n'
                    f'│- <b>Ativos:</b> `{success_br}`\n'
                    f'│- <b>Inativos:</b> `{block_num}`\n'
                    f'│- <b>Falha:</b> `{no_success}`\n'
                    f'╰❑'
                ),
                parse_mode='HTML',
            )
    except Exception as e:

        logger.error(f'Erro ao enviar o broadcast para user: {e}')


# sendgp


@bot.message_handler(commands=['bcgps'])
def cmd_broadcast_chat(message):
    try:
        user_id = message.from_user.id
        if message.from_user.id != OWNER:
            return
        if message.chat.type != 'private':
            return

        command_parts = message.text.split(' ')
        sent_message = bot.send_message(
            message.chat.id, '<i>Processing...</i>', parse_mode='HTML'
        )

        if message.reply_to_message:
            reply_msg = message.reply_to_message
            ulist = get_all_chats()
            success_br = 0
            no_success = 0
            block_num = 0

            for chat in ulist:
                try:
                    if message.text.startswith('/bc'):
                        bot.forward_message(
                            chat['chat_id'],
                            reply_msg.chat.id,
                            reply_msg.message_id,
                        )
                    elif message.text.startswith('/bc'):
                        bot.send_message(chat['chat_id'], reply_msg.text)
                    success_br += 1
                except telebot.apihelper.ApiException as err:
                    if err.result.status_code == 403:
                        block_num += 1
                    else:
                        no_success += 1

            bot.send_message(
                message.chat.id,
                f'╭─❑ 「 <b>Broadcast Concluído</b> 」 ❑──\n'
                f'│- <b>Total grupos:</b> `{sum(1 for _ in ulist)}`\n'
                f'│- <b>Ativos:</b> `{success_br}`\n'
                f'│- <b>Inativos:</b> `{block_num}`\n'
                f'│- <b>Falha:</b> `{no_success}`\n'
                f'╰❑',
            )
        else:
            if len(command_parts) < 2:
                bot.send_message(
                    message.chat.id,
                    '<i>I need text to broadcast.</i>',
                    parse_mode='HTML',
                )
                return

            query = ' '.join(command_parts[1:])
            web_preview = query.startswith('-d')
            query_ = query[2:].strip() if web_preview else query
            ulist = get_all_chats()
            success_br = 0
            no_success = 0
            block_num = 0

            for chat in ulist:
                try:
                    bot.send_message(
                        chat['chat_id'],
                        query_,
                        disable_web_page_preview=not web_preview,
                        parse_mode='HTML',
                    )
                    success_br += 1
                except telebot.apihelper.ApiException as err:
                    if err.result.status_code == 403:
                        block_num += 1
                    else:
                        no_success += 1

            bot.edit_message_text(
                chat_id=sent_message.chat.id,
                message_id=sent_message.message_id,
                text=(
                    f'╭─❑ 「 <b>Broadcast Concluído</b> 」 ❑──\n'
                    f'│- <b>Total grupos:</b> `{sum(1 for _ in ulist)}`\n'
                    f'│- <b>Ativos:</b> `{success_br}`\n'
                    f'│- <b>Inativos:</b> `{block_num}`\n'
                    f'│- <b>Falha:</b> `{no_success}`\n'
                    f'╰❑'
                ),
                parse_mode='HTML',
            )
    except Exception as e:

        logger.error(f'Erro ao enviar o broadcast para grupos: {e}')


# devs


@bot.message_handler(commands=['devs'])
def cmd_list_devs(message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id
    user_db = search_user(user_id)
    if user_db and user_db.get('sudo') != 'true':
        bot.reply_to(
            message, 'Este comando só pode ser usado por desenvolvedores!'
        )
        return

    try:
        devs_data = users_with_sudo()

        devs_list = '<b>Lista de desenvolvedores:</b>\n\n'
        for user in devs_data:
            firstname = user.get('first_name', '')
            user_id = user.get('user_id', '')
            devs_list += f'<b>User:</b> {firstname} || <b>ID:</b> <code>{user_id}</code>\n'

        bot.reply_to(message, devs_list, parse_mode='HTML')
    except Exception as e:

        logger.error(f'Erro ao enviar a listas de dev: {e}')


@bot.message_handler(commands=['dev'])
def cmd_sudo(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user_db = search_user(user_id)
        if user_db and user_db.get('sudo') != 'true':
            bot.reply_to(
                message, 'Este comando só pode ser usado por desenvolvedores!'
            )
            return

        bot.reply_to(
            message,
            f'Lista de comandos\n\n'
            f'/stats - Estatística de grupos, usuarios e mensagens enviadas\n'
            f'/broadcast - envia/encaminha mensagem para todos usuários\n'
            f'/bc - envia/encaminha mensagem para todos os grupos\n'
            f'/ping - veja a latência da VPS\n'
            f'/grupos - lista todos os grupos do db\n'
            f'/fwdoff - desativa o encaminhamento no grupo\n'
            f'/fwdon - ativa o encaminhamento no grupo\n'
            f'/fwrds - Lista de grupos com encaminhamento desabilitado\n',
        )
    except Exception as e:

        logger.error(f'Erro ao enviar a listas de comandos lde dev: {e}')


@bot.message_handler(commands=['sys'])
def cmd_sys(message: types.Message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user_db = search_user(user_id)
        if user_db and user_db.get('sudo') != 'true':
            bot.reply_to(
                message, 'Este comando só pode ser usado por desenvolvedores!'
            )
            return
        bot.reply_to(
            message,
            f'\n──❑ 「 System Stats 」 ❑──\n\n ☆ CPU usage: {psutil.cpu_percent(4)} %\n ☆ RAM usage: {psutil.virtual_memory()[2]} %',
        )
    except Exception as e:

        logger.error(f'Erro ao enviar a listas de comandos lde dev: {e}')
