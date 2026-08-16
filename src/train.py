"""SFT / PEFT / DPO training entry points built on TRL and Accelerate.

Meant to run on remote GPUs (Kaggle/Colab); see README.md for the
git-clone-based sync pattern used to pull this module into a notebook.
"""

import json
import math
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

    train_points = [
        (entry["step"], entry["loss"]) for entry in log_history if "loss" in entry
    ]
    eval_points = [
        (entry["step"], entry["eval_loss"])
        for entry in log_history
        if "eval_loss" in entry
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


def compute_warmup_steps(
    dataset_size: int,
    batch_size: int,
    gradient_accumulation_steps: int,
    num_epochs: int,
    warmup_ratio: float,
    max_steps: int = -1,
) -> int:
    """Convert a warmup *ratio* into an absolute step count.

    Newer `trl` versions dropped `SFTConfig`'s `warmup_ratio` parameter in favor of
    `warmup_steps` only, which needs the total optimizer-step count computed up front
    to stay proportional. Mirrors `Trainer`'s own rule: `max_steps` (when set) overrides
    epoch-based counting entirely rather than being combined with it.
    """
    if max_steps > 0:
        total_steps = max_steps
    else:
        effective_batch_size = batch_size * gradient_accumulation_steps
        steps_per_epoch = math.ceil(dataset_size / effective_batch_size)
        total_steps = steps_per_epoch * num_epochs
    return int(total_steps * warmup_ratio)


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

    dtype_by_precision = {
        "fp32": torch.float32,
        "fp16": torch.float16,
        "bf16": torch.bfloat16,
    }
    dtype = dtype_by_precision[training_config["precision"]]

    model_name = config["model"]["base_model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype)
    model.to(get_device())

    splits = load_split_dataset(config)

    def formatting_func(example: dict) -> str:
        messages = format_as_chat_messages(example)
        return tokenizer.apply_chat_template(messages, tokenize=False)

    warmup_steps = compute_warmup_steps(
        dataset_size=len(splits["train"]),
        batch_size=training_config["batch_size"],
        gradient_accumulation_steps=training_config["gradient_accumulation_steps"],
        num_epochs=training_config["num_epochs"],
        warmup_ratio=training_config["warmup_ratio"],
        max_steps=max_steps,
    )

    sft_args = SFTConfig(
        output_dir=config["paths"]["output_dir"] + "checkpoints",
        per_device_train_batch_size=training_config["batch_size"],
        gradient_accumulation_steps=training_config["gradient_accumulation_steps"],
        gradient_checkpointing=training_config["gradient_checkpointing"],
        num_train_epochs=training_config["num_epochs"],
        max_steps=max_steps,
        learning_rate=training_config["learning_rate"],
        warmup_steps=warmup_steps,
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
            EarlyStoppingCallback(
                early_stopping_patience=training_config["early_stopping_patience"]
            )
        ],
    )
    trainer.train()
    trainer.save_model(config["paths"]["output_dir"] + "checkpoints/final")
    save_training_curves(trainer.state.log_history, config["paths"]["output_dir"])
    return trainer


def run_dpo(config: dict, model_path: str | None = None, max_steps: int = -1):
    """Run DPO alignment with `trl.DPOTrainer`, using `config['dpo']` for hyperparameters.

    `model_path` (defaults to `config['model']['base_model_name']`) is the checkpoint to
    start from — normally an already-SFT'd model, since DPO's theory assumes a reference
    policy `pi_ref` that already follows instructions reasonably well. Passing
    `ref_model=None` to `DPOTrainer` makes it create its own frozen copy of the starting
    model internally as `pi_ref`, matching that theory exactly.
    """
    import torch
    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOConfig, DPOTrainer

    from src.utils import get_device, set_seed

    training_config = config["training"]
    dpo_config_values = config["dpo"]
    set_seed(training_config["seed"])

    dtype_by_precision = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}
    dtype = dtype_by_precision[training_config["precision"]]

    model_name = model_path or config["model"]["base_model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype)
    model.to(get_device())

    train_dataset = load_dataset(dpo_config_values["dataset_name"], split="train")
    train_dataset = train_dataset.select(range(dpo_config_values["train_size"]))
    eval_dataset = load_dataset(dpo_config_values["dataset_name"], split="test")
    eval_dataset = eval_dataset.select(range(dpo_config_values["eval_size"]))

    dpo_args = DPOConfig(
        output_dir=config["paths"]["output_dir"] + "dpo_checkpoints",
        per_device_train_batch_size=dpo_config_values["batch_size"],
        per_device_eval_batch_size=dpo_config_values["batch_size"],
        gradient_accumulation_steps=dpo_config_values["gradient_accumulation_steps"],
        gradient_checkpointing=dpo_config_values["gradient_checkpointing"],
        beta=dpo_config_values["beta"],
        num_train_epochs=dpo_config_values["num_epochs"],
        max_steps=max_steps,
        learning_rate=dpo_config_values["learning_rate"],
        max_length=training_config["max_seq_length"],
        seed=training_config["seed"],
        report_to=training_config["logging_backend"],
        bf16=(training_config["precision"] == "bf16"),
        fp16=(training_config["precision"] == "fp16"),
        eval_strategy="steps",
        eval_steps=dpo_config_values["eval_steps"],
    )

    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=dpo_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
    )
    trainer.train()
    trainer.save_model(config["paths"]["output_dir"] + "dpo_checkpoints/final")
    save_training_curves(trainer.state.log_history, config["paths"]["output_dir"] + "dpo")
    return trainer


