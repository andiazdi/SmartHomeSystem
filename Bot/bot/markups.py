from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

GET_DEVISES = ReplyKeyboardMarkup().add(KeyboardButton("Устройства"))


def devices(connected_devices, user_id):
    markup = InlineKeyboardMarkup()
    for i in connected_devices:
        markup.add(InlineKeyboardButton(i[1], callback_data=i[1]))
    return markup
