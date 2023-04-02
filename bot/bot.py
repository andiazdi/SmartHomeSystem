import sys

import markups
from aiogram import Bot, Dispatcher, executor, types

sys.path.append("../")
import asyncio

import config
from db.db import Devices
from mqtt_client import MqttClient

username = "TelegramBot"
db = Devices()
mqtt_client = MqttClient(username, db)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # if message.chat.id not in config.admin_chat_id:
    #     return
    await message.answer(
        "Привет, посмотрим, что у нас дома?", reply_markup=markups.GET_DEVISES
    )


@dp.message_handler(content_types=["text"])
async def text(message: types.Message):
    # if message.chat.id not in config.admin_chat_id:
    #     return

    ans = await mqtt_client.get_all_connected_devices(message.from_user.id)
    await message.answer("Выберите устройство", reply_markup=markups.devices(ans, message.from_user.id))


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    ans = await mqtt_client.get_data_from_device(callback_query.data, callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, ans["payload"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
