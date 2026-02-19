# sources/loaders/html_loader.py
import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


class HTMLLoader:
    def __init__(self, url, article_selector, title_selector="a", summary_selector=None, max_items=5, base_url=None):
        """
        url: ссылка на страницу с новостями
        article_selector: CSS-селектор для блоков статей
        title_selector: CSS-селектор внутри статьи для заголовка (по умолчанию "a")
        summary_selector: CSS-селектор внутри статьи для краткого описания (по умолчанию None)
        max_items: сколько новостей брать за раз
        base_url: если ссылки относительные, указать базовый URL сайта
        """
        self.url = url
        self.article_selector = article_selector
        self.title_selector = title_selector
        self.summary_selector = summary_selector
        self.max_items = max_items
        self.base_url = base_url

    def load(self):
        try:
            resp = requests.get(self.url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = soup.select(self.article_selector)
            result = []

            for item in articles[:self.max_items]:
                title_tag = item.select_one(self.title_selector)
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href")
                if self.base_url and link and link.startswith("/"):
                    link = self.base_url + link

                summary = ""
                if self.summary_selector:
                    summary_tag = item.select_one(self.summary_selector)
                    summary = summary_tag.get_text(strip=True) if summary_tag else ""

                result.append({
                    "title": title,
                    "summary": summary[:300],
                    "link": link,
                    "image": None  # Можно добавить позже, если нужен
                })
            return result
        except Exception as e:
            logging.error(f"Ошибка HTML загрузки {self.url}: {e}")
            return []
