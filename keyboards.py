from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="📍 Choose Places")],
        [KeyboardButton(text="📌 Location")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

def create_places_keyboard(places):
    builder = InlineKeyboardBuilder()
    for place in places:
        builder.button(
            text=place.name,
            callback_data=f"place_{place.id}"
        )
    builder.adjust(1)
    return builder.as_markup()
