from langchain_core.tools import tool
import httpx
from bs4 import BeautifulSoup
from app.core.storage import safe_save_artifact
import logging

logger = logging.getLogger(__name__)

@tool
def fetch_and_extract_url(url: str) -> str:
    """
    Fetches a URL and extracts its text content. 
    Use this to read data from a specific website.
    """
    try:
        # Use httpx for modern, async-compatible HTTP client capabilities
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = httpx.get(url, headers=headers, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        
        # If it's a CSV or JSON file directly, preserve the raw text
        content_type = response.headers.get('content-type', '').lower()
        if url.endswith('.csv') or 'text/csv' in content_type:
            return response.text[:20000]
            
        if url.endswith('.json') or 'application/json' in content_type:
            return response.text[:20000]
        
        # Parse HTML and extract text cleanly
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove navigation, script, style, header, footer elements
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.extract()
            
        content_root = soup.find('main') or soup.find('article') or soup.find('div', id='bodyContent') or soup.find('body') or soup
        text = content_root.get_text(separator=' ', strip=True)
        
        # Limit to 8000 chars to avoid overwhelming the LLM
        if len(text) > 8000:
            text = text[:8000] + "\n\n... [TRUNCATED FOR LENGTH]"
            
        return text
        
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code} fetching {url}: {e}"
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

@tool
def save_scraped_data(content: str, source_url: str, file_extension: str) -> str:
    """
    Saves extracted data to local storage and returns the generated Artifact ID.
    file_extension should be 'txt', 'csv', 'json', or 'html'.
    """
    try:
        artifact = safe_save_artifact(content, source_url, file_extension)
        # Return a JSON string representation so the LLM understands it succeeded
        return artifact.model_dump_json()
    except Exception as e:
        return f"Failed to save artifact: {str(e)}"
