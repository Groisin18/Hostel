from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_common import get_registration
from database.database import load_user_data


router = Router()

@router.message(Command("start"))
async def send_welcome(message: Message, state: FSMContext):
    user_data = load_user_data()
    user_id = str(message.from_user.id)
    await state.clear()

    if user_id in user_data:
        user_info = user_data[user_id]
        await message.answer(f"Добро пожаловать, {user_info['name']}! Ваша заявка уже зарегистрирована.")
    else:
        await message.answer("Привет! Добро пожаловать в чат-бот нашего форума!", reply_markup=get_registration())


# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )