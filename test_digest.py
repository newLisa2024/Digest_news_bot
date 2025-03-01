import asyncio
import logging
from aiogram.client.bot import Bot, DefaultBotProperties
import config
from modules.digest import generate_weekly_digest
from modules.subscriber_db import list_subscribers


async def send_weekly_digest(bot: Bot):
    """
    Функция для тестовой рассылки дайджеста всем подписчикам.
    """
    # Генерируем дайджест (это текст, который будет передан в OpenAI и сформирован итоговый дайджест)
    digest = generate_weekly_digest()

    # Получаем список подписчиков
    subscribers = list_subscribers()
    if not subscribers:
        print("Нет подписчиков для рассылки.")
        return

    # Отправляем дайджест каждому подписчику
    for sub in subscribers:
        user_id = sub.get("user_id")
        try:
            await bot.send_message(chat_id=user_id, text=digest)
            print(f"Дайджест отправлен пользователю {user_id}")
        except Exception as e:
            print(f"Ошибка отправки дайджеста пользователю {user_id}: {e}")


async def main():
    # Создаем экземпляр бота
    bot = Bot(
        token=config.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # Вызываем функцию тестовой рассылки
    await send_weekly_digest(bot)

    # Закрываем сессию бота
    await bot.session.close()


if __name__ == "__main__":
    # Запускаем основной цикл
    asyncio.run(main())

