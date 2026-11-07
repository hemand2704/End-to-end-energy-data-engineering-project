from cloud_pipeline.pipeline import run_pipeline

def test_pipeline_creates_processed_file(tmp_path, monkeypatch):
    import cloud_pipeline.pipeline as pipeline
    from cloud_pipeline import config

    monkeypatch.setattr(config, "PROJECT_ROOT", tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "pipeline.yaml").write_text(
        "pipeline:\n  name: test\n  input_file: data/raw/input.csv\n  output_file: data/processed/output.csv\n  s3_prefix: test\naws:\n  region: ap-southeast-2\n",
        encoding="utf-8"
    )
    monkeypatch.setattr(pipeline, "PROJECT_ROOT", tmp_path)
    result = run_pipeline()
    assert result["rows_processed"] > 0
    assert (tmp_path / "data/processed/output.csv").exists()
