from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_hackernews():
    try:
        url = "https://news.ycombinator.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        rows = soup.select(".athing")
        for row in rows[:20]:
            title_tag = row.select_one(".titleline a")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = title_tag.get("href", "#")
            if link.startswith("item?"):
                link = f"https://news.ycombinator.com/{link}"

            subtext = row.find_next_sibling("tr")
            points = "0"
            if subtext:
                score_tag = subtext.select_one(".score")
                if score_tag:
                    points = score_tag.text.replace(" points", "").strip()

            articles.append({
                "title": title,
                "link": link,
                "points": points,
                "source": "Hacker News",
                "category": "tech"
            })

        return articles
    except Exception as e:
        print(f"Error scraping Hacker News: {e}")
        return []



def scrape_nytimes():
    try:
        url = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        articles = []

        items = soup.find_all("item")[:20]
        for item in items:
            title = item.find("title")
            link = item.find("link")
            description = item.find("description")

            if not title or not link:
                continue

            articles.append({
                "title": title.text.strip(),
                "link": link.next_sibling.strip() if link.next_sibling else link.text.strip(),
                "description": description.text.strip() if description else "",
                "points": None,
                "source": "NY Times",
                "category": "world"
            })

        print(f"NY Times articles scraped: {len(articles)}")
        return articles
    except Exception as e:
        print(f"Error scraping NY Times: {e}")
        return []

def scrape_techcrunch():
    try:
        url = "https://techcrunch.com/feed/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        articles = []

        items = soup.find_all("item")[:20]
        for item in items:
            title = item.find("title").text.strip()
            link = item.find("link").text.strip()
            description = item.find("description")
            desc = description.text.strip() if description else ""

            articles.append({
                "title": title,
                "link": link,
                "description": desc,
                "points": None,
                "source": "TechCrunch",
                "category": "tech"
            })

        return articles
    except Exception as e:
        print(f"Error scraping TechCrunch: {e}")
        return []


def scrape_reddit_worldnews():
    try:
        url = "https://www.reddit.com/r/worldnews/top.json?limit=20"
        headers = {"User-Agent": "NewsAggregator/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        articles = []

        posts = data["data"]["children"]
        for post in posts:
            p = post["data"]
            articles.append({
                "title": p["title"],
                "link": f"https://reddit.com{p['permalink']}",
                "description": "",
                "points": str(p["score"]),
                "source": "Reddit World News",
                "category": "world"
            })

        return articles
    except Exception as e:
        print(f"Error scraping Reddit: {e}")
        return []


@app.route("/api/news")
def get_news():
    articles = []
    articles += scrape_hackernews()
    articles += scrape_nytimes()
    articles += scrape_techcrunch()
    articles += scrape_reddit_worldnews()
    return jsonify(articles)


@app.route("/api/news/<category>")
def get_news_by_category(category):
    articles = []
    articles += scrape_hackernews()
    articles += scrape_nytimes()
    articles += scrape_techcrunch()
    articles += scrape_reddit_worldnews()

    if category != "all":
        articles = [a for a in articles if a["category"] == category]

    return jsonify(articles)


@app.route("/")
def index():
    return "News Aggregator API is running!"


if __name__ == "__main__":
    app.run(debug=True)