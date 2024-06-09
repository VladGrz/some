import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

API_TOKEN = os.getenv('API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

class WeatherStates(StatesGroup):
    waiting_for_city = State()

@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message, state: FSMContext):
    await message.answer("Hi!\nI'm your Weather bot!\nSend me a city name to get the weather forecast.")
    await state.set_state(WeatherStates.waiting_for_city)

async def get_weather_data(city):
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

@router.message()
async def handle_message(message: Message, state: FSMContext):
    city = message.text.strip()
    weather_info = await get_weather_data(city)
    if weather_info:
        await message.answer(weather_info)
    else:
        await message.answer("Не вдалося отримати дані про погоду. Спробуйте ще раз.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())