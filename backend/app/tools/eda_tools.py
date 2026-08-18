import pandas as pd
import json
import logging
import subprocess
import tempfile
import os
from pathlib import Path
from langchain_core.tools import tool
from typing import Dict, Any

logger = logging.getLogger(__name__)
BASE_STORAGE_DIR = (Path(__file__).parent.parent.parent.parent / "data" / "raw").resolve()
PROCESSED_STORAGE_DIR = (Path(__file__).parent.parent.parent.parent / "data" / "processed").resolve()
PROCESSED_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def _load_dataset(artifact_id: str) -> pd.DataFrame:
    """Helper to safely load a dataset (CSV, JSON, or TXT) from the secure storage."""
    for ext in [".csv", ".json", ".txt"]:
        file_path = BASE_STORAGE_DIR / f"{artifact_id}{ext}"
        if file_path.exists():
            if not str(file_path.resolve()).startswith(str(BASE_STORAGE_DIR)):
                raise ValueError(f"Path Traversal Attempt Detected: {file_path}")
            if ext == ".csv":
                return pd.read_csv(file_path)
            elif ext == ".json":
                return pd.read_json(file_path)
            elif ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                return pd.DataFrame({
                    "line_number": list(range(1, len(lines) + 1)),
                    "text_content": lines,
                    "char_count": [len(l) for l in lines],
                    "word_count": [len(l.split()) for l in lines]
                })
    
    raise FileNotFoundError(f"Artifact {artifact_id} not found in {BASE_STORAGE_DIR}")

@tool
def inspect_dataset(artifact_id: str) -> str:
    """Returns row counts, column names, data types, and missing value counts without arbitrary execution."""
    try:
        df = _load_dataset(artifact_id)
        info = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "sample": df.head(3).to_dict(orient="records")
        }
        return json.dumps(info, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def missing_values_analysis(artifact_id: str) -> str:
    """Analyzes missing values in detail."""
    try:
        df = _load_dataset(artifact_id)
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        result = pd.DataFrame({
            "count": missing_counts,
            "percentage": missing_percentages
        }).to_dict(orient="index")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def descriptive_statistics(artifact_id: str) -> str:
    """Returns descriptive statistics for numeric columns."""
    try:
        df = _load_dataset(artifact_id)
        stats = df.describe().to_dict()
        return json.dumps(stats, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def execute_custom_code(artifact_id: str, python_code: str) -> str:
    """
    [EXPERIMENTAL UNTRUSTED MODE]
    Executes custom python code in a subprocess with a timeout.
    The code will be injected with a `df` variable representing the dataset.
    """
    mode = os.environ.get("EDA_EXECUTION_MODE", "controlled")
    if mode != "untrusted_subprocess":
        return json.dumps({"error": "Security Rejection: execute_custom_code is disabled unless EDA_EXECUTION_MODE=untrusted_subprocess"})
    
    try:
        file_path = BASE_STORAGE_DIR / f"{artifact_id}.csv"
        if not file_path.exists():
            return json.dumps({"error": f"Dataset {artifact_id} not found."})

        # Inject the setup code
        injected_code = f"""
import pandas as pd
import numpy as np

# Load the requested artifact securely
df = pd.read_csv('{file_path.resolve()}')

{python_code}
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(injected_code)
            temp_path = f.name
            
        # Execute the script in a bounded subprocess
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=10 # 10 second bounded limit
        )
        
        os.unlink(temp_path)
        
        return json.dumps({
            "stdout": result.stdout[:5000], # Cap output
            "stderr": result.stderr[:5000],
            "returncode": result.returncode
        })
        
    except subprocess.TimeoutExpired:
        if 'temp_path' in locals(): os.unlink(temp_path)
        return json.dumps({"error": "Subprocess execution timed out after 10 seconds."})
    except Exception as e:
        return json.dumps({"error": str(e)})
