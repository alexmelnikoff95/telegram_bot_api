import telebot
from telebot import types

from settings import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hellow')

    @bot.message_handler(commands=['button'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Кнопка')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    @bot.message_handler(content_types='text')
    def message_return(message):
        if message.text.lower() == 'кнопка':
            bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=x-VB3b4pKcU&t=44s')

    bot.infinity_polling()


if __name__ == '__main__':
    telegram_bot(token)
