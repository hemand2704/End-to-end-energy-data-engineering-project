from energy_pipeline.ingestion import create_sample_csv

def test_sample_data_is_written(tmp_path):
    path = create_sample_csv(tmp_path / "sample.csv")
    assert path.exists()
    assert "Global_active_power" in path.read_text(encoding="utf-8")
