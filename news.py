import feedparser
import logging

import requests
from bs4 import BeautifulSoup

FEED_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (compatible; ITNewsHubBot/1.0; +https://example.com/bot)",
    "Accept":
    "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.5",
}


def fetch_feed(url, source_name, headers=None, relaxed=False):
    request_headers = headers or {}
    try:
        response = requests.get(url,
                                timeout=FEED_TIMEOUT,
                                headers=request_headers)
        response.raise_for_status()
    except requests.RequestException as exc:
        logging.error(f"Ошибка {source_name}: {exc}")
        return None

    parse_kwargs = {}
    if relaxed:
        parse_kwargs["sanitize_html"] = True

    feed = feedparser.parse(response.content, **parse_kwargs)
    if feed.bozo and getattr(feed, "bozo_exception", None):
        logging.error(f"Ошибка {source_name}: {feed.bozo_exception}")
        return None

    return feed


def get_summary(text, max_len=300):
    if not text:
        return ""
    text = text.strip()
    return text[:max_len] + "..." if len(text) > max_len else text


# --- 3DNews ---
def get_3dnews_news():
    feed = fetch_feed("https://3dnews.ru/news/rss/",
                      "3DNews",
                      relaxed=True)
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            result.append({
                "title":
                entry.title,
                "summary":
                get_summary(entry.get("summary", "")),
                "link":
                entry.link,
                "image":
                entry.get("media_content")[0]["url"]
                if entry.get("media_content") else None
            })
        except Exception as exc:
            logging.error(f"Ошибка 3DNews (entry): {exc}")
    return result



# --- Habr ---
def get_habr_news():
    feed = fetch_feed("https://habr.com/ru/rss/all/all/?fl=ru", "Habr")
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            image = img["src"] if img else None
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": image
            })
        except Exception as exc:
            logging.error(f"Ошибка Habr (entry): {exc}")
    return result



# --- HackerNews ---
def get_hackernews():
    feed = fetch_feed("https://news.ycombinator.com/rss", "HackerNews")
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            result.append({
                "title": entry.title,
                "summary": "",  # у Hacker News нет текста новости
                "link": entry.link,
                "image": None
            })
        except Exception as exc:
            logging.error(f"Ошибка HackerNews (entry): {exc}")
    return result

# --- The Verge ---
def get_theverge_news():
    feed = fetch_feed("https://www.theverge.com/rss/index.xml",
                      "The Verge",
                      headers=DEFAULT_HEADERS)
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        except Exception as exc:
            logging.error(f"Ошибка The Verge (entry): {exc}")
    return result



# --- TechCrunch ---
def get_techcrunch_news():
    feed = fetch_feed("https://feeds.feedburner.com/TechCrunch/",
                      "TechCrunch")
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        except Exception as exc:
            logging.error(f"Ошибка TechCrunch (entry): {exc}")
    return result


# --- Slashdot ---
def get_slashdot_news():
    feed = fetch_feed(
        "http://rss.slashdot.org/Slashdot/slashdotMain", "Slashdot")
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        except Exception as exc:
            logging.error(f"Ошибка Slashdot (entry): {exc}")
    return result


# --- StopGame ---
def get_stopgame_news():␊
    try:␊
        url = "https://stopgame.ru/news"
        resp = requests.get(url, timeout=FEED_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser") 

        news_items = soup.find_all("article", class_="_card_1lcny_4")
        results = []

        for item in news_items[:5]:
            try:
                # заголовок и ссылка
                title_tag = item.find("a", class_="_title_1lcny_24")
                title = title_tag.get_text(strip=True) if title_tag else None
                link = "https://stopgame.ru" + title_tag[
                    "href"] if title_tag and title_tag.get("href") else None

                # изображение
                img_tag = item.find("img")
                image = img_tag["src"] if img_tag and img_tag.get("src") else None

                # автор
                author_tag = item.find("span",
                                       class_="_user-info__name_tf5im_1181")
                author = author_tag.get_text(strip=True) if author_tag else None

                # дата публикации
                date_tag = item.find("section", class_="_date_1lcny_225")
                date = date_tag.get_text(strip=True) if date_tag else None

                # summary
                summary_tag = item.find("p")
                summary = summary_tag.get_text(
                    " ", strip=True) if summary_tag else title

                if title and link:
                    results.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "image": image,
                        "author": author,
                        "date": date
                    })
            except Exception as exc:
                logging.error(f"Ошибка StopGame (entry): {exc}")

        return results

    except Exception as e:
        logging.error(f"Ошибка StopGame: {e}")
        return []


# --- Igromania ---
def get_igromania_news():
    feed = fetch_feed("https://www.igromania.ru/rss/news.xml", "Igromania")
    if not feed:
        return []

    result = []
    for entry in feed.entries[:5]:
        try:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        except Exception as exc:
            logging.error(f"Ошибка Igromania (entry): {exc}")
    return result




