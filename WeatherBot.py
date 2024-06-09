import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv('API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your Weather bot!\nSend me a city name to get the weather forecast.")

def get_weather_data(city):
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'uk'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        if data['cod'] != 200:
            return None

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_message = (f"Погода в місті {city}:\n"
                           f"Опис: {weather_desc}\n"
                           f"Температура: {temp}°C\n"
                           f"Відчувається як: {feels_like}°C\n"
                           f"Вологість: {humidity}%\n"
                           f"Швидкість вітру: {wind_speed} м/с")

        return weather_message
    except Exception as e:
        print(e)
        return None

@dp.message_handler()
async def handle_message(message: types.Message):
    city = message.text.strip()
    weather_info = get_weather_data(city)
    if weather_info:
        await message.reply(weather_info)
    else:
        await message.reply("Не вдалося отримати дані про погоду. Спробуйте ще раз.")

if name == 'main':
    executor.start_polling(dp, skip_updates=True)import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv('API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your Weather bot!\nSend me a city name to get the weather forecast.")

def get_weather_data(city):
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'uk'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        if data['cod'] != 200:
            return None

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_message = (f"Погода в місті {city}:\n"
                           f"Опис: {weather_desc}\n"
                           f"Температура: {temp}°C\n"
                           f"Відчувається як: {feels_like}°C\n"
                           f"Вологість: {humidity}%\n"
                           f"Швидкість вітру: {wind_speed} м/с")

        return weather_message
    except Exception as e:
        print(e)
        return None

@dp.message_handler()
async def handle_message(message: types.Message):
    city = message.text.strip()
    weather_info = get_weather_data(city)
    if weather_info:
        await message.reply(weather_info)
    else:
        await message.reply("Не вдалося отримати дані про погоду. Спробуйте ще раз.")

if name == 'main':
    executor.start_polling(dp, skip_updates=True)