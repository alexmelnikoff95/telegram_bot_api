import requests
import json

import telebot
from telebot import types

from settings import vk, youtube, key


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['get_weather', 'pogoda'])
    def get_weather(message):
        url = 'https://api.weather.yandex.ru/v2/informers??lat=44.600513&lon=41.962367&lang=ru_RU'
        headers = {'X-Yandex-API-Key': key}

        r = requests.get(url=url, headers=headers)

        if r.status_code == 200:
            data = json.loads(r.text)
            fact = data["fact"]
            bot.send_message(message.chat.id,
                             text=f'Сейчас температура в Невинномысске {fact["temp"]}°, ощущается как {fact["feels_like"]}°. Погода на улице {fact["condition"]}')
        else:
            bot.send_message(message.chat.id, 'Ошибка в работе API')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет')

    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Скачать видео с вконтакте', callback_data='vk')
        item2 = types.InlineKeyboardButton('Скачать видео с YouTube', callback_data='youtube')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.message:
            if call.data == 'vk':
                bot.send_message(call.message.chat.id, vk)
            elif call.data == 'youtube':
                bot.send_message(call.message.chat.id, youtube)

    @bot.message_handler(content_types='text')
    def message_return(message):
        if message.text.lower() == 'вк':
            bot.send_message(message.chat.id, vk)
        if message.text.lower() == 'ютуб':
            bot.send_message(message.chat.id, youtube)

    bot.infinity_polling()
