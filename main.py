import logging
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from config import config
from models.crawl_request import URLRequest
from models.crawl_response_meta_data import MetadataResponse
from services.crawler import crawler

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=config.MAX_LOG_FILE_SIZE,
            backupCount=config.BACKUP_COUNT,
        ),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Web Crawler Metadata Extractor",
    description="A FastAPI application to extract metadata from web pages",
    version="1.0.0",
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=config.ALLOWED_HOSTS,
)


@app.post("/extract-metadata", response_model=MetadataResponse)
async def extract_metadata_endpoint(request: URLRequest):

    try:
        # Validate URL
        parsed_url = urlparse(request.url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL")

        # Fetch and process
        html_content = await crawler.fetch_url(request.url, request.timeout)
        metadata = crawler.extract_metadata(
            html_content, request.url, request.enable_topic_classification
        )
        logger.info(f"Successfully processed URL: {request.url}")
        return metadata
    except httpx.HTTPError as e:
        logger.error(f"HTTP error for {request.url}: {e}")
        raise HTTPException(status_code=422, detail=f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error for {request.url}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
