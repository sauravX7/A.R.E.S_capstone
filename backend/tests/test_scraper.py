import pytest
from app.core.storage import safe_save_artifact
from app.tools.scraper_tools import fetch_and_extract_url
import httpx

def test_safe_save_artifact_valid():
    content = "Hello, world!"
    source_url = "https://example.com"
    artifact = safe_save_artifact(content, source_url, "txt")
    
    assert artifact.artifact_type == "TXT"
    assert artifact.source_url == source_url
    assert artifact.metadata["scraper"] == "A.R.E.S._Scraper"
    assert "data/raw" in artifact.path

def test_safe_save_artifact_path_traversal():
    # File extensions are stripped and sanitized, but even if someone tries to inject:
    content = "Malicious"
    source_url = "https://example.com"
    
    # We validate extensions. If it's malicious it defaults to txt.
    artifact = safe_save_artifact(content, source_url, "../../../etc/passwd")
    
    # The UUID generation + extension safety makes this impossible to traverse, 
    # but let's just make sure it didn't save to /etc/passwd
    assert "/etc/passwd" not in artifact.path
    assert "data/raw" in artifact.path
    assert artifact.artifact_type == "TXT"

# We use the timeout test below to verify failure handling

def test_fetch_timeout():
    # If a URL times out, it shouldn't crash, it should return an error string
    result = fetch_and_extract_url.invoke({"url": "http://10.255.255.1"}) # Non-routable IP, will timeout
    # Depending on network, it might be a connect error or timeout
    assert "Error fetching" in result or "HTTP Error" in result or "timeout" in result.lower() or "connect" in result.lower() or "host is unreachable" in result.lower()
