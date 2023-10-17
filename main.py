from aiogram import Bot, Dispatcher, executor, types
from logging import basicConfig, INFO
from bs4 import BeautifulSoup
from config import token
import requests, os, lxml
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
basicConfig(level=INFO)
    
url = 'https://www.nbkr.kg/'
responce = requests.get(url=url)

soup = BeautifulSoup(responce.text, 'lxml')
all_links = soup.find_all('td', class_="exrate")
usd_txt = all_links[0]
eur_txt = all_links[2]
rub_txt = all_links[4]
kzt_txt = all_links[6]
usd_txt = usd_txt.text.replace(',', '.')
usd_float = float(usd_txt)

rub_txt = rub_txt.text.replace(',', '.')
rub_float = float(rub_txt)

eur_txt = eur_txt.text.replace(',', '.')
eur_float = float(eur_txt)

kzt_txt = kzt_txt.text.replace(',', '.')
kzt_float = float(kzt_txt)
# a = [usd_txt.text, rub_txt.text]
# print(usd_txt.text, rub_txt.text)
# print(a)

btn = [
    types.KeyboardButton('USD/KGS'),
    types.KeyboardButton('RUB/KGS'),
    types.KeyboardButton('EUR/KGS'),
    types.KeyboardButton('KZT/KGS')
]
kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*btn)
@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Привет {message.from_user.full_name}\nВыберите валюту для обмена!\nВся информация взята из сайта https://nbkr.kg', reply_markup=kb)

class Usd(StatesGroup):
    usd = State()
    rub = State()
    eur = State()
    kzt = State()
@dp.message_handler(text='USD/KGS')
async def usd(message:types.Message) :
    await message.answer(f'Вы быбрали USD/KGS\nСумма...')
    await Usd.usd.set()

@dp.message_handler(state=Usd.usd)
async def usd_valuta(message:types.Message, state: FSMContext):
    answer = float(message.text)
    a = answer * usd_float
    await message.answer(f'Вы получите {a} сом')
    await state.finish()

@dp.message_handler(text='RUB/KGS')
async def usd(message:types.Message) :        
    await message.answer(f'Вы быбрали RUB/KGS\nСумма...')
    await Usd.rub.set()

@dp.message_handler(state=Usd.rub)
async def usd_valuta(message:types.Message, state: FSMContext):
    answer = float(message.text)
    a = answer * rub_float
    await message.answer(f'Вы получите {a} сом')
    await state.finish()
    
@dp.message_handler(text='EUR/KGS')
async def usd(message:types.Message) :
        await message.answer(f'Вы быбрали EUR/KGS\nСумма...')
        await Usd.eur.set()

@dp.message_handler(state=Usd.eur)
async def usd_valuta(message:types.Message, state: FSMContext):
    answer = float(message.text)
    a = answer * eur_float
    await message.answer(f'Вы получите {a} сом')
    await state.finish()

@dp.message_handler(text='KZT/KGS')
async def usd(message:types.Message) :
    await message.answer(f'Вы быбрали KZT/KGS\nСумма...')
    await Usd.kzt.set()

@dp.message_handler(state=Usd.kzt)
async def usd_valuta(message:types.Message, state: FSMContext):
    answer = float(message.text)
    a = answer * kzt_float
    await message.answer(f'Вы получите {a} сом')
    await state.finish()

executor.start_polling(dp)