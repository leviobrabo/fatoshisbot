import telebot

from fatoshistoricos.config import TOKEN
from fatoshistoricos.loggers import logger

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
