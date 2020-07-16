import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from config import TELEGRAM_BOT_API_KEY
from dialog_system.main import get_answer
from dialog_system.config import MESSAGES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_API_KEY)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я диалоговый бот. Я отвечу на твои вопросы по определенной теме. Задавай их!")


@dp.message_handler(commands='help')
async def send_help(message: types.Message):
    await message.reply("Я тебе обязательно помогу, но как-нибудь в другой раз.")


@dp.message_handler()
async def send_answer(message: types.Message):
    answer = get_answer(message.text)
    text = ""
    if answer["success"]:
        text = answer["answers"][random.randint(0, len(answer["answers"]) - 1)]
    else:
        text = MESSAGES["failed"][random.randint(0, len(MESSAGES["failed"]) - 1)]
    await message.reply(text=text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
