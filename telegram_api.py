import telebot
from telebot import types

from settings import settings
from weather import weather, WeatherError

conf = settings()

bot = telebot.TeleBot(conf.token)


@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    fact = weather(message)
    try:
        bot.send_message(
            message.chat.id,
            text=f'Сейчас температура в Невинномысске {fact.temp}°,'
                 f'ощущается как {fact.feels_like}°. '
                 f'Погода на улице {fact.verbose_condition}. '
                 f'Скорость ветра {fact.wind_speed} М/С. '
                 f'Влажность воздуха {fact.humidity} %.'
        )
    except WeatherError as e:
        bot.send_message(message.chat.id, str(e))

    # @bot.message_handler(commands=['prognoz'])
    # def get_weather_forecast(message):
    #     forecast = weather_forecast(message)
    #     a = weather_forecast_data(message)
    #     try:
    #         bot.send_message(
    #             message.chat.id,
    #             text=f'Сейчас температура в Невинномысске {a.date}°,'
    #                  f'температура {forecast.temp_min}°. '
    #                  f'Погода на улице {forecast.temp_max}. '
    #                  f'Погода на улице {forecast.temp_avg}. '
    #         )
    #     except WeatherError as e:
    #         bot.send_message(message.chat.id, str(e))

@bot.message_handler(commands=['kolomna'])
def get_weather_in_kolomna(message):
    fact = weather(message)
    try:
        bot.send_message(
            message.chat.id,

            text=f'Сейчас температура в Коломне {fact.temp}°, '
                 f'ощущается как {fact.feels_like}°. '
                 f'Погода на улице {fact.verbose_condition}. '
                 f'Скорость ветра {fact.wind_speed} М/С. '
                 f'Влажность воздуха {fact.humidity} %.'
        )
    except WeatherError as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Скачать видео с вконтакте', url=conf.vk)
    item2 = types.InlineKeyboardButton('Скачать видео с YouTube', url=conf.youtube)

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'vk':
            bot.send_message(call.message.chat.id, conf.vk)
        elif call.data == 'youtube':
            bot.send_message(call.message.chat.id, conf.youtube)


@bot.message_handler(content_types=['text'])
def message_return(message):
    if message.text.lower() == 'вк':
        bot.send_message(message.chat.id, conf.vk)
    if message.text.lower() == 'ютуб':
        bot.send_message(message.chat.id, conf.youtube)


def start_bot():
    bot.infinity_polling()
