# test_news.py
from modules.news_aggregator import get_all_news

if __name__ == "__main__":
    news = get_all_news()
    for item in news:
        print(f"Заголовок: {item.get('title')}")
        print(f"Ссылка: {item.get('link')}")
        print(f"Краткое содержание: {item.get('summary')}")
        print("-" * 80)
