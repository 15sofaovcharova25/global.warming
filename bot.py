import telebot
import random
import os
from telebot import types
from dotenv import load_dotenv
from data import (
    FACTS_ALL, FACTS_BY_TOPIC,
    TIPS_ALL, TIPS_BY_TOPIC,
    QUIZ_BY_TOPIC, ALL_QUESTIONS
)

# Загружаем токен
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Хранилище для викторины (временное)
user_quiz = {}  # {user_id: {"question": вопрос, "message_id": id, "topic": тема}}

# ============= КАТЕГОРИИ =============

def get_fact_topics():
    """Возвращает список тем для фактов"""
    return {
        "🌡️ Климат": "climate",
        "💧 Вода": "water",
        "🏭 CO2": "co2",
        "🐼 Животные": "animals",
        "🥤 Пластик": "plastic",
        "⚡ Энергия": "energy",
        "🍔 Еда": "food",
        "👕 Одежда": "clothes",
        "🌲 Леса": "forest",
        "📱 Технологии": "tech"
    }

def get_tip_topics():
    """Возвращает список тем для советов"""
    return {
        "💡 Энергия": "energy",
        "💧 Вода": "water",
        "♻️ Отходы": "waste",
        "🥗 Еда": "food",
        "🚗 Транспорт": "transport",
        "👚 Одежда": "clothes"
    }

def get_quiz_topics():
    """Возвращает список тем для викторины"""
    return {
        "♻️ Пластик": "plastic",
        "🚗 Транспорт": "transport",
        "💡 Энергия": "energy",
        "🍔 Еда": "food",
        "💧 Вода": "water",
        "🌳 Деревья": "forest",
        "🐼 Животные": "animals",
        "👕 Одежда": "clothes",
        "🌍 Страны": "countries",
        "🔥 Потепление": "warming",
        "📱 Технологии": "tech",
        "🏙️ Города": "city",
        "🌊 Океаны": "ocean",
        "🧑 Человек": "human",
        "🔮 Будущее": "future"
    }

# ============= КНОПКИ =============

def get_main_keyboard():
    """Главное меню с кнопками"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton("📊 Факт"),
        types.KeyboardButton("🌱 Совет"),
        types.KeyboardButton("❓ Викторина"),
        types.KeyboardButton("📋 Меню")
    ]
    markup.add(*buttons)
    return markup

def get_fact_topics_keyboard():
    """Кнопки для выбора темы факта"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    topics = [
        ("🌡️ Климат", "fact_climate"),
        ("💧 Вода", "fact_water"),
        ("🏭 CO2", "fact_co2"),
        ("🐼 Животные", "fact_animals"),
        ("🥤 Пластик", "fact_plastic"),
        ("⚡ Энергия", "fact_energy"),
        ("🍔 Еда", "fact_food"),
        ("👕 Одежда", "fact_clothes"),
        ("🌲 Леса", "fact_forest"),
        ("📱 Технологии", "fact_tech"),
        ("🎲 Случайный", "fact_random")
    ]
    
    for i in range(0, len(topics), 2):
        if i+1 < len(topics):
            markup.add(
                types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]),
                types.InlineKeyboardButton(topics[i+1][0], callback_data=topics[i+1][1])
            )
        else:
            markup.add(types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]))
    
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return markup

