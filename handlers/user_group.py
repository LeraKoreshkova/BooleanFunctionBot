from string import punctuation

from aiogram import F, Router, types

user_group_router = Router()

restricted_words = {"петух", "овца", "баран"}


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(message.text.lower().split()):
        await message.answer(f"{message.from_user.first_name}, соблюдайте порядок в чате!")
        await message.delete()