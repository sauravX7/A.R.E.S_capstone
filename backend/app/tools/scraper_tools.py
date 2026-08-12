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
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        
        # Parse HTML and extract text cleanly
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator='\n')
        
        # Collapse multiple newlines/spaces
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:20000] # Cap output to avoid blowing up the LLM context
        
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
