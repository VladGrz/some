import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from prometheus_client import start_http_server, Summary, Counter, Gauge
import time

API_TOKEN = os.getenv('API_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

class WeatherStates(StatesGroup):
    waiting_for_city = State()

# Prometheus metrics
REQUEST_TIME = Summary('weather_request_processing_seconds', 'Time spent processing weather requests')
BOT_MESSAGES_RECEIVED = Counter('weather_bot_messages_received_total', 'Total number of messages received by the bot')
BOT_MESSAGES_SENT = Counter('weather_bot_messages_sent_total', 'Total number of messages sent by the bot')
API_ERRORS = Counter('weather_api_errors_total', 'Total number of weather API errors')
STATE_TRANSITIONS = Counter('weather_state_transitions_total', 'Total number of state transitions in the FSM')
CPU_USAGE = Gauge('weather_bot_cpu_usage', 'CPU usage of the Weather Bot')
MEMORY_USAGE = Gauge('weather_bot_memory_usage', 'Memory usage of the Weather Bot')

# Function to measure CPU and Memory usage
def measure_resource_usage():
    import psutil
    process = psutil.Process(os.getpid())
    CPU_USAGE.set(process.cpu_percent())
    MEMORY_USAGE.set(process.memory_info().rss)

@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message, state: FSMContext):
    BOT_MESSAGES_RECEIVED.inc()
    STATE_TRANSITIONS.inc()
    await message.answer("Hi!\nI'm your Weather bot!\nSend me a city name to get the weather forecast.")
    await state.set_state(WeatherStates.waiting_for_city)
    BOT_MESSAGES_SENT.inc()

@REQUEST_TIME.time()
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
            API_ERRORS.inc()
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
        API_ERRORS.inc()
        print(e)
        return None

@router.message()
async def handle_message(message: Message, state: FSMContext):
    BOT_MESSAGES_RECEIVED.inc()
    city = message.text.strip()
    weather_info = await get_weather_data(city)
    if weather_info:
        await message.answer(weather_info)
        BOT_MESSAGES_SENT.inc()
    else:
        await message.answer("Не вдалося отримати дані про погоду. Спробуйте ще раз.")
        BOT_MESSAGES_SENT.inc()
    await state.clear()
    STATE_TRANSITIONS.inc()

async def main():
    # Start the Prometheus server to expose metrics
    start_http_server(8001)
    while True:
        measure_resource_usage()
        await asyncio.sleep(5)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
