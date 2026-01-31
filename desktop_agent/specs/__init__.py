from pathlib import Path

SPECS_DIR = Path(__file__).parent

def get_schema() -> dict:
    schema_path = SPECS_DIR / "v1" / "schema.json"
    if schema_path.exists():
        import json
        return json.loads(schema_path.read_text())
    return {}

def get_version() -> str:
    return "1.0.0"
