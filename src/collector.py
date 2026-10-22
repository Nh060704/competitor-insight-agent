import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class WebCollector:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def collect_page(self, path="/"):
        url = urljoin(self.base_url, path)
        resp = self.session.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        return {"url": url, "title": soup.title.string if soup.title else "", "content": soup.get_text()}
