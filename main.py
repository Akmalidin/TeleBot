from aiogram import Dispatcher, executor, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from config import token
from logging import basicConfig, INFO
from datetime import datetime
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id_user INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        phonenumber INTEGER
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(id_user INTEGER, title TEXT, address_destination TEXT, date_time_order TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS address (id_user, address_latitude, address_longitude)""")
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

start_keyboard = [
    types.KeyboardButton('Отправить номер', request_contact=True),
    types.KeyboardButton('Отправить локацию', request_location=True),
    types.KeyboardButton('Заказать еду')
    ]
start_keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

# Обрабатываем команду start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply(f"Привет! {message.from_user.full_name} Нажмите кнопку ниже, чтобы заказать еду.", reply_markup=start_keyboards)

# Обрабатываем номера телефона, полученного от пользователя
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def on_contact(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    phone_number = message.contact.phone_number
    id_user = message.from_user.id
    cursor.execute('SELECT id_user FROM users WHERE id_user = ?', (id_user,))
    regis_user = cursor.fetchone()
    if regis_user:
        await message.reply("Вы уже зарегистрированы в нашей базе данных.")
    else:
        cursor.execute('INSERT INTO users (id_user, first_name, last_name, username, phonenumber) VALUES (?, ?, ?, ?, ?)', (id_user, first_name, last_name, username, phone_number))
        conn.commit()
        await message.reply(f"Спасибо за предоставленный номер телефона: {phone_number}", reply_markup=start_keyboards)

# Команда для запроса локации
@dp.message_handler(text='Отправить локацию')
async def request_location(message: types.Message):
    await message.reply("Пожалуйста, отправьте вашу локацию, нажав на кнопку 'Отправить локацию' ниже.", reply_markup=start_keyboards)

# Обрабатываем локацию
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def on_location(message: types.Message):
    id_user = message.from_user.id
    address_latitude = message.location.latitude
    address_longitude = message.location.longitude
    cursor.execute('''INSERT INTO address (id_user, address_latitude, address_longitude) VALUES (?, ?, ?)''', (id_user, address_latitude, address_longitude))
    conn.commit()
    await message.reply("Ваша локация успешно сохранена в базе данных.", reply_markup=start_keyboards)

# Добавляем новое состояние для ожидания названия блюда
class OrderState(StatesGroup):
    title = State()
    delivery_address = State()

# ...

# Обработчик команды "Заказать еду"
@dp.message_handler(text='Заказать еду')
async def request_order_info(message: types.Message):
    markup = types.ReplyKeyboardRemove()
    await message.reply("Чтобы заказать еду, введите название блюда:", reply_markup=markup)
    await OrderState.title.set()
# Обработка названия блюда
@dp.message_handler(state=OrderState.title)
async def process_food_name(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    title = message.text
    markup = types.ReplyKeyboardRemove()
    message = await message.reply(f"Вы заказали {title}. Теперь введите адрес доставки:", reply_markup=markup)
    async with state.proxy() as data:
        data['title'] = title
    await OrderState.delivery_address.set()

# Обработка адреса доставки и запись заказа в базу данных
@dp.message_handler(state=OrderState.delivery_address)
async def process_delivery_address(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    async with state.proxy() as data:
        title = data['title']
    delivery_address = message.text
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO orders (id_user, title, address_destination, date_time_order) VALUES (?, ?, ?, ?) ''', (id_user, title, delivery_address, order_time))
    conn.commit()
    await message.reply(f"Ваш заказ: {title} будет доставлен по адресу: {delivery_address}.")
    await state.finish()


executor.start_polling(dp)