from energy_pipeline.config import load_config

def test_config_has_required_sections():
    cfg = load_config()
    assert {"project", "source", "paths", "spark", "quality"} <= set(cfg)
    assert cfg["source"]["mode"] in {"sample", "uci"}
