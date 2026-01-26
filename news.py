# news.py

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def get_ixbt_news(limit=5):
    url = "https://www.ixbt.com/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    news_items = []

    # на ixbt новости обычно в блоках с классом 'news'
    articles = soup.select("div.item")[:limit]  # берем первые limit новостей
    for a in articles:
        title_tag = a.select_one("a")  # ссылка на новость
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.ixbt.com" + link
            news_items.append(f"{title}\n{link}")

    return news_items


def get_3dnews_news(limit=5):
    url = "https://3dnews.ru/news"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    news_items = []

    # новости на 3dnews находятся в блоках с классом 'news-item'
    articles = soup.select("div.news-item")[:limit]
    for a in articles:
        title_tag = a.select_one("a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://3dnews.ru" + link
            news_items.append(f"{title}\n{link}")

    return news_items


def get_all_news(limit=5):
    ixbt = get_ixbt_news(limit)
    d3news = get_3dnews_news(limit)
    return ixbt + d3news
