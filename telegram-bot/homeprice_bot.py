import telebot
import os

from homeprice_ui import *
from config import API
from sessions_utility import *


bot = telebot.TeleBot(API)
sessions = load_or_create_sessions()


@bot.message_handler(commands=['start'])
def process_start(message):
    bot.send_photo(
        message.chat.id, 
        photo = img_logo, 
        caption = start_information,
        parse_mode = 'html', 
        reply_markup = start_markup
    )

@bot.callback_query_handler(func = lambda callback: "set-attr" not in callback.data)
def process_navigation(callback):

    if callback.data == 'new-session':
        user_id = callback.from_user.id
        create_new_session(sessions, user_id)
        bot.edit_message_media(
            chat_id = callback.message.chat.id, 
            message_id = callback.message.message_id,
            media = types.InputMediaPhoto(
                img_logo, 
                caption = successful_new_session_information, 
                parse_mode = 'html'),
            reply_markup = back_to_start_menu_markup
        )

    elif callback.data == 'cont-session':
        user_id = callback.from_user.id
        session_id = get_user_session(sessions, user_id)
        if session_id == -1:
            bot.edit_message_media(
                chat_id = callback.message.chat.id, 
                message_id = callback.message.message_id,
                media = types.InputMediaPhoto(
                    img_logo, 
                    caption = no_active_session_information, 
                    parse_mode = 'html'
                ),
                reply_markup = back_to_start_menu_markup
            )
            return 0

        bot.edit_message_media(
            chat_id = callback.message.chat.id, 
            message_id = callback.message.message_id,
            media = types.InputMediaPhoto(
                media = create_series_table_image(sessions.iloc[session_id], "Ваши данные"), 
                # caption = build_session_text(sessions, user_id), 
                parse_mode = 'html'
            ),
            reply_markup = session_menu_markup
        )
        
    elif callback.data == 'back-to-start-menu':
        bot.edit_message_media(
            chat_id = callback.message.chat.id, 
            message_id = callback.message.message_id,
            media = types.InputMediaPhoto(
                img_logo, 
                caption = start_information, 
                parse_mode = 'html'
            ),
            reply_markup = start_markup
        )

    elif callback.data == 'save-and-end-session':
        user_id = callback.from_user.id
        session_id = get_user_session(sessions, user_id)
        bot.edit_message_media(
            chat_id = callback.message.chat.id, 
            message_id = callback.message.message_id,
            media = types.InputMediaPhoto(
                img_logo, 
                caption = start_information, 
                parse_mode = 'html'
            ),
            reply_markup = start_markup
        )

    elif callback.data == 'show-desription':
        bot.edit_message_media(
            chat_id = callback.message.chat.id, 
            message_id = callback.message.message_id,
            media = types.InputMediaPhoto(
                img_logo, 
                caption = description_information, 
                parse_mode = 'html'
            ),
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
            text = incorrect_user_input_information, 
            parse_mode = 'html', 
        )
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.register_next_step_handler(message, lambda msg: careful_input(msg, sessions, attr))
        return 0
    
    user_id = message.from_user.id
    session_id = get_user_session(sessions, user_id)
    sessions.at[session_id, attr] = validate_input

    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_photo(
        chat_id = message.chat.id, 
        photo = create_series_table_image(sessions.iloc[session_id], "Ваши данные"),
        parse_mode = 'html',
        reply_markup = session_menu_markup
    )

def careful_photo_input(message, sessions):
    user_id = message.from_user.id
    session_id = get_user_session(sessions, user_id)
    sessions.at[session_id, 'last_mesage_photo'] = message.message_id

    if not(hasattr(message, 'photo') and bool(message.photo)):
        bot.send_message(
            message.chat.id, 
            text = incorrect_user_input_information, 
            parse_mode = 'html', 
        )
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.register_next_step_handler(message, lambda msg: careful_photo_input(msg, sessions))
        return 0

    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_photo(
        chat_id = message.chat.id, 
        photo = create_series_table_image(sessions.iloc[session_id], "Ваши данные"),
        parse_mode = 'html',
        reply_markup = session_menu_markup
    )
    
# def careful_input_photos(message, sessions):
#     msg = bot.copy_message(chat_id, chat_id, message_id) 
#     unique_photos = {}
    
#     for photo in message.photo:
#         if photo.file_unique_id not in unique_photos:
#             unique_photos[photo.file_unique_id] = photo
    
#     saved_photos = []
    
#     for file_unique_id, photo in unique_photos.items():
#         file_info = bot.get_file(photo.file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
        
#         img = Image.open(io.BytesIO(downloaded_file))

#     bot.reply_to(message, reply)
    
@bot.callback_query_handler(func = lambda callback: "set-attr" in callback.data)
def process_set_attributes(callback):
    user_id = callback.message.from_user.id
    session_id = get_user_session(sessions, user_id)

    attr_to_cnange = -1
    for attr in sessions.columns:
        if callback.data == 'set-attr-photos':
            try:
                bot.edit_message_media(
                    chat_id = callback.message.chat.id, 
                    message_id = callback.message.message_id,
                    media = types.InputMediaPhoto(
                        create_series_table_image(sessions.iloc[session_id], "Ваши данные"), 
                        caption = "Загрузите одно или несколько фото", 
                        parse_mode = 'html'
                    )
                )
                bot.register_next_step_handler(callback.message, lambda msg: careful_photo_input(msg, sessions))
            except Exception:
                pass

        if callback.data == 'set-attr-' + attr:
            bot.edit_message_media(
                chat_id = callback.message.chat.id, 
                message_id = callback.message.message_id,
                media = types.InputMediaPhoto(
                    create_series_table_image(sessions.iloc[session_id], "Ваши данные"), 
                    caption = "Введите " + attr, 
                    parse_mode = 'html'
                )
            )
            attr_to_cnange = attr
    
    if attr_to_cnange == -1:
        return 0
            
    bot.register_next_step_handler(callback.message, lambda msg: careful_input(msg, sessions, attr_to_cnange))


if __name__ == "__main__":
    bot.infinity_polling()

    sessions.to_csv("telegram-bot/sessions.csv", index=False)
