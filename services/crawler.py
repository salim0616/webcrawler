import logging
import httpx
from random import choice
from bs4 import BeautifulSoup
from models.crawl_response_meta_data import MetadataResponse
import hashlib
import time
from urllib.parse import urljoin, urlparse
from services.html_processor import HTMLProcessor
from services.classifiers.simple_classifier import classifier

logger = logging.getLogger(__name__)


class WebCrawler:
    def __init__(self):
        self.processor = HTMLProcessor()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        ]

    async def fetch_url(self, url: str, timeout: int = 30) -> str:
        """Fetch URL with proper headers and error handling"""
        headers = {
            "User-Agent": choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
        ) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.text
            except httpx.HTTPError as e:
                logger.error(f"HTTP error while fetching {url}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error while fetching {url}: {e}")
                raise

    def extract_metadata(
        self, html: str, url: str, enable_topics: bool = True
    ) -> MetadataResponse:
        start_time = time.time()

        try:
            soup = BeautifulSoup(html, "lxml")
            parsed_url = urlparse(url)

            # Title
            title = soup.find("title")
            title_text = self.processor.clean_text(title.get_text()) if title else ""

            # Description
            description = ""
            for meta in soup.find_all("meta"):
                if meta.get("name") in ["description", "og:description"]:
                    description = self.processor.clean_text(meta.get("content", ""))
                    break

            # Main content
            main_content = self.processor.extract_main_content(soup)
            cleaned_content = self.processor.clean_text(main_content)

            # Topic classification
            topics = []
            if enable_topics and len(cleaned_content) > 100:
                topics = classifier.classify(cleaned_content)

            # Images
            images = []
            for img in soup.find_all("img")[:20]:
                src = img.get("src") or img.get("data-src")
                if src:
                    absolute_url = urljoin(url, src)
                    images.append(absolute_url)

            # Links
            links = []
            for a in soup.find_all("a")[:50]:
                href = a.get("href")
                if href and href.startswith(("http", "/")):
                    absolute_url = urljoin(url, href)
                    links.append(absolute_url)

            # Content hash for deduplication
            content_hash = hashlib.md5(cleaned_content.encode()).hexdigest()

            processing_time = time.time() - start_time

            return MetadataResponse(
                url=url,
                domain=parsed_url.netloc,
                title=title_text,
                description=description,
                body_text=cleaned_content[:5000],  # Limit for storage
                word_count=len(cleaned_content.split()),
                topics=topics,
                images=images[:10],
                links=links[:20],
                content_hash=content_hash,
                crawl_timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                processing_time=round(processing_time, 2),
            )

        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            raise


crawler = WebCrawler()
