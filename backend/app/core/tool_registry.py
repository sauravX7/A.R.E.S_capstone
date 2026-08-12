"""
Tool Registry Contract.

YAML configuration files can only specify tools by names defined in this registry.
This prevents arbitrary code execution or unrecognized tool requests.
"""

AVAILABLE_TOOLS = {
    "fetch_and_extract_url",
    "save_scraped_data",
    "inspect_dataset",
    "missing_values_analysis",
    "descriptive_statistics",
    "execute_custom_code",
    "web_search",
    "extract_html",
    "extract_csv",
    "execute_pandas",
    "generate_chart"
}

def validate_tool_name(tool_name: str) -> bool:
    """Returns True if the tool name exists in the registry."""
    return tool_name in AVAILABLE_TOOLS
