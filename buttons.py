from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ===============================================================

start = ReplyKeyboardMarkup(resize_keyboard=True,
                            row_width=2)

start_buttons = KeyboardButton('/start')


start.add(start_buttons)

# ===============================================================

start_test = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
    ).add(
KeyboardButton('/start')
)

# ===============================================================

start_test_1 = ReplyKeyboardMarkup(
    resize_keyboard=True,
    row_width=2
    )

start_test_1.add(
    KeyboardButton('/start')
)

# ===============================================================

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Cancel'))
submit_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(KeyboardButton('Yes'), KeyboardButton('No'))