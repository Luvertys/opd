import telebot
from telebot import types
import requests


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
    bot.send_message(call.message.chat.id, 'Я могу дать рекомендации по уходу, для этого нажмите кнопку "Моя проблема"')

@bot.callback_query_handler(func=lambda call: call.data == "developers")
def about_bot(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Бот разработан командой "Кто. Мы"')

@bot.callback_query_handler(func=lambda call: call.data == "my_plant")
def plant_query(call):
    user_data[call.from_user.id] = {"issue": None}
    msg = bot.send_message(call.message.chat.id, "Опишите проблему вашего растения:  ")
    bot.register_next_step_handler(msg, get_issue_description)


def get_issue_description(message):
    user_id = message.from_user.id
    user_data[user_id]["issue"] = message.text

    req = {
        "modelUri": "ds://b1g1u2pbs0tgd2e5sgqd/bt1i5tpvefui1a50vm5n",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": f"{user_data[user_id]['issue']}"
            }
        ]
    }
    headers = {"Authorization": "Api-Key AQVNyDMaibnhcQ2sepygJn4mb3lQM4OM7zA0aAHQ"}
    res = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                        headers=headers, json=req)
    result = res.json()
    reply_text = result['result']['alternatives'][0]['message']['text']
    bot.send_message(message.chat.id, f"{reply_text}")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Я умею выполнять следующие команды:\n/start - начать общение\n/help - помощь")


bot.infinity_polling()