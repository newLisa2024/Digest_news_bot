from modules.news_aggregator import get_all_news
from modules.summarizer import generate_summary
from aiogram import Bot
from modules.subscriber_db import list_subscribers
import logging


async def send_weekly_digest(bot: Bot):  # NEW
    try:
        # Генерируем дайджест
        digest_text = generate_weekly_digest()

        # Получаем подписчиков
        subscribers = list_subscribers()

        # Отправляем всем
        for user in subscribers:
            try:
                await bot.send_message(
                    chat_id=user["user_id"],
                    text=digest_text,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
            except Exception as e:
                logging.error(f"Ошибка отправки для {user['user_id']}: {e}")

    except Exception as e:
        logging.error(f"Ошибка генерации/рассылки: {e}")


def generate_weekly_digest() -> str:  # UPDATED
    news_list = get_all_news()

    if not news_list:
        return "📭 На этой неделе новостей по ИИ не найдено."

    # Формируем текст для промпта (ваш оригинальный код сохранен)
    combined_text = "Новости за неделю:\n\n"
    for idx, news_item in enumerate(news_list, start=1):
        combined_text += f"{idx}. {news_item.get('title', '')}\nСсылка: {news_item.get('link', '')}\n\n"

    # Ваш кастомный промпт без изменений
    custom_prompt = (
        "Ты – опытный программист и специалист по AI... [ваш оригинальный текст]"
    )

    # Генерация саммари
    digest = generate_summary(combined_text, custom_prompt)

    # Форматирование результата
    return (
        "📰 <b>Еженедельный дайджест AI-новостей</b>\n\n"
        f"{digest}\n\n"
        "➖➖➖➖➖➖➖➖➖\n"
        "📌 Подписаться: /start\n"
        "📌 Отписаться: /stop"
    )


