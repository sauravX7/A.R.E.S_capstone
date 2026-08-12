import os
import uuid
from pathlib import Path
from app.models.artifact import CollectedArtifact

# Ensure the base directory exists
BASE_STORAGE_DIR = (Path(__file__).parent.parent.parent.parent / "data" / "raw").resolve()
BASE_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def safe_save_artifact(content: str, source_url: str, file_extension: str) -> CollectedArtifact:
    """
    Saves content to the strictly controlled data/raw directory.
    Validates the extension and generates a safe UUID filename to prevent path traversal.
    """
    # Force extension safety
    ext = file_extension.lower().replace(".", "")
    if ext not in ["txt", "html", "csv", "json"]:
        ext = "txt"
        
    artifact_id = str(uuid.uuid4())
    safe_filename = f"{artifact_id}.{ext}"
    
    # Resolve and enforce strict boundaries
    file_path = (BASE_STORAGE_DIR / safe_filename).resolve()
    
    if not str(file_path).startswith(str(BASE_STORAGE_DIR)):
        raise ValueError(f"Path Traversal Attempt Detected: {file_path}")
        
    # Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Construct metadata
    return CollectedArtifact(
        artifact_id=artifact_id,
        artifact_type=ext.upper(), # type: ignore
        path=str(file_path),
        source_url=source_url,
        metadata={"scraper": "A.R.E.S._Scraper", "byte_size": len(content.encode('utf-8'))}
    )
