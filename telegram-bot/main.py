import telebot

from buttons import *
from config import API

bot = telebot.TeleBot(API)


@bot.message_handler(commands=['start'])
def process_start(message):
    pass


@bot.message_handler(commands=['help'])
def process_help(message):
    help_information = "<b>Help</b> informations"

    markup = types.InlineKeyboardMarkup()
    markup.row(example_button_1, example_button_2)
    markup.add(project_link_button)

    bot.send_message(
        message.chat.id, 
        text=help_information, 
        parse_mode='html', 
        reply_markup=markup
    )

@bot.callback_query_handler(func = lambda callback: True)
def callback_example    (callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('new text', callback.message.chat.id, callback.message.message_id)



@bot.message_handler(content_types=['photo'])
def process_photo(message):
    pass

@bot.message_handler()
def process_mixed(message):
    text = message.text

bot.infinity_polling()
