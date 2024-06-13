from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задача 1"),
            KeyboardButton(text="Задача 2"),
            KeyboardButton(text="Задача 3")
        ],
        [
            KeyboardButton(text="Задача 4"),
            KeyboardButton(text="Задача 5"),
            KeyboardButton(text="Задача 6")
        ],
        [
            KeyboardButton(text="Задача 7"),
            KeyboardButton(text="Задача 8"),
            KeyboardButton(text="Задача 9")
        ],
        [
            KeyboardButton(text="Задача 10"),
            KeyboardButton(text="Задача 11"),
            KeyboardButton(text="Задача 12")
        ]
    ], resize_keyboard=True#, one_time_keyboard=True#, input_field_placeholder="Выбери задачу ↓"
)


four_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="конъюнкция"),
            KeyboardButton(text="дизъюнкция"),
            KeyboardButton(text="сложение по mod 2"),
            KeyboardButton(text="штрих Шеффера")
        ],
        [
            KeyboardButton(text="стрелка Пирса"),
            KeyboardButton(text="импликация"),
            KeyboardButton(text="эквивалентность"),
            KeyboardButton(text="коимпликация")
        ],
        [
            KeyboardButton(text="обратная импликация"),
            KeyboardButton(text="обратная коимпликация"),
            KeyboardButton(text="константа 0"),
            KeyboardButton(text="функция равна второму аргументу")
        ],
        [
            KeyboardButton(text="функция равна первому аргументу"),
            KeyboardButton(text="отрицание второго аргумента"),
            KeyboardButton(text="отрицание первого аргумента"),
            KeyboardButton(text="константа 1")
        ],
    ], resize_keyboard=True
)


five_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Существенная")
        ],
        [
            KeyboardButton(text="Фиктивная")
        ]
    ], resize_keyboard=True
)


ten_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Принадлежит")
        ],
        [
            KeyboardButton(text="Не принадлежит")
        ]
    ], resize_keyboard=True
)


eleven_full_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Полный")
        ],
        [
            KeyboardButton(text="Неполный")
        ]
    ], resize_keyboard=True
)