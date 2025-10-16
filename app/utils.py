import httpx
from datetime import datetime, timezone
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_cat_fact() -> str:
    """
    Fetch a random cat fact from the Cat Facts API
    Returns a fallback message if the API call fails
    """
    try:
        async with httpx.AsyncClient(timeout=settings.cat_fact_timeout) as client:
            response = await client.get(settings.cat_fact_url)
            response.raise_for_status()
            data = response.json()
            return data.get("fact", "No fact available")
    
    except httpx.TimeoutException:
        logger.warning("Cat Facts API timeout")
        return "Could not fetch cat fact: API timeout"
    
    except httpx.RequestError as e:
        logger.error(f"Cat Facts API request error: {e}")
        return "Could not fetch cat fact: API unavailable"
    
    except Exception as e:
        logger.error(f"Unexpected error fetching cat fact: {e}")
        return "Could not fetch cat fact: Unexpected error"

def get_current_timestamp() -> str:
    """Get current UTC time in ISO 8601 format"""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')