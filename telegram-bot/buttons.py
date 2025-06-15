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
