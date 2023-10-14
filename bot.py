from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from logging import basicConfig, INFO
import os, requests, sqlite3

conn = sqlite3.connect('tiktok.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, last_name TEXT, user_name TEXT)""")

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_name = message.from_user.full_name
    cursor.execute("INSERT INTO users (name, last_name, user_name) VALUES (?, ?, ?)", (name, last_name, user_name))
    conn.commit()
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler()
async def get_message_url(message:types.Message):
    if 'tiktok.com' in message.text:
        # await message.answer(f"{message.text}")
        input_url = message.text.split("?")
        get_id_video = input_url[0].split("/")[-1]
        # print(get_id_video)
        video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={get_id_video}').json()
        # await message.answer(type(video_api))
        video_url = video_api.get("aweme_list")[0].get("video").get("play_addr").get("url_list")[0]
        id_user = video_api.get("aweme_list")[0].get("author").get("uid")
        
        
        
        comment_count_video = video_api.get('aweme_list')[0].get('statistics').get('comment_count')
        like_video = video_api.get('aweme_list')[0].get('statistics').get('digg_count')
        play_video = video_api.get('aweme_list')[0].get('statistics').get('play_count')
        desc_video = video_api.get("aweme_list")[0].get('desc')
        await message.answer(f'ID пользователя: {id_user}\nКоличество просмотров: {play_video}\nЛайкнули: {like_video} раз\nКоментарии: {comment_count_video}\nОписание видео: {desc_video}')
        if video_url:
            await message.answer("Скачиваем видео...")
            title_video = video_api.get("aweme_list")[0].get("desc")
            await message.answer(title_video)
            try:
                with open(f'video/{title_video}.mp4', 'wb') as video_file:
                    video_file.write(requests.get(video_url).content)
                with open(f'video/{title_video}.mp4', 'rb') as send_video_file:
                    await message.answer_video(send_video_file)
                
                await message.answer(f"Видео {title_video} успешно скачан XD")
                os.remove(f'video/{title_video}.mp4')
            except Exception as error:
                await message.answer(f"Error: {error}")
    else:
        await message.answer("Неправильная ссылка на видео TikTok")

executor.start_polling(dp, skip_updates=True)





# from aiogram import Bot, Dispatcher, types, executor
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from dotenv import load_dotenv
# from logging import basicConfig, INFO
# import os, requests

# load_dotenv('.env')

# bot = Bot(os.environ.get('token'))
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# basicConfig(level=INFO)

# @dp.message_handler(commands='start')
# async def start(message:types.Message):
#     await message.answer(f"Привет {message.from_user.full_name}")

# @dp.message_handler()
# async def get_message_url(message:types.Message):
#     if 'tiktok.com' in message.text:
#         await message.answer(f"{message.text}")
#         input_url = message.text.split("?")
#         get_id_video = input_url[0].split("/")[5]
#         print(get_id_video)
#         video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={get_id_video}').json()
#         print(type(video_api))
#         video_url = video_api.get("aweme_list")[0].get("video").get("play_addr").get("url_list")[0]
#         print(video_url)
#         if video_url:
#             await message.answer("Скачиваем видео...")
#             title_video = video_api.get("aweme_list")[0].get("desc")
#             print(title_video)
#             try:
#                 with open(f'video/{title_video}.mp4', 'wb') as video_file:
#                     video_file.write(requests.get(video_url).content)
#                 await message.answer(f"Видео {title_video} успешно скачан XD")
#                 with open(f'video/{title_video}.mp4', 'rb') as send_video_file:
#                     await message.answer_video(send_video_file)
#             except Exception as error:
#                 await message.answer(f"Error: {error}")
#     else:
#         await message.answer("Неправильная ссылка на видео TikTok")

# executor.start_polling(dp, skip_updates=True)