from datetime import datetime, timedelta

import schedule

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *


def get_current_count():
    try:
        current_count = bot.get_chat_members_count(CHANNEL_POST)
        logger.info(f'contador: {current_count}')
        current_date = datetime.now().strftime("%d/%m/%Y - %H:%M")

        last_entry = get_last_entry()

        if last_entry:
            difference_days = (datetime.strptime(current_date, "%d/%m/%Y - %H:%M") - last_entry['date']).days

            if difference_days >= 3:
                count_difference = current_count - last_entry['count']
                percentage_increase = (
                    ((count_difference) / last_entry['count']) * 100
                    if last_entry['count'] != 0
                    else 0
                )

                if count_difference > 0:
                    message = (
                        f'<b>Hoje na história aumentou a quantidade de membros:</b>\n'
                        f"<b>User antes:</b> {last_entry['count']}\n"
                        f'<b>User agora:</b> {current_count}\n'
                        f'<b>Aumento:</b> +{count_difference}\n'
                        f'<b>Porcentagem:</b> {percentage_increase:.2f}%'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)
                    last_entry['date'] = datetime.strptime(current_date, "%d/%m/%Y - %H:%M")
                    last_entry['count'] = current_count
                    update_last_entry(last_entry)

                elif count_difference < 0:
                    message = (
                        f'<b>Hoje na história diminuiu a quantidade de membros:</b>\n'
                        f"<b>User antes:</b> {last_entry['count']}\n"
                        f'<b>User agora:</b> {current_count}\n'
                        f'<b>Aumento:</b> -{abs(count_difference)}\n'
                        f'<b>Porcentagem:</b> {percentage_increase:.2f}%'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)
                    last_entry['date'] = datetime.strptime(current_date, "%d/%m/%Y - %H:%M")
                    last_entry['count'] = current_count
                    update_last_entry(last_entry)

                else:
                    message = (
                        '<b>Hoje na história a quantidade de membros permaneceu a mesma.</b>\n'
                        f'<b>Usuários:</b> {current_count}'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)
                    last_entry['date'] = datetime.strptime(current_date, "%d/%m/%Y - %H:%M")
                    last_entry['count'] = current_count
                    update_last_entry(last_entry)
        else:
            message = (
                '<b>Esta é a primeira verificação da quantidade de membros:</b>\n'
                f'<b>Usuários:</b> {current_count}'
            )

            bot.send_message(GROUP_LOG, message)
            bot.send_message(OWNER, message)

        count_user_channel(current_count, current_date)
    except Exception as e:

        logger.error('Erro ao obter informações:', str(e))
