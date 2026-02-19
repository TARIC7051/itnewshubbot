# sources/loaders/rss_loader.py
import feedparser
import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


class RSSLoader:
    def __init__(self, url, max_items=5):
        """
        url: RSS-ссылка на источник
        max_items: сколько новостей брать за раз
        """
        self.url = url
        self.max_items = max_items

    def load(self):
        """
        Возвращает список новостей в формате:
        {"title": ..., "summary": ..., "link": ..., "image": ...}
        """
        try:
            resp = requests.get(self.url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            if not feed or not feed.entries:
                return []

            result = []
            for entry in feed.entries[:self.max_items]:
                summary_html = entry.get("summary", "")
                if not summary_html and entry.get("content"):
                    summary_html = entry.get("content")[0].get("value", "")
                soup = BeautifulSoup(summary_html, "html.parser")
                img_tag = soup.find("img")
                result.append({
                    "title": entry.title,
                    "summary": soup.get_text(strip=True)[:300],
                    "link": entry.link,
                    "image": img_tag["src"] if img_tag else None
                })
            return result
        except Exception as e:
            logging.error(f"Ошибка загрузки RSS {self.url}: {e}")
            return []
