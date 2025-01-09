import asyncio
import logging
import config
import json
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

class Checking:

    def __init__(self, *args):
        data = list(args)
        self.fio = data[0]
        self.age = data[1]

    def check_data(self):
        def check_fio():
            pass

        def check_age():
            pass
        check_fio()
        check_age()

        return None




# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # ParseMode.MARKDOWN_V2
    )
)

# Диспетчер
dp = Dispatcher(storage=MemoryStorage())

# Инициализация файла с данными пользователей

USER_DATA_FILE = "user_data.json"

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w", encoding='UTF-8') as f:
        json.dump({}, f)

def load_user_data():
    with open(USER_DATA_FILE, "r", encoding='UTF-8') as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_data = load_user_data()
    user_id = str(message.from_user.id)

    if user_id in user_data:
        user_info = user_data[user_id]
        await message.answer(
            f"Привет, {user_info['name']}! Ваша заявка уже зарегистрирована."
        )
    else:
        await message.answer(
            "Привет! Пожалуйста, отправьте свои ФИО и возраст в формате:\nФИО, возраст"
        )

@dp.message(F.text)
async def handle_user_data(message: Message):
    user_data = load_user_data()
    user_id = str(message.from_user.id)

    if user_id in user_data:
        await message.answer("Вы уже зарегистрированы. Если хотите изменить данные, обратитесь к администратору.")
        return

    try:
        name, age = map(str.strip, message.text.split(","))
        age = int(age)
        checker = Checking(name, age)
        checker.check_data()
# Надо реализовать проверку данных

        # Сохранение данных
        user_data[user_id] = {"name": name, "age": age}
        save_user_data(user_data)

        await message.answer(
            f"Спасибо! Ваши данные зарегистрированы:\n<b>Имя:</b> {name}\n<b>Возраст:</b> {age}",
            parse_mode=ParseMode.HTML
        )
    except ValueError:
        await message.answer("Пожалуйста, отправьте данные в правильном формате: ФИО, возраст")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
