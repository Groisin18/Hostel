from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.database import load_user_data, save_user_data
from keyboards.for_registration import get_male_fem_kb


class Registration(StatesGroup):
    enter_name = State()
    enter_age = State()
    enter_city = State()
    enter_sex = State()

router = Router()

@router.message(F.text == 'Зарегистрироваться')
async def registration_answer(message: Message, state: FSMContext):
    await message.answer(
        text='Пожалуйста, отправьте ваше ФИО в формате: Фамилия Имя Отчество',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Registration.enter_name)

@router.message(Registration.enter_name, F.text)
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

@router.message(Registration.enter_age, F.text)
async def enter_age(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    age = int(message.text)
# Надо реализовать проверку данных
    user_data[user_id]["age"] = age
    save_user_data(user_data) 
    await state.clear()
    await message.answer(f"Прекрасно! Укажите ваш город")
    await state.set_state(Registration.enter_city)    

@router.message(Registration.enter_city, F.text)
async def enter_city(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    city = str(message.text)
# Надо реализовать проверку данных
    user_data[user_id]["city"] = city
    save_user_data(user_data)  
    await state.clear()
    await message.answer(f"Волшебно! Укажите, пожалуйста, ваш пол", reply_markup=get_male_fem_kb())
    await state.set_state(Registration.enter_sex) 

@router.message(Registration.enter_sex, F.text)
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