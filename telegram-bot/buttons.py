from telebot import types


project_link_button = types.InlineKeyboardButton(
    text = "Мы на GitHub", 
    url = "https://github.com/Snomty/hse-cw-2025"
)


example_button_1 = types.InlineKeyboardButton(
    text = 'Удалить', 
    callback_data='delete'
)


example_button_2 = types.InlineKeyboardButton(
    text = 'Редактировать', 
    callback_data='edit'
)
