import asyncio
import logging
from aiogram import Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
import config
from modules.subscriber_db import add_subscriber, remove_subscriber
from modules.admin_menu import (
    cmd_admin_menu,
    callback_admin_subscribers,
    callback_admin_remove,
    callback_admin_send,
    callback_admin_broadcast
)
from modules.scheduler import start_scheduler

# Дополнительная клавиатура для админа (кнопка с командой)
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/admin_menu")]],
    resize_keyboard=True
)

async def cmd_start(message: Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        add_subscriber(user_id, username)
        if user_id in config.ADMIN_IDS:
            # Если это админ, показываем кнопку "/admin_menu"
            await message.answer(
                "Добро пожаловать! Вы успешно подписались на рассылку новостей.\n\n"
                "Получите бонус за подписку — набор из 1444 промптов для бизнеса, маркетинга и жизни: https://uni-prompt.com/\n\n"
                "Так как вы администратор, используйте кнопку ниже или введите /admin_menu для входа в админ-панель.",
                reply_markup=admin_keyboard
            )
        else:
            # Обычный пользователь
            await message.answer("Добро пожаловать! Вы успешно подписались на рассылку новостей.\n\n"
            "Получите бонус за подписку — набор из 1444 промптов для бизнеса, маркетинга и жизни: https://uni-prompt.com/.\n\n")
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
        bot = Bot(token=config.TELEGRAM_TOKEN)
        dp = Dispatcher()

        dp.message.register(cmd_start, Command(commands=["start"]))
        dp.message.register(cmd_stop, Command(commands=["stop"]))
        dp.message.register(cmd_admin_menu, Command(commands=["admin_menu"]))

        # Регистрируем колбэки для админ-меню
        dp.callback_query.register(callback_admin_subscribers, F.data == "admin_subscribers")
        dp.callback_query.register(callback_admin_remove, F.data == "admin_remove")
        dp.callback_query.register(callback_admin_send, F.data == "admin_send")
        dp.callback_query.register(callback_admin_broadcast, F.data == "admin_broadcast")

        # Запускаем планировщик рассылки
        start_scheduler(bot)

        await dp.start_polling(bot)
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())







