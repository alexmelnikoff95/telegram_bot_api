import requests
from pydantic import BaseModel

from settings import settings

CONDITION_MAP = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом'
}


class WeatherError(Exception):
    pass


# class WeatherForecast(BaseModel):
#     # date: date
#     temp_min: float
#     temp_max: float
#     temp_avg: float
# class WeatherForecastDate(BaseModel):
#     date: date


class Weather(BaseModel):
    wind_speed: float | int
    temp: float
    condition: str
    feels_like: float
    humidity: int | float

    @property
    def verbose_condition(self) -> str:
        return CONDITION_MAP.get(self.condition, self.condition)


def weather(message) -> Weather:
    if message.text.lower() == '/get_weather':
        url = 'https://api.weather.yandex.ru/v2/informers?lat=44.600513&lon=41.962367&lang=ru_RU'
    else:
        url = 'https://api.weather.yandex.ru/v2/informers?lat=55.0794&lon=38.7783&lang=ru_RU'

    headers = {'X-Yandex-API-Key': settings().key}
    request_server = requests.get(url=url, headers=headers)

    if not request_server.ok:
        raise WeatherError('Ошибка API')

    data = request_server.json()
    fact = data["fact"]

    return Weather.parse_obj(fact)


# def weather_forecast(message) -> WeatherForecast:
#     if message.text.lower() == '/prognoz':
#         url = 'https://api.weather.yandex.ru/v2/informers?lat=44.600513&lon=41.962367&lang=ru_RU'
#     else:
#         url = 'https://api.weather.yandex.ru/v2/informers?lat=55.0794&lon=38.7783&lang=ru_RU'
#
#     headers = {'X-Yandex-API-Key': settings().key}
#     request_server = requests.get(url=url, headers=headers)
#
#     if not request_server.ok:
#         raise WeatherError('Ошибка API')
#
#     data = request_server.json()
#     forecast = data['forecast']['parts'][0]
#
#     return WeatherForecast.parse_obj(forecast)


# def weather_forecast_data(message) -> WeatherForecastDate:
#     if message.text.lower() == '/prognoz':
#         url = 'https://api.weather.yandex.ru/v2/informers?lat=44.600513&lon=41.962367&lang=ru_RU'
#     else:
#         url = 'https://api.weather.yandex.ru/v2/informers?lat=55.0794&lon=38.7783&lang=ru_RU'
#
#     headers = {'X-Yandex-API-Key': settings().key}
#     request_server = requests.get(url=url, headers=headers)
#
#     if not request_server.ok:
#         raise WeatherError('Ошибка API')
#
#     data = request_server.json()
#     forecast = data['forecast']
#
#     return WeatherForecastDate.parse_obj(forecast)