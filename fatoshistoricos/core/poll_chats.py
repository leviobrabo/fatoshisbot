import json
from datetime import datetime

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger


def send_poll_chat(
    chat_id,
    question,
    options,
    correct_option_id,
    explanation,
    message_thread_id,
):
    try:
        today = datetime.now()
        current_date = today.strftime('%d/%m/%Y')

        chat_info = bot.get_chat(chat_id)
        chat_type = chat_info.type

        is_anonymous = True if chat_type == 'channel' else False

        sent_poll = bot.send_poll(
            chat_id,
            question,
            options,
            is_anonymous=is_anonymous,
            type='quiz',
            correct_option_id=correct_option_id,
            explanation=explanation[:200] if explanation else None,
            message_thread_id=message_thread_id,
        )

        poll_id = sent_poll.poll.id

        add_poll_db(chat_id, poll_id, correct_option_id, current_date)
        logger.info('-' * 50)
        logger.success(f'Enviada pergunta para o chat {chat_id}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao enviar a pergunta: {e}')
        logger.info('-' * 50)


def send_question_chat():
    try:
        today = datetime.now()
        current_time = today.time()

        with open(
            './fatoshistoricos/data/perguntas.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)

        events = json_events[f'{today.month}-{today.day}']

        all_chats = get_all_chats()

        for chat in all_chats:
            chat_id = chat['chat_id']
            chat_db = search_group(chat_id)
            thread_id = chat_db.get('thread_id')
            if chat_id and chat_id != '':
                if current_time.hour == 10 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['pergunta1']['enunciado'],
                        list(events['pergunta1']['alternativas'].values()),
                        list(events['pergunta1']['alternativas']).index(
                            events['pergunta1']['correta']
                        ),
                        events['pergunta1'].get('explicacao', ''),
                        thread_id,
                    )

                elif current_time.hour == 14 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['pergunta2']['enunciado'],
                        list(events['pergunta2']['alternativas'].values()),
                        list(events['pergunta2']['alternativas']).index(
                            events['pergunta2']['correta']
                        ),
                        events['pergunta2'].get('explicacao', ''),
                        thread_id,
                    )

                elif current_time.hour == 16 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['pergunta3']['enunciado'],
                        list(events['pergunta3']['alternativas'].values()),
                        list(events['pergunta3']['alternativas']).index(
                            events['pergunta3']['correta']
                        ),
                        events['pergunta3'].get('explicacao', ''),
                        thread_id,
                    )

                elif current_time.hour == 21 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['pergunta4']['enunciado'],
                        list(events['pergunta4']['alternativas'].values()),
                        list(events['pergunta4']['alternativas']).index(
                            events['pergunta4']['correta']
                        ),
                        events['pergunta4'].get('explicacao', ''),
                        thread_id,
                    )

    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao enviar a pergunta: {e}')
        logger.info('-' * 50)


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    try:
        user_id = poll_answer.user.id
        first_name = poll_answer.user.first_name
        last_name = poll_answer.user.last_name
        username = poll_answer.user.username

        poll_id = poll_answer.poll_id
        option_id = poll_answer.option_ids[0]

        poll_db = search_poll(poll_id)
        correto = poll_db.get('correct_option_id')

        user = search_user(user_id)
        if not user:
            add_new_user(user_id, first_name, last_name, username)

        if option_id == correto:
            set_hit_user(user_id)
            set_questions_user(user_id)

    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao processar a resposta da enquete: {e}')
        logger.info('-' * 50)


def remove_all_poll():
    try:
        logger.success('Removido as polls do banco de dados!')
        remove_all_poll_db()
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao processar a resposta da enquete: {e}')
        logger.info('-' * 50)
