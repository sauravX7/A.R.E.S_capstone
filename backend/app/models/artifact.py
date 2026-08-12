from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Optional
from datetime import datetime

class CollectedArtifact(BaseModel):
    """
    Strict contract representing a scraped or collected file.
    Provides enough metadata for the EDA Agent to understand the data.
    """
    artifact_id: str = Field(..., description="Unique identifier for the artifact")
    artifact_type: Literal["CSV", "JSON", "TXT", "HTML"] = Field(..., description="The type of data format")
    path: str = Field(..., description="Absolute or relative path to the saved file")
    source_url: str = Field(..., description="The original URL the data was collected from")
    retrieval_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="When it was collected")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional provenance or context metadata")
