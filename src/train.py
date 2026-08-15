"""SFT / PEFT / DPO training entry points built on TRL and Accelerate.

Meant to run on remote GPUs (Kaggle/Colab); see README.md for the
git-clone-based sync pattern used to pull this module into a notebook.
"""

import json
import shutil
from pathlib import Path


def cleanup_checkpoint_dir(checkpoint_dir: str, keep_name: str) -> None:
    """Remove everything under `checkpoint_dir` except the entry named `keep_name`.

    Handles both files (e.g. a `README.md` `Trainer` writes alongside checkpoints)
    and directories (intermediate `checkpoint-*` snapshots) — `shutil.rmtree` alone
    fails on plain files. Safe to call more than once on the same directory.
    """
    for entry in Path(checkpoint_dir).iterdir():
        if entry.name == keep_name:
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()


def save_training_curves(log_history: list[dict], output_dir: str) -> dict:
    """Save training/eval loss curves (PNG) and the raw log history (JSON) to `output_dir`.

    `log_history` is `trainer.state.log_history` after `trainer.train()`: a list of dicts,
    each either a training-step entry (has `loss`) or an evaluation entry (has `eval_loss`).
    Kept separate from `run_sft` so it can be tested without a real training run.
    """
    import matplotlib

    matplotlib.use("Agg")  # headless backend: no display needed, safe for CI/notebooks
    import matplotlib.pyplot as plt

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    train_points = [(entry["step"], entry["loss"]) for entry in log_history if "loss" in entry]
    eval_points = [
        (entry["step"], entry["eval_loss"]) for entry in log_history if "eval_loss" in entry
    ]

    fig, ax = plt.subplots()
    if train_points:
        steps, losses = zip(*train_points)
        ax.plot(steps, losses, label="train_loss")
    if eval_points:
        steps, losses = zip(*eval_points)
        ax.plot(steps, losses, label="eval_loss")
    ax.set_xlabel("step")
    ax.set_ylabel("loss")
    ax.legend()
    fig.savefig(output_path / "training_curve.png")
    plt.close(fig)

    with open(output_path / "training_log_history.json", "w") as f:
        json.dump(log_history, f, indent=2)

    return {"train_points": train_points, "eval_points": eval_points}


def build_peft_config(training_config: dict):
    """Return a `peft.LoraConfig` built from `training_config['lora']`, or `None` for full fine-tuning.

    Kept separate from `run_sft` so the LoRA/full-finetune switch is testable without a real model.
    """
    if training_config["full_finetune"]:
        return None

    from peft import LoraConfig

    lora_config = training_config["lora"]
    return LoraConfig(
        r=lora_config["r"],
        lora_alpha=lora_config["alpha"],
        lora_dropout=lora_config["dropout"],
        task_type="CAUSAL_LM",
    )


def run_sft(config: dict, max_steps: int = -1):
    """Run supervised fine-tuning with trl.SFTTrainer, using `config['training']` for hyperparameters.

    Full fine-tuning for Week 1 (small model, no `peft_config`); LoRA/QLoRA start in Week 3.

    `max_steps` (-1 by default, meaning "run the full `num_epochs`") lets a caller cap the
    run to a handful of steps for a dry run, to check for out-of-memory errors before
    committing to the full training time.

    Week 2 corrections applied here, in response to Week 1's overfitting result
    (13.92 -> 75.41 perplexity): learning rate lowered an order of magnitude
    (`2e-4` was tuned for LoRA, not full fine-tuning), a warmup + cosine schedule,
    and validation-driven early stopping (`eval_steps`, `load_best_model_at_end`,
    `EarlyStoppingCallback`) so overfitting is caught during training instead of
    only discovered afterward.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, EarlyStoppingCallback
    from trl import SFTConfig, SFTTrainer

    from src.data import format_as_chat_messages, load_split_dataset
    from src.utils import get_device, set_seed

    training_config = config["training"]
    set_seed(training_config["seed"])

    dtype_by_precision = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}
    dtype = dtype_by_precision[training_config["precision"]]

    model_name = config["model"]["base_model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype)
    model.to(get_device())

    splits = load_split_dataset(config)

    def formatting_func(example: dict) -> str:
        messages = format_as_chat_messages(example)
        return tokenizer.apply_chat_template(messages, tokenize=False)

    sft_args = SFTConfig(
        output_dir=config["paths"]["output_dir"] + "checkpoints",
        per_device_train_batch_size=training_config["batch_size"],
        gradient_accumulation_steps=training_config["gradient_accumulation_steps"],
        gradient_checkpointing=training_config["gradient_checkpointing"],
        num_train_epochs=training_config["num_epochs"],
        max_steps=max_steps,
        learning_rate=training_config["learning_rate"],
        warmup_ratio=training_config["warmup_ratio"],
        lr_scheduler_type=training_config["lr_scheduler_type"],
        max_length=training_config["max_seq_length"],
        seed=training_config["seed"],
        report_to=training_config["logging_backend"],
        bf16=(training_config["precision"] == "bf16"),
        fp16=(training_config["precision"] == "fp16"),
        eval_strategy="steps",
        eval_steps=training_config["eval_steps"],
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_args,
        train_dataset=splits["train"],
        eval_dataset=splits["validation"],
        processing_class=tokenizer,
        formatting_func=formatting_func,
        peft_config=build_peft_config(training_config),
        callbacks=[
            EarlyStoppingCallback(early_stopping_patience=training_config["early_stopping_patience"])
        ],
    )
    trainer.train()
    trainer.save_model(config["paths"]["output_dir"] + "checkpoints/final")
    save_training_curves(trainer.state.log_history, config["paths"]["output_dir"])
    return trainer


def run_dpo(config: dict):
    """Run DPO/ORPO alignment using trl per `config['training']`."""
    raise NotImplementedError("Wire up once a reference SFT checkpoint exists.")
