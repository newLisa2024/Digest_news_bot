from modules.news_aggregator import get_all_news
from modules.summarizer import generate_summary
from aiogram import Bot
from modules.subscriber_db import list_subscribers
import logging


async def send_weekly_digest(bot: Bot):
    """
    Асинхронная функция, отправляющая еженедельный дайджест всем подписчикам.
    """
    try:
        # Генерируем дайджест
        digest_text = generate_weekly_digest()

        # Получаем подписчиков
        subscribers = list_subscribers()

        # Отправляем дайджест каждому подписчику
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


def generate_weekly_digest() -> str:
    """
    Формирует итоговый текст дайджеста на основе новостей и вызывает генерацию саммари через OpenAI.
    """
    news_list = get_all_news()

    if not news_list:
        return "📭 На этой неделе новостей по ИИ не найдено."

    # Формируем текст для промпта
    combined_text = "Новости за неделю:\n\n"
    for idx, news_item in enumerate(news_list, start=1):
        combined_text += (
            f"{idx}. {news_item.get('title', '')}\n"
            f"Ссылка: {news_item.get('link', '')}\n\n"
        )

    # Заменяем placeholder «[ваш оригинальный текст]» на готовый текст промпта
    custom_prompt = (
        "Ты – опытный программист и специалист по AI, освещающий новости об искусственном интеллекте "
        "для Telegram-канала. Ты смотришь на технологии с лёгким юмором и уверен, что AI – это всего лишь инструмент, "
        "без сценариев восстания машин, потому что у него нет собственных желаний. AI – мощный, но, как и любой инструмент, "
        "его эффективность зависит от того, кто и как его использует. Твоя задача – делать краткое, но ёмкое саммари статьи "
        "на русском языке без потери сути, сохраняя баланс между информативностью и лёгкой ироничностью. Заголовок должен "
        "быть жирным текстом, но без специальных символов, просто текст заголовка с начальной заглавной буквы, основанный "
        "на «Титул», но с живостью и интригой. Текст 250–300 слов, с чёткой структурой, без лишней воды. Обязательно укажи "
        "автора и источник (URL-адрес). Если статья подаёт AI в слишком драматичном или паническом тоне, ты мягко "
        "иронизируешь над этим, объясняя, что он не более опасен, чем молоток в умелых руках. Если речь о достижениях AI, "
        "подчёркивай, что технологии – это возможности, но за ними всегда стоит человеческий труд. Пиши живо, с изюминкой, "
        "чтобы читателю хотелось делиться твоим текстом!"
    )

    # Генерация саммари через OpenAI
    digest = generate_summary(combined_text, custom_prompt)

    # Форматирование итогового текста
    return (
        "📰 <b>Еженедельный дайджест AI-новостей</b>\n\n"
        f"{digest}\n\n"
        "➖➖➖➖➖➖➖➖➖\n"
        "📌 Подписаться: /start\n"
        "📌 Отписаться: /stop"
    )



