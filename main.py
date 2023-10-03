from aiogram import Bot, Dispatcher, types, executor
from config import token
from logging import basicConfig, INFO

bot = Bot(token=token)
dp = Dispatcher(bot)
basicConfig(level=INFO)

vision_keyboard = [
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Объекты"),
    types.KeyboardButton("Контакты"),
]
objects_finished = [
    types.KeyboardButton("Завершенные объекты"),
    types.KeyboardButton("Строящиеся объекты"),
    types.KeyboardButton("Назад")
]
objects_btn = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*objects_finished)
vision_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*vision_keyboard)
@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}\nДобро пожаловать в VisionGroup\nЧто вы хотели узнать?", reply_markup=vision_button)
@dp.message_handler(text="start")
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}\nДобро пожаловать в VisionGroup\nЧто вы хотели узнать?", reply_markup=vision_button)
@dp.message_handler(text="О нас")
async def about(message:types.Message):
    await message.answer("""
                                                    <b><i>СТРОИТЕЛЬНАЯ КОМПАНИЯ</i></b>

                            <b>ОсОО «Визион Групп»</b>
Мы - развивающаяся компания, которая предлагает своим клиентам широкий выбор квартир в объектах расположенных во всех наиболее привлекательных районах городов Ош и Джалал-Абад. \nУ нас максимально выгодные условия, гибкий (индивидуальный) подход при реализации жилой и коммерческой недвижимости. Мы занимаем лидирующие позиции по количеству объектов по югу Кыргызстана. \nНаша миссия: Мы обеспечиваем население удобным жильем для всей семьи, проявляя лояльность и индивидуальный подход и обеспечивая высокий уровень обслуживания.\n\n Мы обеспечиваем бизнес подходящим коммерческим помещением, используя современные решения и опыт профессионалов своего дела.
                         """,parse_mode="HTML")

@dp.message_handler(text="Объекты")
async def objects(message:types.Message):
    await message.answer("Выберите из меню объекты которые хотите увидеть!", reply_markup=objects_btn)

@dp.message_handler(text="Завершенные объекты")
async def finished_objects(message:types.Message):
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_1260,h_708/https://vg-stroy.com/wp-content/uploads/2022/01/dji_0392-scaled-1.jpeg")
    await message.answer("ЖК «Малина-Лайф»\n г.Ош, ул Монуева 19")
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_873,h_1280/https://vg-stroy.com/wp-content/uploads/2022/01/2022-02-09-14.22.41.jpg")
    await message.answer("ЖК «Малина-Лайф»\n г.Ош, ул Монуева 19")
@dp.message_handler(text="Строящиеся объекты")
async def notfinished_objects(message:types.Message):
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_1260,h_708/https://vg-stroy.com/wp-content/uploads/2022/01/dji_0392-scaled-1.jpeg")
    await message.answer("ЖК «Малина-Лайф»\n г.Ош, ул Монуева 19")
    await message.answer_photo("https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_873,h_1280/https://vg-stroy.com/wp-content/uploads/2022/01/2022-02-09-14.22.41.jpg")
    await message.answer("ЖК «Малина-Лайф»\n г.Ош, ул Монуева 19")
@dp.message_handler(text="Назад")
async def prev(message:types.Message):
    await start(message)

@dp.message_handler(text="Контакты")
async def contacts(message:types.Message):
    await message.answer("Телефонные номера: \n+996 709 620088\n+996 772 620088\n+996 550 620088")

@dp.message_handler()
async def text(message:types.Message):
    await message.answer("Я вас не понял введите команду /start")
executor.start_polling(dp)