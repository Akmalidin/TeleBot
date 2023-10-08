from aiogram import Bot, Dispatcher, types, executor
from config import token
from logging import basicConfig, INFO

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

buttons = [
    types.KeyboardButton("BackEnd"),
    types.KeyboardButton("FrontEnd"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("UX/UI"),
]

button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

@dp.message_handler(commands=['start', 'Start', 'старт', 'Старт'])
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}\nДобро пожаловать в IT курсы. Выберите команду из меню!", reply_markup=button)

@dp.message_handler(text='BackEnd')
async def backend(message:types.Message):
    await message.reply("""Backend — это внутренняя часть сайта и сервера и т.д
                            Стоимость 10000 сом в месяц
                        Обучение: 5 месяц""")

@dp.message_handler(text='FrontEnd')
async def frontend(message:types.Message):
    await message.reply("""FrontEnd — это Наружная часть сайта и т.д
                            Стоимость 10000 сом в месяц
                        Обучение: 5 месяц""")


@dp.message_handler(text='Android')
async def android(message:types.Message):
    await message.reply("""Android — это разработка приложений для телефонов с базой Android и т.д
                            Стоимость 10000 сом в месяц
                        Обучение: 5 месяц""")


@dp.message_handler(text='IOS')
async def ios(message:types.Message):
    await message.reply("""IOS — это  это разработка приложений для телефонов Iphone и т.д
                            Стоимость 10000 сом в месяц
                        Обучение: 5 месяц""")


@dp.message_handler(text='UX/UI')
async def uxui(message:types.Message):
    await message.reply("""UX/UI — это разработка дизайна для сайта, телефонов и т.д
                            Стоимость 10000 сом в месяц
                        Обучение: 5 месяц""")


executor.start_polling(dp)
    
