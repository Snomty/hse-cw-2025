from telebot import types
from PIL import Image


# ==================== КОНСТАНТЫ ТЕКСТОВ ====================
description_information = """
<b>🏠 AI-Помощник по прогнозированию цен на недвижимость</b>

<b>Ваш персональный аналитик рынка недвижимости на базе искусственного интеллекта!</b> 🚀

Этот бот помогает <b>предсказывать стоимость жилья</b> используя алгоритмы машинного обучения и анализа изображений. 
Просто введите параметры объекта!

<b>🔹 Как это работает?</b>

<b>📌 1. Создать сессию</b>
➠ Если вы <b>новичок</b> или хотите начать с чистого листа
➠ Бот подготовит новую форму для ввода данных

<b>📌 2. Продолжить сессию</b>
➠ Уже начинали работу? <b>Загрузите прошлую сессию</b>
➠ Идеально, если нужно <b>скорректировать параметры</b>

<b>📌 3. Получить предсказание</b>
➠ После заполнения данных алгоритмы машинного обучения делает <b>прогноз стоимости</b>

<b>📌 4. Сохраниться и выйти</b>
➠ Можно <b>прерваться</b> на любом этапе
➠ Вернитесь позже без потери данных!

<b>📌 5. Мы на GitHub</b>
➠ Открытый код проекта — <b>прозрачность и доверие</b>

<b>💡 Почему это удобно?</b>
✅ <b>Простота</b> — удобный интерфейс
✅ <b>Гибкость</b> — можно сохранять и редактировать сессии
✅ <b>Открытость</b> — весь код доступен для проверки
"""

successful_new_session_information = (
    "Новая сессия успешно создана! Нажмите на кнопку \n<b>Продолжить сессию</b>"
    " в главном меню, и начните заполнять данные!"
)

start_information = (
    "<b>🏡  Добро пожаловать в HomePriceAI!</b>\n\n"
    "\t\t\tВаш личный помощник в прогнозирвании цен на недвижимость на базе искусственного интеллекта"
)

incorrect_user_input_information = ("<b>📛 Ой, кажется, произошла ошибка!</b>\n\n"
    "Похоже, я не могу распознать ваш ввод. Вот что могло пойти не так:\n\n"
    "🔸 <i>Вы ввели текст вместо числа</i>\n"
    "🔸 <i>Указали значение в неправильном формате (например попыталсь ввести целое число в виде 10.0)</i>\n"
    "🔸 <i>Вместо фотографии отправили текст или иные данные</i>\n\n"
    "Попробуйте еще раз:"
)

spam_information = "Запрос не распознан, пожалустай, используйте команду <b>/start</b> чтобы начать."

no_active_session_information = (
    "У вас пока что нет активных сессий. Вы можете создать <b>новую сессию</b> по кнопке в главном меню!"
)

fill_all_data_information = (
    "<b>📝 Пожалуйста, введите все данные (кроме фото), чтобы получить предсказание</b>\n\n"
)

# ==================== ОПРЕДЕЛЕНИЕ КНОПОК ====================
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

continue_session_button = types.InlineKeyboardButton(
    text = 'Продолжить сессию', 
    callback_data = 'cont-session'
)

back_to_start_menu_button = types.InlineKeyboardButton(
    text = "Назад",
    callback_data = 'back-to-start-menu'
)

attr_photo_button = types.InlineKeyboardButton(
    text = "Фотографии ремонта",
    callback_data = 'set-attr-photos' 
)

attr_city_button = types.InlineKeyboardButton(
    text = "Город",
    callback_data = 'set-attr-city' 
)

attr_street_button = types.InlineKeyboardButton(
    text = "Адрес",
    callback_data = 'set-attr-street' 
)

attr_rooms_button = types.InlineKeyboardButton(
    text = "Количество комнат",
    callback_data = 'set-attr-rooms' 
)

attr_area_button = types.InlineKeyboardButton(
    text = "Площадь квартиры",
    callback_data = 'set-attr-area' 
)

attr_nearest_metro_button = types.InlineKeyboardButton(
    text = "Ближайшее станция метро",
    callback_data = 'set-attr-nearest_metro' 
)

attr_time_to_metro_button = types.InlineKeyboardButton(
    text = "Время до станции",
    callback_data = 'set-attr-time_to_metro' 
)

attr_nearest_pond_button = types.InlineKeyboardButton(
    text = "Ближайший парк",
    callback_data = 'set-attr-nearest_pond' 
)

attr_distance_pond_button = types.InlineKeyboardButton(
    text = "Расстояние до парка",
    callback_data = 'set-attr-distance_pond' 
)

get_prediction_button = types.InlineKeyboardButton(
    text = "Получить прдсказание",
    callback_data = 'get-predict' 
)

end_and_save_session_button = types.InlineKeyboardButton(
    text = "Сохранить и закончить",
    callback_data = 'save-and-end-session'
)

back_to_session_menu_button = types.InlineKeyboardButton(
    text = "Назад",
    callback_data = 'cont-session'
)


# ==================== КЛАВИАТУРЫ ====================
start_markup = types.InlineKeyboardMarkup()
start_markup.add(description_button)
start_markup.row(new_session_button , continue_session_button )
start_markup.add(project_link_button)

back_to_start_menu_markup = types.InlineKeyboardMarkup()
back_to_start_menu_markup.add(back_to_start_menu_button)

back_to_session_menu_markup = types.InlineKeyboardMarkup()
back_to_session_menu_markup.add(back_to_session_menu_button)

incorrect_user_input_markup = types.InlineKeyboardMarkup()
incorrect_user_input_markup.add(back_to_session_menu_button)

session_menu_markup = types.InlineKeyboardMarkup()
session_menu_markup.add(attr_photo_button)
session_menu_markup.row(attr_city_button, attr_street_button)
session_menu_markup.row(attr_rooms_button, attr_area_button)
session_menu_markup.row(attr_nearest_metro_button, attr_time_to_metro_button)
session_menu_markup.row(attr_nearest_pond_button, attr_distance_pond_button)
session_menu_markup.add(get_prediction_button)
session_menu_markup.add(end_and_save_session_button)


# ==================== ДРУГИЕ РЕСУРСЫ ====================
img_logo = Image.open("telegram-bot/logo.png")
