import os
import telebot
from pyt import sandbox

# Obtener la clave de API de Telegram desde una variable de entorno
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

bot = telebot.TeleBot(bot_token, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send code <Python>")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    # Usar un intérprete de Python aislado para ejecutar el código enviado por el usuario
    with sandbox.Sandbox():
        # Deshabilitar ciertas funciones peligrosas
        sandbox.disable_import()
        sandbox.disable_open()
        sandbox.disable_eval()

        # Validar y sanear el código enviado por el usuario
        my_code = sandbox.validate_and_clean(message.text)

        # Ejecutar el código enviado por el usuario
        try:
            output = os.system(my_code)
            if output=='':
                output='Empty result🤷🏻‍♀️🤷🏻‍♂️'
            bot.send_message(message.chat.id, text=output)
        except Exception as e:
            bot.send_message(message.chat.id, text='⚠️: '+str(e))

bot.infinity_polling()
