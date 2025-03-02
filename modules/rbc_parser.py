import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import config
import re

# Расширенный список ключевых слов для фильтрации новостей
KEYWORDS = [
    "искусственный интеллект", "ai", "machine learning", "машинное обучение",
    "deep learning", "глубокое обучение", "нейросеть", "нейронная сеть", "gpt",
    "llm", "большая языковая модель", "chatgpt", "openai", "nlp", "обработка естественного языка",
    "computer vision", "компьютерное зрение", "data science", "big data", "робототехника",
    "ии-разработка", "ai-разработка", "it-разработка", "ит-разработка", "генеративный ии",
    "автоматизация", "аналитика данных", "предсказательная аналитика", "ии-модели",
    "когнитивные технологии", "цифровой двойник", "алгоритмы машинного обучения"
]

def filter_news_by_keywords(news_list, keywords):
    """
    Фильтрует новости, оставляя только те, в которых встречаются заданные ключевые слова.
    Проверка проводится по заголовку и краткому описанию (summary).
    """
    filtered = []
    for news in news_list:
        text = (news.get("title", "") + " " + news.get("summary", "")).lower()
        if any(keyword.lower() in text for keyword in keywords):
            filtered.append(news)
    return filtered

def get_rbc_news() -> list:
    """
    Парсит новости с главной страницы РБК (https://www.rbc.ru/),
    фильтруя их по дате и ключевым словам из KEYWORDS.
    """
    url = "https://www.rbc.ru/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error("Ошибка получения главной страницы РБК: %s", e)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    news_list = []
    now = datetime.now()

    try:
        # Пример: ищем блоки статей по селектору
        # На главной РБК часто встречаются div с классом "main__feed", в нём - "main__feed__item"
        articles = soup.find_all('div', class_=re.compile(r"main__feed__item"))
    except Exception as e:
        logging.error("Ошибка парсинга HTML главной страницы РБК: %s", e)
        return []

    for article in articles:
        try:
            # Ищем ссылку
            link_tag = article.find('a', href=True)
            if not link_tag:
                continue

            link = link_tag['href'].strip()
            title = link_tag.get_text(strip=True)

            # Пытаемся найти дату (не всегда есть). Если нет - приравняем к текущему времени.
            # Иногда дата бывает в <span> или <time> с классами вроде "main__feed__date" и т.д.
            # В качестве упрощения берём "now".
            pub_date = now

            # Фильтрация по дате: если (now - pub_date) > NEWS_PERIOD_DAYS, пропускаем
            if now - pub_date > timedelta(days=config.NEWS_PERIOD_DAYS):
                continue

            # Вытаскиваем краткое описание, если есть
            # Для примера посмотрим, есть ли <span class="main__feed__author">, либо другие блоки
            # Если ничего нет, оставляем пустую строку
            summary = ""
            desc_span = article.find('span', class_=re.compile(r"item__text|main__feed__author"))
            if desc_span:
                summary = desc_span.get_text(strip=True)

            news_item = {
                "title": title,
                "link": link,
                "summary": summary,
                "pub_date": pub_date,
            }
            news_list.append(news_item)
        except Exception as e:
            logging.warning("Ошибка обработки статьи на главной РБК: %s", e)
            continue

    # Применяем фильтрацию по ключевым словам
    filtered_news = filter_news_by_keywords(news_list, KEYWORDS)
    return filtered_news


