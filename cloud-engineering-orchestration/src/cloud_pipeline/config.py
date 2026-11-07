from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_config(path=None):
    config_path = Path(path) if path else PROJECT_ROOT / "config" / "pipeline.yaml"
    with config_path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)
