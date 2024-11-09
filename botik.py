import telebot
from telebot import types

API_TOKEN = '8164845661:AAHlkU4ljc_bv_1s6llzUniWxjfXhro0A-o'
bot = telebot.TeleBot(API_TOKEN)
user_data = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    about_button = types.InlineKeyboardButton("О боте", callback_data="about")
    dev_button = types.InlineKeyboardButton("О разработчиках", callback_data="developers")
    my_plant_btn = types.InlineKeyboardButton("Моя проблема", callback_data="my_plant")
    markup.add(about_button, dev_button, my_plant_btn)

    bot.send_message(message.chat.id, "Привет! Я бот для ухода за растениями 🌱", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "about")
def about_bot(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Я могу дать рекомендации по уходу, для этого нажмите соответствующую кнопку")

@bot.callback_query_handler(func=lambda call: call.data == "developers")
def about_bot(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Бот разработан командой "Кто Мы"')

@bot.callback_query_handler(func=lambda call: call.data == "my_plant")
def plant_query(call):
    user_data[call.from_user.id] = {"plant": None, "issue": None}
    msg = bot.send_message(call.message.chat.id, "Введите название вашего растения: ")
    bot.register_next_step_handler(msg, get_plant_name)

def get_plant_name(message):
    user_id = message.from_user.id
    user_data[user_id]["plant"] = message.text
    msg = bot.send_message(message.chat.id, "Опишите проблему вашего растения: ")
    bot.register_next_step_handler(msg, get_issue_description)

def get_issue_description(message):
    user_id = message.from_user.id
    user_data[user_id]["issue"] = message.text
    bot.send_message(message.chat.id, f"Растение: {user_data[user_id]['plant']}\nПроблема: {user_data[user_id]['issue']}")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Я умею выполнять следующие команды:\n/start - начать общение\n/help - помощь")


bot.infinity_polling()