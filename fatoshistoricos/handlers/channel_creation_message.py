from datetime import datetime
import time


from fatoshistoricos.bot.bot import bot
from fatoshistoricos.config import *
from fatoshistoricos.database.db import *
from fatoshistoricos.loggers import logger
from fatoshistoricos.utils.get_historical import *
from fatoshistoricos.utils.month import *

data_criacao = datetime(2022, 11, 19)

def enviar_mensagem_aniversario(CHANNEL):
    try:
        data_atual = datetime.now()
        
        if data_atual.month == data_criacao.month and data_atual.day == data_criacao.day:
            anos_de_criacao = data_atual.year - data_criacao.year
            
            if anos_de_criacao == 1:
                mensagem = f"Hoje o canal Hoje na história está completando 1 ano de criação! 🎉🎂🎈"
            else:
                mensagem = f"Hoje o canal Hoje na história está completando {anos_de_criacao} anos de criação! 🎉🎂🎈"
            
            bot.send_message(CHANNEL, mensagem)
            
    except Exception as e:
        logger.error('Erro ao enviar mensagem de aniversário:', str(e))

def agendar_aniversario():
    while True:
        agora = datetime.now()
        proximo_aniversario = datetime(agora.year, data_criacao.month, data_criacao.day, 0, 0, 0)
        
        if agora >= proximo_aniversario:
            proximo_aniversario = datetime(agora.year + 1, data_criacao.month, data_criacao.day, 0, 0, 0)
        
        espera = (proximo_aniversario - agora).total_seconds()
        time.sleep(espera)
        
        enviar_mensagem_aniversario(CHANNEL) 