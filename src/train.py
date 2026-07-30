"""SFT / PEFT / DPO training entry points built on TRL and Accelerate.

Meant to run on remote GPUs (Kaggle/Colab); see README.md for the
git-clone-based sync pattern used to pull this module into a notebook.
"""


def run_sft(config: dict):
    """Run supervised fine-tuning with trl.SFTTrainer, using `config['training']` for hyperparameters.

    Full fine-tuning for Week 1 (small model, no `peft_config`); LoRA/QLoRA start in Week 3.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
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
        learning_rate=training_config["learning_rate"],
        max_length=training_config["max_seq_length"],
        seed=training_config["seed"],
        report_to=training_config["logging_backend"],
        bf16=(training_config["precision"] == "bf16"),
        fp16=(training_config["precision"] == "fp16"),
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_args,
        train_dataset=splits["train"],
        eval_dataset=splits["validation"],
        processing_class=tokenizer,
        formatting_func=formatting_func,
    )
    trainer.train()
    trainer.save_model(config["paths"]["output_dir"] + "checkpoints/final")
    return trainer


def run_dpo(config: dict):
    """Run DPO/ORPO alignment using trl per `config['training']`."""
    raise NotImplementedError("Wire up once a reference SFT checkpoint exists.")
