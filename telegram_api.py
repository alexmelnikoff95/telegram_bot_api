import telebot
from telebot import types

from settings import token, vk, youtube


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет')

    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Скачать видео с вконтакте', callback_data='vk')
        item2 = types.InlineKeyboardButton('Скачать видео с YouTube', callback_data='yotube')

        markup.add(item1, item2)

        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.message:
            if call.data == 'vk':
                bot.send_message(call.message.chat.id, vk)
            elif call.data == 'yotube':
                bot.send_message(call.message.chat.id, youtube)

    @bot.message_handler(content_types='text')
    def message_return(message):
        if message.text.lower() == 'вк':
            bot.send_message(message.chat.id, vk)
        if message.text.lower() == 'ютуб':
            bot.send_message(message.chat.id, youtube)

    bot.infinity_polling()


if __name__ == '__main__':
    telegram_bot(token)
