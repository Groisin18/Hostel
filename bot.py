import asyncio
import logging
import config
import json
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

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


# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#    kb = [
#        [
#            KeyboardButton(text="Сможешь повторить это?"),
#            KeyboardButton(text="А это?")
#        ],
#    ]
#    keyboard = ReplyKeyboardMarkup(keyboard=kb)

#    await message.reply("Привет!\nЯ Эхобот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.", reply_markup=keyboard)



@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_data = load_user_data()
    user_id = str(message.from_user.id)

    if user_id in user_data:
        user_info = user_data[user_id]
        await message.answer(f"Привет, {user_info['name']}! Ваша заявка уже зарегистрирована.")
    else:
        kb = [
        [
           KeyboardButton(text="Зарегистрироваться"),
        ],
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Привет! Добро пожаловать в чат-бот нашего форума!", reply_markup=keyboard)

class Registration(StatesGroup):
    enter_name = State()
    enter_age = State()
    enter_city = State()
    enter_sex = State()

@dp.message(F.text == 'Зарегистрироваться')
async def registration_answer(message: Message, state: FSMContext):
    await message.answer(
        text='Пожалуйста, отправьте ваше ФИО в формате: Фамилия Имя Отчество',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.enter_name)

@dp.message(Registration.enter_name, F.text)
async def enter_name(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    name = str(message.text)
# Надо реализовать проверку данных
    user_data[user_id] = {"name": name}
    save_user_data(user_data) 
    await state.clear() 
    await message.answer(f"Замечательно! Сколько вам лет?")
    await state.set_state(Registration.enter_age)      

@dp.message(Registration.enter_age, F.text)
async def enter_age(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    age = int(message.text)
# Надо реализовать проверку данных
    user_data[user_id]["age"] = age
    await state.clear()
    await message.answer(f"Прекрасно! Укажите ваш город")
    await state.set_state(Registration.enter_city)    

@dp.message(Registration.enter_city, F.text)
async def enter_city(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    city = str(message.text)
# Надо реализовать проверку данных
    user_data[user_id]["city"] = city
    save_user_data(user_data)  
    await state.clear()
    kb = [
        [
           KeyboardButton(text="Мужской"),
           KeyboardButton(text="Женский"),
        ],
        ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Волшебно! Укажите, пожалуйста, ваш пол", reply_markup=keyboard)
    await state.set_state(Registration.enter_sex) 

@dp.message(Registration.enter_sex, F.text)
async def enter_sex(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    sex = str(message.text)
# Надо реализовать проверку данных
    user_data[user_id]["sex"] = sex
    save_user_data(user_data) 
    await state.clear() 
    await message.answer(
            f"Спасибо! Ваши данные зарегистрированы.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        ) 

    



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
