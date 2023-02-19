from aiogram import Bot, Dispatcher, executor, types

from settings import BOT_TOKEN

import logging

import ebay.parse
import aliexpress.parse

import os

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

platform = None

search_method = {
    "Ebay": ebay.parse.main,
    "Aliexpress": aliexpress.parse.main
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = """
    Hi, boss. Let's start work!

    Set searching platform: /platform
    For full info: /help
    """
    await message.reply(text)


@dp.message_handler(commands=['help'])
async def send_help_text(message: types.Message):
    text = """
    So, you wanna know how to make deal with me?

    Here my manual:

    Before you start you have to set searching platform. Type command /platform
    After you done with this you can send requests.
    
    To send me request typle "search:" before actual request text.
    Example: search: rtx 3060.

    I will send you file with information and links.
    That's it. Simple, right?

    PS: Because of platforms security I can't surf for info time by time.
    Don't forget I am not human.
    I will say if I can not work with site.

    My code: https://github.com/Dasifue/parsing_bot
    """
    await message.reply(text)


@dp.message_handler(commands=['platform'])
async def choose_platform(message: types.Message):
    message_text = "Choose platform for searching:"
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    ebay = types.InlineKeyboardButton("Ebay", callback_data="Ebay")
    aliexpress = types.InlineKeyboardButton("Aliexpress", callback_data="Aliexpress")
    markup.add(ebay, aliexpress)
    await bot.send_message(chat_id=message.from_user.id, text=message_text, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in ("Ebay", "Aliexpress"))
async def set_platform(call_bacK_query: types.CallbackQuery):
    global platform
    platform = call_bacK_query.data
    text = f"""
    Good! The platform has been changed. 
    Your actual searching platform is *{platform}*
    """
    await bot.send_message(chat_id=call_bacK_query.message.chat['id'], text=text)


@dp.message_handler(lambda message: message.text.startswith("search:"))
async def send_file(message: types.Message):
    print(message)
    request = message["text"].lstrip("search:").strip(" ")
    if platform:
        try:
            search_method[platform](request)
        except AttributeError:
            await message.reply("Oops! Something went wrong. Try again leter. Sometimes it happens.")
        else:
            await bot.send_document(message.from_user.id, document=open(request, "rb"), caption="Here! I found something")
            os.remove(request)
    else:
        text = """
        Before to search set the platform: /platform
        For instruction send me - /help
        """
        await message.reply(text)


@dp.message_handler(content_types=types.ContentType.ANY)
async def reply(message: types.Message):
    message_text = f"{message.text} 😝"
    await message.reply(message_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)