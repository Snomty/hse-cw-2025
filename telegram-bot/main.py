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
        sessions_id = create_new_session(sessions, user_id)
        bot.edit_message_text(
            successful_new_session_text,
            callback.message.chat.id, 
            callback.message.message_id,
            parse_mode='html',
            reply_markup = back_to_start_menu_markup
        )

    elif callback.data == 'cont-session':
        user_id = callback.message.from_user.id
        session_id = get_user_session(sessions, user_id)
        if session_id == -1:
            bot.edit_message_text(
                "У вас пока что нет активных сессий. Вы можете создать новую сессию по кнопке в главном меню!",
                callback.message.chat.id, 
                callback.message.message_id,
                parse_mode='html',
                reply_markup = back_to_start_menu_markup
            )
            return 0
        
        
        
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
           "description later...", 
            callback.message.chat.id, 
            callback.message.message_id, 
            parse_mode = 'html',
            reply_markup = back_to_start_menu_markup
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

print('\ndebug message\n')
sessions.to_csv("telegram-bot/sessions.csv", index=False)
