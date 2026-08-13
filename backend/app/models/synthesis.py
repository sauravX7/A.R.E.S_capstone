from pydantic import BaseModel, Field
from typing import List

class SynthesisResult(BaseModel):
    answer: str = Field(..., description="The main response answering the user request.")
    key_findings: List[str] = Field(default_factory=list, description="A list of bullet points detailing the main factual findings.")
    supporting_artifacts: List[str] = Field(default_factory=list, description="List of valid artifact IDs used to support the answer.")
    warnings: List[str] = Field(default_factory=list, description="Any limitations, missing evidence, or warnings.")