def get_tip_topics_keyboard():
    """Кнопки для выбора темы совета"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    topics = [
        ("💡 Энергия", "tip_energy"),
        ("💧 Вода", "tip_water"),
        ("♻️ Отходы", "tip_waste"),
        ("🥗 Еда", "tip_food"),
        ("🚗 Транспорт", "tip_transport"),
        ("👚 Одежда", "tip_clothes"),
        ("🎲 Случайный", "tip_random")
    ]
    
    for i in range(0, len(topics), 2):
        if i+1 < len(topics):
            markup.add(
                types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]),
                types.InlineKeyboardButton(topics[i+1][0], callback_data=topics[i+1][1])
            )
        else:
            markup.add(types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]))
    
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return markup

def get_quiz_topics_keyboard():
    """Кнопки для выбора темы викторины"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    topics = [
        ("♻️ Пластик", "quiz_plastic"),
        ("🚗 Транспорт", "quiz_transport"),
        ("💡 Энергия", "quiz_energy"),
        ("🍔 Еда", "quiz_food"),
        ("💧 Вода", "quiz_water"),
        ("🌳 Деревья", "quiz_forest"),
        ("🐼 Животные", "quiz_animals"),
        ("👕 Одежда", "quiz_clothes"),
        ("🌍 Страны", "quiz_countries"),
        ("🔥 Потепление", "quiz_warming"),
        ("📱 Технологии", "quiz_tech"),
        ("🏙️ Города", "quiz_city"),
        ("🌊 Океаны", "quiz_ocean"),
        ("🧑 Человек", "quiz_human"),
        ("🔮 Будущее", "quiz_future"),
        ("🎲 ВСЕ ТЕМЫ", "quiz_all")
    ]
    
    for i in range(0, len(topics), 2):
        if i+1 < len(topics):
            markup.add(
                types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]),
                types.InlineKeyboardButton(topics[i+1][0], callback_data=topics[i+1][1])
            )
        else:
            markup.add(types.InlineKeyboardButton(topics[i][0], callback_data=topics[i][1]))
    
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    return markup

def get_menu_keyboard():
    """Меню выбора раздела"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 Факты", callback_data="menu_facts"),
        types.InlineKeyboardButton("🌱 Советы", callback_data="menu_tips"),
        types.InlineKeyboardButton("❓ Викторина", callback_data="menu_quiz"),
        types.InlineKeyboardButton("ℹ️ О боте", callback_data="menu_about")
    )
    return markup

# ============= КОМАНДЫ =============

@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие и главное меню"""
    bot.reply_to(message, 
        "🌍 *Добро пожаловать в Эко-бот Потепление!*\n\n"
        "Я помогу тебе узнать о глобальном потеплении\n"
        "и дам советы, как помочь планете.\n\n"
        "👇 *Выбери действие:*",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard())

@bot.message_handler(commands=['menu'])
def show_menu(message):
    """Показывает главное меню"""
    bot.send_message(message.chat.id,
        "📋 *Главное меню*\n\n"
        "Выбери раздел:",
        parse_mode='Markdown',
        reply_markup=get_menu_keyboard())

@bot.message_handler(commands=['facts'])
def facts_command(message):
    """Команда для показа меню фактов"""
    bot.send_message(message.chat.id,
        "📊 *Факты о потеплении*\n\n"
        "Выбери тему:",
        parse_mode='Markdown',
        reply_markup=get_fact_topics_keyboard())

@bot.message_handler(commands=['tips'])
def tips_command(message):
    """Команда для показа меню советов"""
    bot.send_message(message.chat.id,
        "🌱 *Эко-советы*\n\n"
        "Выбери тему:",
        parse_mode='Markdown',
        reply_markup=get_tip_topics_keyboard())

@bot.message_handler(commands=['quiz'])
def quiz_command(message):
    """Команда для показа меню викторины"""
    bot.send_message(message.chat.id,
        "❓ *Викторина*\n\n"
        "Выбери тему вопросов:",
        parse_mode='Markdown',
        reply_markup=get_quiz_topics_keyboard())

# ============= ОБРАБОТКА КНОПОК МЕНЮ =============

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    """Возврат в главное меню"""
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(
            "📋 *Главное меню*\n\n"
            "Выбери раздел:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=get_menu_keyboard()
        )
    except:
        bot.send_message(call.message.chat.id,
            "📋 *Главное меню*\n\n"
            "Выбери раздел:",
            parse_mode='Markdown',
            reply_markup=get_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "menu_facts")
def menu_facts(call):
    """Меню фактов"""
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(
            "📊 *Факты о потеплении*\n\n"
            "Выбери тему:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=get_fact_topics_keyboard()
        )
    except:
        bot.send_message(call.message.chat.id,
            "📊 *Факты о потеплении*\n\n"
            "Выбери тему:",
            parse_mode='Markdown',
            reply_markup=get_fact_topics_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "menu_tips")
def menu_tips(call):
    """Меню советов"""
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(
            "🌱 *Эко-советы*\n\n"
            "Выбери тему:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=get_tip_topics_keyboard()
        )
    except:
        bot.send_message(call.message.chat.id,
            "🌱 *Эко-советы*\n\n"
            "Выбери тему:",
            parse_mode='Markdown',
            reply_markup=get_tip_topics_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "menu_quiz")
