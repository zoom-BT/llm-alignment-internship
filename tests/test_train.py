import json

from src.train import build_peft_config, cleanup_checkpoint_dir, save_training_curves


def test_build_peft_config_returns_none_for_full_finetune():
    training_config = {"full_finetune": True, "lora": {"r": 16, "alpha": 32, "dropout": 0.05}}
    assert build_peft_config(training_config) is None


def test_build_peft_config_returns_lora_config_with_configured_values():
    training_config = {"full_finetune": False, "lora": {"r": 16, "alpha": 32, "dropout": 0.05}}
    peft_config = build_peft_config(training_config)
    assert peft_config.r == 16
    assert peft_config.lora_alpha == 32
    assert peft_config.lora_dropout == 0.05
    assert peft_config.task_type == "CAUSAL_LM"


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


def test_cleanup_checkpoint_dir_keeps_only_the_named_entry(tmp_path):
    (tmp_path / "keep.zip").write_text("zip content")
    (tmp_path / "README.md").write_text("a file, not a directory")
    checkpoint_dir = tmp_path / "checkpoint-500"
    checkpoint_dir.mkdir()
    (checkpoint_dir / "model.bin").write_text("weights")
    (tmp_path / "final").mkdir()

    cleanup_checkpoint_dir(str(tmp_path), keep_name="keep.zip")

    remaining = sorted(p.name for p in tmp_path.iterdir())
    assert remaining == ["keep.zip"]


def test_cleanup_checkpoint_dir_is_safe_to_rerun(tmp_path):
    (tmp_path / "keep.zip").write_text("zip content")

    cleanup_checkpoint_dir(str(tmp_path), keep_name="keep.zip")
    cleanup_checkpoint_dir(str(tmp_path), keep_name="keep.zip")  # nothing left to clean, must not error

    remaining = sorted(p.name for p in tmp_path.iterdir())
    assert remaining == ["keep.zip"]
