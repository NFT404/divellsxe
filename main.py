import os
import telebot

# Obtener la clave de API de Telegram desde una variable de entorno
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

bot = telebot.TeleBot(bot_token, parse_mode=None)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send code <Python>")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        my_code = message.text
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        bot.send_message(message.chat.id, parse_mode= 'Markdown')
        try:
            exec(my_code)
        except Exception as e:
            print('\n⚠️: '+str(e))
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        if output=='': output='Empty result🤷🏻‍♀️🤷🏻‍♂️'
        #print (output)
        bot.send_message(message.chat.id,text=output)
    except Exception as e:
        bot.send_message(message.chat.id,text='⚠️: '+e)
    finally:
        bot.send_message(message.chat.id, parse_mode= 'Markdown')


bot.infinity_polling()
