from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_registration() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Зарегистрироваться")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
