from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


x = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="something", callback_data="something")
        ]
    ]
)