import json
from datetime import datetime, timedelta

import pytz

from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *

with open(
    './fatoshistoricos/data/presidentes.json', 'r', encoding='utf-8'
) as file:
    presidentes = json.load(file)


def enviar_foto_presidente():
    try:
        if db.presidentes.count_documents({}) == 0:
            presidente = presidentes.get('1')
            id_new = 1
            date_new = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidentes_db(id_new, date_new)
            enviar_info_pelo_canal(presidente)
        else:
            ultimo_presidente = (
                db.presidentes.find().sort([('_id', -1)]).limit(1)[0]
            )
            ultimo_id = ultimo_presidente['id']
            data_envio = datetime.strptime(
                ultimo_presidente['date'], '%Y-%m-%d'
            )

            proximo_id = int(ultimo_id) + 1
            proxima_data = data_envio + timedelta(days=1)

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            if proxima_data.date() == today.date():
                proximo_presidente = presidentes.get(str(proximo_id))
                if proximo_presidente:
                    date = proxima_data.strftime('%Y-%m-%d')
                    add_presidentes_db(proximo_id, date)

                    enviar_info_pelo_canal(proximo_presidente)
                else:
                    logger.info('-' * 50)
                    logger.error('Não há mais presidentes para enviar.')
                    logger.info('-' * 50)
            else:
                logger.info('-' * 50)
                logger.info(
                    'Ainda não é hora de enviar as informações do próximo presidente.'
                )
                logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error(
            f'Ocorreu um erro ao enviar informações do presidente: {str(e)}'
        )
        logger.info('-' * 50)


def enviar_info_pelo_canal(info_presidente):
    try:
        titulo = info_presidente.get('titulo', '')
        nome = info_presidente.get('nome', '')
        posicao = info_presidente.get('posicao', '')
        partido = info_presidente.get('partido', '')
        ano_de_mandato = info_presidente.get('ano_de_mandato', '')
        vice_presidente = info_presidente.get('vice_presidente', '')
        foto = info_presidente.get('foto', '')

        caption = (
            f'<b>{titulo}</b>\n\n'
            f'<b>Nome:</b> {nome}\n'
            f'<b>Informação:</b> {posicao}° {titulo}\n'
            f'<b>Partido:</b> {partido}\n'
            f'<b>Ano de mandato:</b> {ano_de_mandato}\n'
            f'<b>Vice-Presidente:</b> {vice_presidente}\n\n'
            f'💬 Você sabia? Siga o @hoje_na_historia.'
        )

        logger.info('-' * 50)
        logger.success('Envio de presidente concluído com sucesso!')
        logger.info('-' * 50)
        bot.send_photo(CHANNEL, photo=foto, caption=caption, parse_mode='HTML')
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Erro ao enviar foto do presidente: {str(e)}')
        logger.info('-' * 50)
