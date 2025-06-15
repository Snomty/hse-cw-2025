from telebot import types


description_button = types.InlineKeyboardButton(
    text = "✨ Узнать возможности",
    callback_data = 'show-desription'
)


project_link_button = types.InlineKeyboardButton(
    text = "👨‍💻 GitHub проекта", 
    url = "https://github.com/Snomty/hse-cw-2025"
)


new_session_button = types.InlineKeyboardButton(
    text = 'Создать сессию', 
    callback_data = 'new-session'
)
successful_new_session_text = (
    "Новая сессия успешно создана! Нажмите на кнопку \n<b>Продолжить сессию</b>"
    " в главном меню, и начните заполнять данные!"
)


continue_session_button = types.InlineKeyboardButton(
    text = 'Продолжить сессию', 
    callback_data = 'cont-session'
)


back_to_start_menu_button = types.InlineKeyboardButton(
    text = "Назад",
    callback_data = 'back-to-start-menu'
)



start_information = (
    "<b>🏡  Добро пожаловать в HomePriceAI!</b>\n\n"
    "\t\t\tВаш личный помощник в прогнозирвании цен на недвижимость на базе искусственного интеллекта"
)
start_markup = types.InlineKeyboardMarkup()
start_markup.add(description_button)
start_markup.row(new_session_button , continue_session_button )
start_markup.add(project_link_button)


back_to_start_menu_markup = types.InlineKeyboardMarkup()
back_to_start_menu_markup.add(back_to_start_menu_button)


spam_information = "Запрос не распознан, пожалустай, используйте команду <b>/start</b> чтобы начать."


session_text = "Текущая сессия"
attr_1_button = types.InlineKeyboardButton(
    text = "Параметр 1",
    callback_data = 'set-attr-attr_1' 
)
attr_2_button = types.InlineKeyboardButton(
    text = "Параметр 2",
    callback_data = 'set-attr-attr_2' 
)
attr_3_button = types.InlineKeyboardButton(
    text = "Параметр 3",
    callback_data = 'set-attr-attr_3' 
)
get_prediction_button = types.InlineKeyboardButton(
    text = "Получить прдсказание",
    callback_data = 'get-predict' 
)
end_and_save_session_button = types.InlineKeyboardButton(
    text = "Сохранить и закончить",
    callback_data = 'save-and-end-session'
)
session_menu_markup = types.InlineKeyboardMarkup()
session_menu_markup.row(attr_1_button, attr_2_button, attr_3_button)
session_menu_markup.add(get_prediction_button)
session_menu_markup.add(end_and_save_session_button)


back_to_session_menu_button = types.InlineKeyboardButton(
    text = "Назад",
    callback_data = 'cont-session'
)
incorrect_user_input_text = ("<b>📛 Ой, кажется, произошла ошибка!</b>\n\n"
"Похоже, я не могу распознать ваш ввод. Вот что могло пойти не так:\n\n"
"🔸 <i>Вы ввели текст вместо числа</i>\n"
"🔸 <i>Указали значение в неправильном формате (например попыталсь ввести целое число в виде 10.0)</i>\n\n"
"Попробуйте еще раз:"
)
incorrect_user_input_markup = types.InlineKeyboardMarkup()
incorrect_user_input_markup.add(back_to_session_menu_button)
