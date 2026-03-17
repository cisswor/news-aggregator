import requests
from bs4 import BeautifulSoup

url = "https://feeds.bbci.co.uk/news/rss.xml"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Fetching BBC feed...")
response = requests.get(url, headers=headers, timeout=10)
print(f"Status code: {response.status_code}")
print(f"Content length: {len(response.content)}")
print(f"First 500 chars: {response.text[:500]}")