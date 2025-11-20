import re
from bs4 import BeautifulSoup


class HTMLProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespace and clean text"""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def extract_main_content(soup: BeautifulSoup) -> str:
        """Extract main content using heuristic rules"""
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()

        # Try to find main content containers
        selectors = [
            "main",
            "article",
            '[role="main"]',
            ".content",
            ".main-content",
            "#content",
            "#main",
            ".post-content",
            ".post-body",
            ".entry-content",
        ]

        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                return main_content.get_text()

        # Fallback to body
        return soup.get_text()
