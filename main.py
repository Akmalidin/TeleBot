from config import token, smtp_email, smtp_password
from aiogram import Bot, Dispatcher, executor, types
from logging import basicConfig, INFO
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os, smtplib, random
from aiogram.dispatcher import FSMContext
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)
start_buttons = [
    types.InlineKeyboardButton('Идентификация', callback_data='identification'),
]
start_btn = types.InlineKeyboardMarkup().add(*start_buttons)
password = ''.join(random.choices('0123456789', k=6))
def send_mail(title, message, to_email):
    sender = smtp_email
    password = smtp_password
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    try:
        server.login(sender, password)
        server.sendmail(sender, to_email, title, message)
        return '200 ok'
    except Exception as error:
        return f'Error: {error}'


@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f'Привет! {message.from_user.full_name}', reply_markup=start_btn)

class IdentificationState(StatesGroup):
    email = State()

class Password(StatesGroup):
    password = State()
@dp.callback_query_handler(lambda call: call.data == 'identification')
async def identification(message:types.Message):
    await bot.send_message(message.from_user.id, 'Введите вашу почту')
    await IdentificationState.email.set()

@dp.message_handler(state=IdentificationState.email)
async def email(message:types.Message, state: FSMContext):
    send_mail(password, password, message.text)
    await message.answer(f'Пароль отправлена на почту {message.text}\nВведите пароль для подтверждения')
    await Password.password.set()
    
@dp.message_handler(state=Password.password)
async def passwords(message:types.Message, state: FSMContext):
    if message.text == password:
        await message.answer('Идентификация прошла успешно\nМожете использовать нашего бота')
    else:
        await message.answer('Пароль неверен\nПовторите попытку используя команду /start')
    await state.finish()

executor.start_polling(dp, skip_updates=True)
