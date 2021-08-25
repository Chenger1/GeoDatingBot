from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from emoji import emojize


level_1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Display users'),
    KeyboardButton('Display liked users'),
    KeyboardButton('Display my likers')
).add(
    KeyboardButton('Edit info'),
    KeyboardButton('Remove dislikes')
).add(
    KeyboardButton('Add custom user(For test only)'),
    KeyboardButton('Request admin status(For test only)')
)


level_2_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Broadcast mailing'),
    KeyboardButton('Statistic')
).add(
    KeyboardButton('Logs'),
    KeyboardButton('Requests to admin')
).add(
    KeyboardButton('Back')
)


level_2_profiles = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(emojize(':thumbs_down:')),
    KeyboardButton(emojize(':thumbs_up:'))
).add(
    KeyboardButton('Back')
)
