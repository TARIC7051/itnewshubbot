import feedparser
import requests
from bs4 import BeautifulSoup
import logging


def get_summary(text, max_len=300):
    if not text:
        return ""
    text = text.strip()
    return text[:max_len] + "..." if len(text) > max_len else text


# --- 3DNews ---
def get_3dnews_news():
    try:
        feed = feedparser.parse("https://3dnews.ru/news/rss/")
        result = []
        for entry in feed.entries[:5]:
            result.append({
                "title": entry.title,
                "summary": get_summary(entry.get("summary", "")),
                "link": entry.link,
                "image": entry.get("media_content")[0]["url"]
                if entry.get("media_content") else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка 3DNews: {e}")
        return []


# --- Habr ---
def get_habr_news():
    try:
        feed = feedparser.parse("https://habr.com/ru/rss/all/all/?fl=ru")
        result = []
        for entry in feed.entries[:5]:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Habr: {e}")
        return []


# --- HackerNews ---
def get_hackernews():
    try:
        feed = feedparser.parse("https://news.ycombinator.com/rss")
        result = []
        for entry in feed.entries[:5]:
            result.append({
                "title": entry.title,
                "summary": "",
                "link": entry.link,
                "image": None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка HackerNews: {e}")
        return []


# --- The Verge ---
def get_theverge_news():
    try:
        feed = feedparser.parse("https://www.theverge.com/rss/index.xml")
        result = []
        for entry in feed.entries[:5]:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка The Verge: {e}")
        return []


# --- TechCrunch ---
def get_techcrunch_news():
    try:
        feed = feedparser.parse("https://techcrunch.com/feed/")
        result = []
        for entry in feed.entries[:5]:
            summary_html = entry.get("summary", "")
            if not summary_html and entry.get("content"):
                summary_html = entry.get("content")[0].get("value", "")
            soup = BeautifulSoup(summary_html, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка TechCrunch: {e}")
        return []


# --- Slashdot ---
def get_slashdot_news():
    try:
        feed = feedparser.parse("http://rss.slashdot.org/Slashdot/slashdotMain")
        result = []
        for entry in feed.entries[:5]:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Slashdot: {e}")
        return []


# --- StopGame ---
def get_stopgame_news():
    try:
        url = "https://stopgame.ru/news"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        news_items = soup.find_all("article", class_="_card_1lcny_4")
        results = []
        for item in news_items[:5]:
            title_tag = item.find("a", class_="_title_1lcny_24")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = "https://stopgame.ru" + title_tag["href"] if title_tag and title_tag.get("href") else None
            img_tag = item.find("img")
            image = img_tag["src"] if img_tag and img_tag.get("src") else None
            author_tag = item.find("span", class_="_user-info__name_tf5im_1181")
            author = author_tag.get_text(strip=True) if author_tag else None
            date_tag = item.find("section", class_="_date_1lcny_225")
            date = date_tag.get_text(strip=True) if date_tag else None
            summary_tag = item.find("p")
            summary = summary_tag.get_text(" ", strip=True) if summary_tag else title
            if title and link:
                results.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "image": image,
                    "author": author,
                    "date": date
                })
        return results
    except Exception as e:
        logging.error(f"Ошибка StopGame: {e}")
        return []


# --- Igromania ---
def get_igromania_news():
    try:
        feed = feedparser.parse("https://www.igromania.ru/rss/news.xml")
        result = []
        for entry in feed.entries[:5]:
            soup = BeautifulSoup(entry.get("summary", ""), "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Igromania: {e}")
        return []


# --- Shazoo ---
def get_shazoo_news():
    try:
        feed = feedparser.parse("https://www.shazoo.ru/feed/")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Shazoo: {e}")
        return []


# --- PravilaMag ---
def get_pravilamag_news():
    try:
        feed = feedparser.parse("https://www.pravilamag.ru/rss")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка PravilaMag: {e}")
        return []


# --- KinoPoisk ---
def get_kinopoisk_news():
    try:
        url = "https://www.kinopoisk.ru/news/"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        news_items = soup.select(".news-item")  # пример, может потребоваться уточнить селектор
        results = []
        for item in news_items[:5]:
            title_tag = item.find("a")
            title = title_tag.get_text(strip=True) if title_tag else None
            link = "https://www.kinopoisk.ru" + title_tag["href"] if title_tag else None
            summary_tag = item.find("p")
            summary = summary_tag.get_text(strip=True) if summary_tag else title
            img_tag = item.find("img")
            image = img_tag["src"] if img_tag else None
            if title and link:
                results.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "image": image
                })
        return results
    except Exception as e:
        logging.error(f"Ошибка KinoPoisk: {e}")
        return []


# --- DTF ---
def get_dtf_news():
    try:
        feed = feedparser.parse("https://dtf.ru/rss")
        result = []
        for entry in feed.entries[:5]:
            summary_html = entry.get("summary", "")
            soup = BeautifulSoup(summary_html, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка DTF: {e}")
        return []


# --- NoFilmSchool ---
def get_nofilmschool_news():
    try:
        feed = feedparser.parse("https://nofilmschool.com/rss.xml")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка NoFilmSchool: {e}")
        return []


# --- Pitchfork ---
def get_pitchfork_news():
    try:
        feed = feedparser.parse("https://pitchfork.com/feed/")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Pitchfork: {e}")
        return []


# --- The Quietus ---
def get_thequietus_news():
    try:
        feed = feedparser.parse("https://thequietus.com/rss/news")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка The Quietus: {e}")
        return []


# --- Aeon ---
def get_aeon_news():
    try:
        feed = feedparser.parse("https://aeon.co/feed")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Aeon: {e}")
        return []


# --- Nautilus ---
def get_nautilus_news():
    try:
        feed = feedparser.parse("https://nautil.us/feed")
        result = []
        for entry in feed.entries[:5]:
            content = entry.get("content")[0]["value"] if entry.get("content") else entry.get("summary", "")
            soup = BeautifulSoup(content, "html.parser")
            img = soup.find("img")
            result.append({
                "title": entry.title,
                "summary": get_summary(soup.get_text()),
                "link": entry.link,
                "image": img["src"] if img else None
            })
        return result
    except Exception as e:
        logging.error(f"Ошибка Nautilus: {e}")
        return []
