import json

from src.train import save_training_curves


def test_save_training_curves_creates_png_and_json(tmp_path):
    log_history = [
        {"loss": 3.0, "step": 10},
        {"loss": 2.5, "step": 20},
        {"eval_loss": 2.8, "step": 20},
        {"loss": 2.0, "step": 30},
        {"eval_loss": 2.6, "step": 30},
    ]

    result = save_training_curves(log_history, str(tmp_path))

    assert (tmp_path / "training_curve.png").exists()
    assert (tmp_path / "training_curve.png").stat().st_size > 0
    assert (tmp_path / "training_log_history.json").exists()

    assert result["train_points"] == [(10, 3.0), (20, 2.5), (30, 2.0)]
    assert result["eval_points"] == [(20, 2.8), (30, 2.6)]


def test_save_training_curves_json_matches_input(tmp_path):
    log_history = [{"loss": 1.0, "step": 1}]
    save_training_curves(log_history, str(tmp_path))

    with open(tmp_path / "training_log_history.json") as f:
        saved = json.load(f)
    assert saved == log_history


def test_save_training_curves_handles_missing_eval_points(tmp_path):
    log_history = [{"loss": 1.0, "step": 1}, {"loss": 0.9, "step": 2}]
    result = save_training_curves(log_history, str(tmp_path))
    assert result["eval_points"] == []
