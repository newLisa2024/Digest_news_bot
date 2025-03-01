import logging
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError
import config
from modules.subscriber_db import list_subscribers, remove_subscriber


async def cmd_list_subscribers(message: Message):
    try:
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Нет доступа.")
            return

        subscribers = list_subscribers()
        if not subscribers:
            await message.answer("Список подписчиков пуст.")
            return

        response = "📋 <b>Список подписчиков:</b>\n"
        for sub in subscribers:
            response += f"🆔 ID: {sub.get('user_id', '---')}, 👤 Username: @{sub.get('username', '---')}\n"

        await message.answer(response, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Ошибка в cmd_list_subscribers: {e}")
        await message.answer("Ошибка при получении списка.")


async def cmd_remove_subscriber(message: Message):
    try:
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Нет доступа.")
            return

        parts = message.text.split()
        if len(parts) != 2:
            await message.answer("Используйте: /remove <user_id>")
            return

        user_id = int(parts[1])
        remove_subscriber(user_id)
        await message.answer(f"✅ Подписчик с ID {user_id} удалён.")
    except ValueError:
        await message.answer("❌ Некорректный user_id.")
    except Exception as e:
        logging.error(f"Ошибка в cmd_remove_subscriber: {e}")
        await message.answer("❌ Ошибка при удалении.")


async def cmd_send_message(message: Message):
    try:
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Нет доступа.")
            return

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("Используйте: /send <user_id> <текст>")
            return

        user_id = int(parts[1])
        text = parts[2]
        await message.bot.send_message(chat_id=user_id, text=text)
        await message.answer(f"✅ Сообщение отправлено пользователю {user_id}.")
    except ValueError:
        await message.answer("❌ Некорректный user_id.")
    except TelegramAPIError as e:
        logging.error(f"Ошибка Telegram API: {e}")
        await message.answer("❌ Пользователь заблокировал бота или не существует.")
    except Exception as e:
        logging.error(f"Ошибка в cmd_send_message: {e}")
        await message.answer("❌ Ошибка отправки.")


async def cmd_broadcast(message: Message):
    try:
        if message.from_user.id not in config.ADMIN_IDS:
            await message.answer("Нет доступа.")
            return

        text = message.text.split(maxsplit=1)[1]
        subscribers = list_subscribers()
        if not subscribers:
            await message.answer("Список подписчиков пуст.")
            return

        success, failed = 0, 0
        for sub in subscribers:
            try:
                await message.bot.send_message(chat_id=sub["user_id"], text=text)
                success += 1
            except Exception:
                failed += 1

        await message.answer(f"📢 Рассылка завершена.\nУспешно: {success}\nНеудачно: {failed}")
    except IndexError:
        await message.answer("Используйте: /broadcast <текст>")
    except Exception as e:
        logging.error(f"Ошибка в cmd_broadcast: {e}")
        await message.answer("❌ Ошибка рассылки.")