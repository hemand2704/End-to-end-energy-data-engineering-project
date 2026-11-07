from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def load_config(config_path=None):
    path = Path(config_path) if config_path else PROJECT_ROOT / "config" / "pipeline.yaml"
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)
