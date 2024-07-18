import logging
import time
import aiohttp
import redis
from scraper import fetch_availability  # Import from scraper.py
import config
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Połączenie z Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def get_cached_data(url):
    data = redis_client.get(url)
    if data:
        logger.info(f"Data found in cache for {url}: {data}")
        try:
            cached_data = json.loads(data)
            return cached_data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from cache for {url}: {e}")
            return None
    logger.info(f"No cache data found for {url}")
    return None

def set_cache_data(url, data):
    logger.info(f"Caching data for {url}: {data}")
    try:
        json_data = json.dumps(data)
        redis_client.setex(url, config.CACHE_TIMEOUT, json_data)
    except TypeError as e:
        logger.error(f"Error encoding JSON for {url}: {e}")

async def fetch_data(name, url):
    cached_data = get_cached_data(url)
    if cached_data is not None:
        logger.info(f"Using cached data for {url}")
        return name, cached_data
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html_content = await response.text()
        data = fetch_availability(html_content)
        if data:
            set_cache_data(url, data)
            logger.info(f"Fetched and cached data for {url}")
        return name, data
    except Exception as e:
        logger.error(f"Error fetching data for {url}: {e}")
        return name, []
