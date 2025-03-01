import asyncio
import logging
from aiogram import Dispatcher, F, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import config
from modules.subscriber_db import add_subscriber, remove_subscriber
from modules.admin_menu import (
    cmd_admin_menu,
    callback_admin_subscribers,
    callback_admin_remove,
    callback_admin_send,
    callback_admin_broadcast
)
from modules.scheduler import start_scheduler  # NEW

logging.basicConfig(level=logging.INFO)

async def cmd_start(message: Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        add_subscriber(user_id, username)
        await message.answer("Добро пожаловать! Вы успешно подписались на рассылку новостей.")
    except Exception as e:
        logging.error(f"Ошибка в cmd_start: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке команды.")

async def cmd_stop(message: Message):
    try:
        user_id = message.from_user.id
        remove_subscriber(user_id)
        await message.answer("Вы успешно отписались от рассылки.")
    except Exception as e:
        logging.error(f"Ошибка в cmd_stop: {e}")
        await message.answer("⚠️ Произошла ошибка при отписке.")

async def main():
    try:
        bot = Bot(
            token=config.TELEGRAM_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        dp = Dispatcher()

        # Регистрация обработчиков
        dp.message.register(cmd_start, Command(commands=["start"]))
        dp.message.register(cmd_stop, Command(commands=["stop"]))
        dp.message.register(cmd_admin_menu, Command(commands=["admin_menu"]))

        # Колбэки админ-меню
        dp.callback_query.register(callback_admin_subscribers, F.data == "admin_subscribers")
        dp.callback_query.register(callback_admin_remove, F.data == "admin_remove")
        dp.callback_query.register(callback_admin_send, F.data == "admin_send")
        dp.callback_query.register(callback_admin_broadcast, F.data == "admin_broadcast")

        # Запуск планировщика рассылки # NEW
        start_scheduler(bot)

        await dp.start_polling(bot)
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())





