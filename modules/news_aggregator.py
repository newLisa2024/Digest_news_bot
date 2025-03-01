# modules/news_aggregator.py
import feedparser
import logging
from datetime import datetime, timedelta
import config
from dateutil import parser as date_parser
from modules import rbc_parser  # импортируем модуль для парсинга РБК

# Добавляем новый источник RSS от TAdviser
RSS_FEEDS = [
    "https://infra.tadviser.ru/xml/tadviser.xml",  # новый источник
]

def fetch_feed(url: str):
    try:
        data = feedparser.parse(url)
        if data.bozo:
            logging.warning("Ошибка парсинга RSS из %s: %s", url, data.bozo_exception)
        return data.entries
    except Exception as e:
        logging.error("Ошибка при получении данных из %s: %s", url, e)
        return []

def get_rss_news() -> list:
    all_news = []
    now = datetime.now()
    period = timedelta(days=config.NEWS_PERIOD_DAYS)
    for url in RSS_FEEDS:
        entries = fetch_feed(url)
        for entry in entries:
            published_str = entry.get("published", "")
            if published_str:
                try:
                    published_date = date_parser.parse(published_str)
                    # Приводим дату к offset-naive
                    published_date = published_date.replace(tzinfo=None)
                except Exception as e:
                    logging.warning("Не удалось разобрать дату публикации: %s", published_str)
                    continue
                if now - published_date > period:
                    continue

            news_item = {
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "summary": entry.get("summary", "").strip(),
            }
            all_news.append(news_item)
    return all_news

def get_all_news() -> list:
    """
    Собирает новости как из RSS-ленты, так и с помощью HTML-парсинга (например, РБК).
    """
    rss_news = get_rss_news()
    rbc_news = rbc_parser.get_rbc_news()  # функция из нового модуля для РБК
    all_news = rss_news + rbc_news
    # Дополнительно можно отсортировать новости по дате, если добавите поле "pub_date"
    return all_news