def menu_quiz(call):
    """Меню викторины"""
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text(
            "❓ *Викторина*\n\n"
            "Выбери тему вопросов:",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=get_quiz_topics_keyboard()
        )
    except:
        bot.send_message(call.message.chat.id,
            "❓ *Викторина*\n\n"
            "Выбери тему вопросов:",
            parse_mode='Markdown',
            reply_markup=get_quiz_topics_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "menu_about")
def menu_about(call):
    """Информация о боте"""
    bot.answer_callback_query(call.id)
    
    total_facts = len(FACTS_ALL)
    total_tips = len(TIPS_ALL)
    total_quiz = len(ALL_QUESTIONS)
    fact_topics = len(get_fact_topics())
    tip_topics = len(get_tip_topics())
    quiz_topics = len(get_quiz_topics())
    
    text = (
        f"🌍 *Эко-бот Потепление*\n\n"
        f"Версия: 5.0\n\n"
        f"📊 *Факты:* {total_facts} по {fact_topics} темам\n"
        f"🌱 *Советы:* {total_tips} по {tip_topics} темам\n"
        f"❓ *Викторина:* {total_quiz} вопросов по {quiz_topics} темам\n\n"
        f"Создан для хакатона, чтобы помочь людям\n"
        f"узнать о глобальном потеплении и научиться\n"
        f"помогать планете.\n\n"
        f"Каждый маленький выбор имеет значение! 🌱"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu"))
    
    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(call.message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=markup)

# ============= ОБРАБОТКА ФАКТОВ =============

@bot.callback_query_handler(func=lambda call: call.data.startswith('fact_'))
def handle_fact_choice(call):
    """Обрабатывает выбор темы факта"""
    bot.answer_callback_query(call.id)
    
    topic_key = call.data.replace("fact_", "")
    
    # Маппинг ключей на названия тем
    topic_map = {
        "climate": "🌡️ Климат",
        "water": "💧 Вода",
        "co2": "🏭 CO2",
        "animals": "🐼 Животные",
        "plastic": "🥤 Пластик",
        "energy": "⚡ Энергия",
        "food": "🍔 Еда",
        "clothes": "👕 Одежда",
        "forest": "🌲 Леса",
        "tech": "📱 Технологии",
        "random": "🎲 Случайная"
    }
    
    # Маппинг ключей на списки фактов
    fact_map = {
        "climate": FACTS_BY_TOPIC["Климат и температура"],
        "water": FACTS_BY_TOPIC["Ледники и вода"],
        "co2": FACTS_BY_TOPIC["CO2 и выбросы"],
        "animals": FACTS_BY_TOPIC["Животные и природа"],
        "plastic": FACTS_BY_TOPIC["Пластик и отходы"],
        "energy": FACTS_BY_TOPIC["Энергия"],
        "food": FACTS_BY_TOPIC["Еда"],
        "clothes": FACTS_BY_TOPIC["Одежда"],
        "forest": FACTS_BY_TOPIC["Леса"],
        "tech": FACTS_BY_TOPIC["Технологии"]
    }
    
    if topic_key == "random":
        # Случайная тема
        topic_name = random.choice(list(topic_map.values()))
        fact_list = random.choice(list(fact_map.values()))
        fact = random.choice(fact_list)
        display_topic = "🎲 Случайная тема"
    else:
        # Конкретная тема
        topic_name = topic_map.get(topic_key, "Тема")
        fact_list = fact_map.get(topic_key, FACTS_ALL)
        fact = random.choice(fact_list)
        display_topic = topic_name
    
    # Создаем кнопки для продолжения
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Ещё факт", callback_data=f"fact_{topic_key}"),
        types.InlineKeyboardButton("📋 Другая тема", callback_data="menu_facts"),
        types.InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_menu")
    )
    
    # Отправляем факт
    try:
        bot.edit_message_text(
            f"📊 *{display_topic}*\n\n{fact}",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(
            call.message.chat.id,
            f"📊 *{display_topic}*\n\n{fact}",
            parse_mode='Markdown',
            reply_markup=markup
        )

# ============= ОБРАБОТКА СОВЕТОВ =============

@bot.callback_query_handler(func=lambda call: call.data.startswith('tip_'))
def handle_tip_choice(call):
    """Обрабатывает выбор темы совета"""
    bot.answer_callback_query(call.id)
    
    topic_key = call.data.replace("tip_", "")
    
    # Маппинг ключей на названия тем
    topic_map = {
        "energy": "💡 Энергия",
        "water": "💧 Вода",
        "waste": "♻️ Отходы",
        "food": "🥗 Еда",
        "transport": "🚗 Транспорт",
        "clothes": "👚 Одежда",
        "random": "🎲 Случайная"
    }
    
    # Маппинг ключей на списки советов
    tip_map = {
        "energy": TIPS_BY_TOPIC["Энергия"],
        "water": TIPS_BY_TOPIC["Вода"],
        "waste": TIPS_BY_TOPIC["Отходы"],
        "food": TIPS_BY_TOPIC["Еда"],
        "transport": TIPS_BY_TOPIC["Транспорт"],
        "clothes": TIPS_BY_TOPIC["Одежда"]
    }
    
    if topic_key == "random":
        # Случайная тема
        topic_name = random.choice(list(topic_map.values()))
        tip_list = random.choice(list(tip_map.values()))
        tip = random.choice(tip_list)
        display_topic = "🎲 Случайная тема"
    else:
        # Конкретная тема
        topic_name = topic_map.get(topic_key, "Тема")
        tip_list = tip_map.get(topic_key, TIPS_ALL)
        tip = random.choice(tip_list)
        display_topic = topic_name
    
    # Создаем кнопки для продолжения
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 Ещё совет", callback_data=f"tip_{topic_key}"),
        types.InlineKeyboardButton("📋 Другая тема", callback_data="menu_tips"),
        types.InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_menu")
    )
    
    # Отправляем совет
    try:
        bot.edit_message_text(
            f"🌱 *{display_topic}*\n\n{tip}",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(
            call.message.chat.id,
            f"🌱 *{display_topic}*\n\n{tip}",
            parse_mode='Markdown',
            reply_markup=markup
        )

# ============= ВИКТОРИНА =============

def get_questions_by_topic(topic_key):
    """Возвращает вопросы по ключу темы"""
    topic_map = {
        "plastic": "Пластик и отходы",
        "transport": "Транспорт",
        "energy": "Энергия",
        "food": "Еда",
        "water": "Вода",
        "forest": "Деревья и леса",
        "animals": "Животные",
        "clothes": "Одежда",
        "countries": "Страны",
        "warming": "Глобальное потепление",
        "tech": "Технологии",
        "city": "Города",
        "ocean": "Океаны",
        "human": "Человек",
        "future": "Будущее"
    }
    
    topic_name = topic_map.get(topic_key)
    if topic_name and topic_name in QUIZ_BY_TOPIC:
        return QUIZ_BY_TOPIC[topic_name]
    return ALL_QUESTIONS

def send_quiz_question(chat_id, topic_key="all", message_id=None):
    """Отправляет вопрос викторины по выбранной теме"""
    
    # Получаем вопросы по теме
    if topic_key == "all":
        questions = ALL_QUESTIONS
        topic_display = "Все темы"
    else:
        questions = get_questions_by_topic(topic_key)
        # Находим название темы для отображения
        topic_map = {
            "plastic": "♻️ Пластик", "transport": "🚗 Транспорт", "energy": "💡 Энергия",
            "food": "🍔 Еда", "water": "💧 Вода", "forest": "🌳 Деревья",
            "animals": "🐼 Животные", "clothes": "👕 Одежда", "countries": "🌍 Страны",
            "warming": "🔥 Потепление", "tech": "📱 Технологии", "city": "🏙️ Города",
            "ocean": "🌊 Океаны", "human": "🧑 Человек", "future": "🔮 Будущее"
        }
        topic_display = topic_map.get(topic_key, topic_key)
    
    if not questions:
        bot.send_message(chat_id, 
            "😕 По этой теме пока нет вопросов. Выбери другую!")
        return
    
    # Выбираем случайный вопрос
    q = random.choice(questions)
    
    # Создаем кнопки для ответов
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Перемешиваем варианты ответов
    options = q["options"].copy()
    random.shuffle(options)
    
    for option in options:
        button = types.InlineKeyboardButton(
            option[:30] + ("..." if len(option) > 30 else ""),
            callback_data=f"answer_{option}_{questions.index(q)}_{topic_key}"
        )
        markup.add(button)
    
    # Добавляем кнопки управления
    markup.add(
        types.InlineKeyboardButton("🔄 Следующий", callback_data=f"next_{topic_key}"),
        types.InlineKeyboardButton("📋 Сменить тему", callback_data="menu_quiz"),
        types.InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_menu")
    )
    
    # Отправляем вопрос
    text = f"❓ *Тема: {topic_display}*\n\n*Вопрос:* {q['question']}\n\nВыбери ответ:"
    
    if message_id:
        try:
            bot.edit_message_text(
                text,
                chat_id,
                message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
        except:
            msg = bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
            user_quiz[chat_id] = {
                "question": q,
                "message_id": msg.message_id,
                "topic": topic_key
            }
            return
    else:
        msg = bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)
    
    # Сохраняем информацию о вопросе
    user_quiz[chat_id] = {
        "question": q,
        "message_id": msg.message_id,
        "topic": topic_key
    }

@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_'))
def handle_quiz_topic(call):
    """Обработчик выбора темы викторины"""
    bot.answer_callback_query(call.id)
    topic_key = call.data.replace("quiz_", "")
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    send_quiz_question(call.message.chat.id, topic_key)

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_quiz_answer(call):
    """Обрабатывает ответ на вопрос викторины"""
    chat_id = call.message.chat.id
    
    # Парсим данные
    parts = call.data.split('_', 3)
    user_answer = parts[1]
    q_index = int(parts[2])
    topic_key = parts[3]
    
    # Получаем вопрос из соответствующего списка
    if topic_key == "all":
        questions = ALL_QUESTIONS
    else:
        questions = get_questions_by_topic(topic_key)
    
    if q_index >= len(questions):
        bot.answer_callback_query(call.id, "Ошибка: вопрос не найден")
        return
    
    q = questions[q_index]
    
    # Проверяем правильность
    if user_answer == q["correct"]:
        result = "✅ *Правильно!*"
        emoji = "🎉"
    else:
        result = "❌ *Неправильно.*"
        emoji = "😕"
    
    # Создаем кнопки для продолжения
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("➡️ Следующий", callback_data=f"next_{topic_key}"),
        types.InlineKeyboardButton("📋 Сменить тему", callback_data="menu_quiz"),
        types.InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_menu")
    )
    
    # Формируем ответ
    response = (
        f"{emoji} {result}\n\n"
        f"*Твой ответ:* {user_answer}\n"
        f"*Правильный ответ:* {q['correct']}\n\n"
        f"*Пояснение:* {q['explanation']}"
    )
    
    # Обновляем сообщение
    try:
        bot.edit_message_text(
            response,
            chat_id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except:
        bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=markup)
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('next_'))
def next_quiz_question(call):
    """Переход к следующему вопросу викторины"""
    bot.answer_callback_query(call.id)
    topic_key = call.data.replace("next_", "")
    
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    
    send_quiz_question(call.message.chat.id, topic_key)

# ============= ОБРАБОТКА ТЕКСТОВЫХ КНОПОК =============

@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    """Обрабатывает нажатия на текстовые кнопки"""
    text = message.text
    
    if text == "📊 Факт":
        facts_command(message)
    elif text == "🌱 Совет":
        tips_command(message)
    elif text == "❓ Викторина":
        quiz_command(message)
    elif text == "📋 Меню":
        show_menu(message)
    else:
        bot.reply_to(message, 
            "❓ Я не понимаю. Используй кнопки ниже 👇",
            reply_markup=get_main_keyboard())

# ============= ЗАПУСК =============

if __name__ == '__main__':
    print("🚀 Эко-бот Потепление запущен!")
    print(f"✅ Имя: @{bot.get_me().username}")
    print(f"📊 Фактов: {len(FACTS_ALL)} по {len(get_fact_topics())} темам")
    print(f"🌱 Советов: {len(TIPS_ALL)} по {len(get_tip_topics())} темам")
    print(f"❓ Вопросов: {len(ALL_QUESTIONS)} по {len(get_quiz_topics())} темам")
    print("📋 Нажми Ctrl+C для остановки")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен.")
