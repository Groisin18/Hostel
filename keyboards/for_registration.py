from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_male_fem_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мужской")
    kb.button(text="Женский")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)