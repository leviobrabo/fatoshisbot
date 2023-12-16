from sys import version_info

import telebot

python_version = f'{version_info[0]}.{version_info[1]}.{version_info[2]}'
fatoshist_version = '2.5.4'
telebot_version = telebot.__version__ if hasattr(
    telebot, '__version__') else "Versão não encontrada"