def run_orpo(config: dict, model_path: str | None = None, max_steps: int = -1):
    """Run ORPO alignment with `trl.experimental.orpo.ORPOTrainer`, using `config['orpo']`.

    Unlike DPO, ORPO needs no separate reference model: its loss combines the standard SFT
    cross-entropy (on the chosen response) with an odds-ratio preference term computed
    entirely from the model being trained, so only one model copy is ever resident in
    memory. ORPOConfig names the odds-ratio term's weight `beta`, even though it plays the
    role the ORPO paper calls lambda -- unrelated to DPO's KL-penalty beta despite the
    shared field name.
    """
    import torch
    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl.experimental.orpo import ORPOConfig, ORPOTrainer

    from src.utils import get_device, set_seed

    training_config = config["training"]
    orpo_config_values = config["orpo"]
    set_seed(training_config["seed"])

    dtype_by_precision = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}
    dtype = dtype_by_precision[training_config["precision"]]

    model_name = model_path or config["model"]["base_model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype)
    model.to(get_device())

    train_dataset = load_dataset(orpo_config_values["dataset_name"], split="train")
    train_dataset = train_dataset.select(range(orpo_config_values["train_size"]))
    eval_dataset = load_dataset(orpo_config_values["dataset_name"], split="test")
    eval_dataset = eval_dataset.select(range(orpo_config_values["eval_size"]))

    orpo_args = ORPOConfig(
        output_dir=config["paths"]["output_dir"] + "orpo_checkpoints",
        per_device_train_batch_size=orpo_config_values["batch_size"],
        per_device_eval_batch_size=orpo_config_values["batch_size"],
        gradient_accumulation_steps=orpo_config_values["gradient_accumulation_steps"],
        gradient_checkpointing=orpo_config_values["gradient_checkpointing"],
        beta=orpo_config_values["lambda_orpo"],
        num_train_epochs=orpo_config_values["num_epochs"],
        max_steps=max_steps,
        learning_rate=orpo_config_values["learning_rate"],
        max_length=training_config["max_seq_length"],
        seed=training_config["seed"],
        report_to=training_config["logging_backend"],
        bf16=(training_config["precision"] == "bf16"),
        fp16=(training_config["precision"] == "fp16"),
        eval_strategy="steps",
        eval_steps=orpo_config_values["eval_steps"],
    )

    trainer = ORPOTrainer(
        model=model,
        args=orpo_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
    )
    trainer.train()
    trainer.save_model(config["paths"]["output_dir"] + "orpo_checkpoints/final")
    save_training_curves(trainer.state.log_history, config["paths"]["output_dir"] + "orpo")
    return trainer
