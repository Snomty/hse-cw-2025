import telebot
import os

from buttons import *
from config import API
from sessions_utility import *


bot = telebot.TeleBot(API)
sessions = load_or_create_sessions()



@bot.message_handler(commands=['start'])
def process_start(message):

    bot.send_message(
        message.chat.id, 
        text=start_information, 
        parse_mode='html', 
        reply_markup=start_markup
    )


@bot.callback_query_handler(func = lambda callback: True)
def process_callback(callback):

    if callback.data == 'new-session':
        user_id = callback.message.from_user.id
        try:
            create_new_session(user_id)
        except Exception as e:
            bot.send_message(text="Произошла ошибка, повторите попытку позже.")
        # bot.register_next_step_handler(callback.message, foo)

    elif callback.data == 'back-to-start-menu':
        bot.edit_message_text(
            start_information, 
            callback.message.chat.id, 
            callback.message.message_id,
            parse_mode = 'html',
            reply_markup = start_markup
        )
    elif callback.data == 'show-desription':
        bot.edit_message_text(
            description_information, 
            callback.message.chat.id, 
            callback.message.message_id, 
            parse_mode = 'html',
            reply_markup = description_markup
        )


@bot.message_handler(content_types=['text', 'audio', 'video'])
def process_spam(message):
    bot.send_message(
        message.chat.id, 
        text = spam_information, 
        parse_mode = 'html'
    )



@bot.message_handler(content_types=['photo'])
def process_photo(message):
    pass

@bot.message_handler()
def process_mixed(message):
    text = message.text

bot.infinity_polling()

sessions.to_csv("telegram-bot/sessions.csv", index=False)
