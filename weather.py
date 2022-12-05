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


class Weather(BaseModel):
    wind_speed: float
    temp: float
    condition: str
    feels_like: float

    @property
    def verbose_condition(self) -> str:
        return CONDITION_MAP.get(self.condition, self.condition)


def weather() -> Weather:
    url = 'https://api.weather.yandex.ru/v2/informers?lat=44.600513&lon=41.962367&lang=ru_RU'
    headers = {'X-Yandex-API-Key': settings().key}
    r = requests.get(url=url, headers=headers)

    if not r.ok:
        raise WeatherError('Ошибка API')

    data = r.json()
    fact = data["fact"]

    return Weather.parse_obj(fact)
