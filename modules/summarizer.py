# modules/summarizer.py
import logging
import openai
import config

# Устанавливаем API-ключ OpenAI
openai.api_key = config.OPENAI_API_KEY


def generate_summary(news_text: str, custom_prompt: str = None) -> str:
    """
    Генерирует краткое содержание для заданного текста новостей с использованием
    актуального OpenAI API (версия 1.0.0+).

    :param news_text: Текст новостей для суммаризации.
    :param custom_prompt: (Опционально) Дополнительный промпт, задающий стиль и формат саммари.
    :return: Сгенерированное саммари или сообщение об ошибке.
    """
    if custom_prompt is None:
        custom_prompt = "Сделай краткое, но ёмкое саммари следующих новостей на русском языке:"

    # Формируем полный текст промпта
    prompt = f"{custom_prompt}\n\n{news_text}"

    try:
        # Новый вызов для openai>=1.0.0
        response = openai.chat.completions.create(
            model="gpt-4",  # Или "gpt-4", если у вас есть доступ
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты – опытный программист и специалист по AI, освещающий "
                        "новости об искусственном интеллекте."
                    )
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.5,
        )

        # Извлекаем текст ответа из объекта response
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        logging.error("Ошибка генерации саммари: %s", e)
        return "Ошибка генерации саммари."



