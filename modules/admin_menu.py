import logging
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
import config
from modules.subscriber_db import list_subscribers, remove_subscriber


async def cmd_admin_menu(message: Message):
    try:
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Нет доступа.")
            return

        text = (
            "🔧 <b>Административное меню</b> 🔧\n\n"
            "📋 Список подписчиков — кнопка ниже\n"
            "❌ Удалить подписчика — запросит ID\n"
            "✉️ Отправить сообщение — запросит данные\n"
            "📢 Массовая рассылка — введите текст"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 Список подписчиков", callback_data="admin_subscribers")],
            [InlineKeyboardButton(text="❌ Удалить подписчика", callback_data="admin_remove")],
            [InlineKeyboardButton(text="✉️ Отправить сообщение", callback_data="admin_send")],
            [InlineKeyboardButton(text="📢 Массовая рассылка", callback_data="admin_broadcast")]
        ])

        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Ошибка в cmd_admin_menu: {e}")
        await message.answer("Ошибка при открытии меню.")


async def callback_admin_subscribers(call: CallbackQuery):
    try:
        if call.from_user.id not in config.ADMIN_IDS:
            await call.answer("Нет доступа", show_alert=True)
            return

        subscribers = list_subscribers()
        if not subscribers:
            await call.message.answer("Список подписчиков пуст.")
            return

        response = "📋 <b>Список подписчиков:</b>\n"
        for sub in subscribers:
            response += f"🆔 ID: {sub.get('user_id', '---')}, 👤 Username: @{sub.get('username', '---')}\n"

        await call.message.edit_text(response, parse_mode="HTML")
        await call.answer()
    except TelegramBadRequest:
        await call.message.answer("Слишком длинный список. Используйте /subscribers.")
    except Exception as e:
        logging.error(f"Ошибка в callback_admin_subscribers: {e}")
        await call.message.answer("Ошибка при получении списка.")


async def callback_admin_remove(call: CallbackQuery):
    try:
        if call.from_user.id not in config.ADMIN_IDS:
            await call.answer("Нет доступа", show_alert=True)
            return

        await call.message.answer("Введите ID подписчика для удаления (например: <code>/remove 123456</code>):",
                                  parse_mode="HTML")
        await call.answer()
    except Exception as e:
        logging.error(f"Ошибка в callback_admin_remove: {e}")
        await call.message.answer("Ошибка при обработке запроса.")


async def callback_admin_send(call: CallbackQuery):
    try:
        if call.from_user.id not in config.ADMIN_IDS:
            await call.answer("Нет доступа", show_alert=True)
            return

        await call.message.answer("Введите команду в формате:\n<code>/send 123456 Ваш текст</code>", parse_mode="HTML")
        await call.answer()
    except Exception as e:
        logging.error(f"Ошибка в callback_admin_send: {e}")
        await call.message.answer("Ошибка при обработке запроса.")


async def callback_admin_broadcast(call: CallbackQuery):
    try:
        if call.from_user.id not in config.ADMIN_IDS:
            await call.answer("Нет доступа", show_alert=True)
            return

        await call.message.answer("Введите текст для рассылки:\n<code>/broadcast Ваш текст</code>", parse_mode="HTML")
        await call.answer()
    except Exception as e:
        logging.error(f"Ошибка в callback_admin_broadcast: {e}")
        await call.message.answer("Ошибка при обработке запроса.")

