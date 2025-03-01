import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import config
import re

# Расширенный список ключевых слов для фильтрации новостей РБК
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
    Проверка проводится по заголовку и краткому описанию.
    """
    filtered = []
    for news in news_list:
        text = (news.get("title", "") + " " + news.get("summary", "")).lower()
        if any(keyword.lower() in text for keyword in keywords):
            filtered.append(news)
    return filtered


def get_rbc_news() -> list:
    """
    Парсит новости с раздела «Нейросети» на РБК Тренды, фильтруя их по дате и ключевым словам.
    """
    url = "https://trends.rbc.ru/trends/tag/neural_network"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error("Ошибка получения страницы РБК: %s", e)
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    news_list = []
    now = datetime.now()

    # Парсим список новостей на странице раздела "Нейросети"
    try:
        # На странице раздела 'Нейросети' каждая новость представлена ссылкой с 24-символьным ID
        articles = soup.find_all('article')
    except Exception as e:
        logging.error("Ошибка парсинга HTML РБК: %s", e)
        return []

    for article in articles:
        try:
            # Ищем ссылку на новость по шаблону URL с 24-символьным ID
            link_tag = article.find('a', href=re.compile(r"/trends/[^/]+/[0-9a-f]{24}"))
            if not link_tag:
                continue
            title = link_tag.get_text(strip=True)
            link = link_tag['href']
            if link.startswith('/'):
                link = "https://trends.rbc.ru" + link
            # Получаем дату публикации, если указана
            date_str = ""
            time_tag = article.find('time')
            if time_tag:
                date_str = time_tag.get('datetime') or time_tag.get_text(strip=True)
            pub_date = date_parser.parse(date_str) if date_str else now
            # Фильтрация по дате: новости за последние NEWS_PERIOD_DAYS
            if now - pub_date > timedelta(days=config.NEWS_PERIOD_DAYS):
                continue
            # Извлекаем краткое описание, если доступно
            summary = ""
            summary_elem = article.find(
                lambda tag: tag.name == 'div' and tag.get('class') and any('desc' in cls for cls in tag.get('class')))
            if summary_elem:
                summary = summary_elem.get_text(strip=True)
            news_item = {
                "title": title,
                "link": link,
                "summary": summary,
                "pub_date": pub_date,
            }
            news_list.append(news_item)
        except Exception as e:
            logging.warning("Ошибка обработки статьи РБК: %s", e)
            continue

    # Применяем фильтрацию по ключевым словам
    filtered_news = filter_news_by_keywords(news_list, KEYWORDS)
    return filtered_news

