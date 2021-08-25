from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callbacks import item_cb, like_dislike_cb

gender_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Man', callback_data=item_cb.new(action='choose_gender',
                                                          value=1,
                                                          second_value=False)),
    InlineKeyboardButton('Woman', callback_data=item_cb.new(action='choose_gender',
                                                            value=0,
                                                            second_value=False))
)

confirm_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Confirm', callback_data=item_cb.new(action='confirm',
                                                              value=1,
                                                              second_value=False)),
    InlineKeyboardButton('Cancel', callback_data=item_cb.new(action='confirm',
                                                             value=0,
                                                             second_value=False))
)


async def get_request_to_admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton('Approve', callback_data=item_cb.new(action='request_to_admin',
                                                                  value=user_id,
                                                                  second_value=1)),
        InlineKeyboardButton('Disapprove', callback_data=item_cb.new(action='request_to_admin',
                                                                     value=user_id,
                                                                     second_value=0))
    )
