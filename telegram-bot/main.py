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
        text = start_information, 
        parse_mode = 'html', 
        reply_markup = start_markup
    )


@bot.callback_query_handler(func = lambda callback: "set-attr" not in callback.data)
def process_navigation(callback):

    if callback.data == 'new-session':
        user_id = callback.from_user.id
        create_new_session(sessions, user_id)
        bot.edit_message_text(
            successful_new_session_text,
            callback.message.chat.id, 
            callback.message.message_id,
            parse_mode='html',
            reply_markup = back_to_start_menu_markup
        )

    elif callback.data == 'cont-session':
        user_id = callback.from_user.id
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

        bot.edit_message_text(
            session_text,
            callback.message.chat.id, 
            callback.message.message_id,
            parse_mode='html',
            reply_markup = session_menu_markup
        )
        
    elif callback.data == 'back-to-start-menu':
        bot.edit_message_text(
            start_information, 
            callback.message.chat.id, 
            callback.message.message_id,
            parse_mode = 'html',
            reply_markup = start_markup
        )

    elif callback.data == 'save-and-end-session':
        user_id = callback.from_user.id
        session_id = get_user_session(sessions, user_id)
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



def careful_input(message, sessions, attr): 
    user_input = message.text
    validate_input = user_input
    is_correct_input = True

    if sessions[attr].dtype == np.float64:
        try:
            validate_input = float(user_input)
        except ValueError:
            is_correct_input = False

    if not is_correct_input:
        bot.send_message(
            message.chat.id, 
            text = incorrect_user_input_text, 
            parse_mode = 'html', 
        )
        bot.register_next_step_handler(message, lambda msg: careful_input(msg, sessions, attr))
        return 0
    
    user_id = message.from_user.id
    session_id = get_user_session(sessions, user_id)
    sessions.at[session_id, attr] = validate_input

    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(
        message.chat.id, 
        text = session_text, 
        parse_mode = 'html', 
        reply_markup = session_menu_markup
    )
    
    


@bot.callback_query_handler(func = lambda callback: "set-attr" in callback.data)
def process_(callback):
    attr_to_cnange = -1
    for attr in sessions.columns:
        if callback.data == 'set-attr-' + attr:
            bot.edit_message_text(
                "Введите " + attr,
                callback.message.chat.id, 
                callback.message.message_id,
                parse_mode='html'
            )
            attr_to_cnange = attr
    
    if attr_to_cnange == -1:
        return 0
    
    bot.register_next_step_handler(callback.message, lambda msg: careful_input(msg, sessions, attr_to_cnange))


@bot.message_handler(content_types=['audio', 'video', 'text', 'photo'])
def process_spam(message):
    bot.send_message(
        message.chat.id, 
        text = spam_information,
        parse_mode = 'html'
    )


if __name__ == "__main__":
    bot.infinity_polling()

    sessions.to_csv("telegram-bot/sessions.csv", index=False)
