"""
网页采集模块
负责抓取竞品官网的关键页面内容，并做初步结构化提取
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict
import re
import time


class WebCollector:
    # 默认采集路径，可根据实际情况调整
    DEFAULT_PATHS = ["/", "/products", "/pricing", "/about", "/blog"]

    def __init__(self, base_url: str, paths: List[str] = None):
        self.base_url = base_url.rstrip("/")
        self.domain = urlparse(base_url).netloc
        self.paths = paths or self.DEFAULT_PATHS
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def collect_page(self, path: str = "/") -> Dict:
        """采集单个页面内容，带失败重试"""
        url = urljoin(self.base_url, path)
        max_retries = 2

        for attempt in range(max_retries + 1):
            try:
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")

                title = soup.title.string.strip() if soup.title else ""

                # 去掉导航、页脚等无关内容
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                content = soup.get_text(separator="\n", strip=True)
                content = content[:5000]

                structured = self._extract_structured_info(content)

                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "structured": structured,
                    "status": "success"
                }
            except Exception as e:
                if attempt < max_retries:
                    time.sleep(1)
                    continue
                return {
                    "url": url,
                    "title": "",
                    "content": "",
                    "structured": {},
                    "status": f"failed: {str(e)}"
                }

    def _extract_structured_info(self, text: str) -> Dict:
        """从正文里提取结构化信息：价格、产品名等"""
        result = {
            "prices": [],
            "product_names": []
        }

        # 提取价格
        price_patterns = [
            r'\$(\d+(?:\.\d+)?)',
            r'¥(\d+(?:\.\d+)?)',
            r'每月\s*(\d+(?:\.\d+)?)\s*元',
            r'(\d+(?:\.\d+)?)\s*元/月'
        ]
        for pattern in price_patterns:
            matches = re.findall(pattern, text)
            result["prices"].extend([float(m) for m in matches])

        # 提取产品名
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if 2 < len(line) < 30 and any(kw in line for kw in ["版", "Plan", "方案", "套餐"]):
                result["product_names"].append(line)

        result["prices"] = list(set(result["prices"]))[:5]
        result["product_names"] = list(set(result["product_names"]))[:5]

        return result

    def collect_common_pages(self) -> List[Dict]:
        """采集配置的关键页面"""
        results = []
        for path in self.paths:
            print(f"正在采集: {path}")
            result = self.collect_page(path)
            results.append(result)
            time.sleep(1)
        return results


if __name__ == "__main__":
    collector = WebCollector("https://example.com")
    results = collector.collect_common_pages()
    for r in results:
        print(f"[{r['status']}] {r['url']} - {r['title']}")
