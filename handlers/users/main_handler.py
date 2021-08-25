from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils import exceptions
from loader import dp, log

from keyboards.inline.user_info_keyboard import confirm_keyboard, item_cb, get_user_profile_keyboard, like_dislike_cb
from keyboards.dispatcher import dispatcher

from db.models import User, Rate
from handlers.users.utils import prepare_user_profile

from states.state_groups import ListProfiles


async def get_user_info(user_id: int, me: int) -> tuple[str, str]:
    user_info, photo_id, liked = await prepare_user_profile(user_id, me)
    return user_info, photo_id


async def pair_likes(user: User, me: User, m: types.Message):
    if await Rate.filter(rate_owner=user, target=me, type=True).exists():
        try:
            await m.bot.send_message(chat_id=me.user_id,
                                     text=f'This user ({user.full_name}) is also liked you.\n' +
                                          f'See user`s profile: @{user.username}')
            await m.bot.send_message(chat_id=user.user_id,
                                     text=f'You have been liked by: @{me.username} too. ({me.full_name})')
        except exceptions.ChatNotFound:
            log.info(f'{user.user_id} char was not found')
            await m.answer('You liked test user. So here may be a username of real user')


async def set_rate(m: types.Message, state: FSMContext, rate_type: bool) -> bool:
    me = await User.get(user_id=m.from_user.id)
    async with state.proxy() as data:
        index = int(data['current_user_index'])
        current_user = data['users_list'][index]
        user = await User.get(user_id=current_user)
        await Rate.get_or_create(rate_owner=me, target=user, type=rate_type)

        if index < len(data['users_list'])-1:
            index += 1
        else:
            return False
        user_info, photo_id = await get_user_info(data['users_list'][index], m.from_user.id)
        await m.delete()
        await m.bot.send_photo(
            chat_id=me.user_id, photo=photo_id, caption=user_info
        )
        data['current_user_index'] = index
        await pair_likes(user, me, m)
        return True


@dp.message_handler(Text(equals=['Remove dislikes']))
async def remove_dislikes(m: types.Message):
    user = await User.get(user_id=m.from_user.id)
    disliked = await Rate.filter(rate_owner=user, type=False)
    for u in disliked:
        await u.delete()
    await m.answer(f'{len(disliked)} dislikes was removed')


@dp.message_handler(Text(equals=['Display liked users']))
async def display_liked_users(m: types.Message, state: FSMContext):
    user = await User.get(user_id=m.from_user.id)
    liked_users = await user.get_liked_users()
    if not liked_users:
        await m.answer('You havent liked anyone yet')
        return
    await m.answer(f'Founded {len(liked_users)} users.\nDo you want to see their profiles?',
                   reply_markup=confirm_keyboard)
    await ListProfiles.confirm.set()
    await state.update_data(users_list=liked_users)


@dp.message_handler(Text(equals=['Display users']))
async def display_matched_users(m: types.Message, state: FSMContext):
    user = await User.get(user_id=m.from_user.id)
    matched_users = await user.find_matched_users()
    if not matched_users:
        nearest = round(await user.find_nearest(), 2)
        if nearest != 6371000:  # Earth radius
            await m.answer('There are no any users in this area.\n' +
                           f'Nearest person is <b>{nearest}</b> meters away from you')
        else:
            await m.answer('There are no any users in this area.')
        return
    log.info(f'Founded: {len(matched_users)} for {m.from_user.id}')
    keyboard, prev_level = await dispatcher('LEVEL_2_PROFILES')
    await m.answer(f'Founded {len(matched_users)} users',
                   reply_markup=keyboard)
    async with state.proxy() as data:
        data['users_list'] = matched_users
        data['prev_level'] = prev_level
        data['current_user_index'] = 0
        user_info, photo_id = await get_user_info(matched_users[0], m.from_user.id)
        message = await m.bot.send_photo(photo=photo_id, caption=user_info, chat_id=m.from_user.id)
        await ListProfiles.main.set()
        data['message_id'] = message.message_id


@dp.message_handler(Text(equals=['👍']), state=ListProfiles.main)
async def like(m: types.Message, state: FSMContext):
    if not await set_rate(m, state, True):
        await m.answer('There are no any users more')


@dp.message_handler(Text(equals=['👎']), state=ListProfiles.main)
async def like(m: types.Message, state: FSMContext):
    if not await set_rate(m, state, False):
        await m.answer('There are no any users more')
