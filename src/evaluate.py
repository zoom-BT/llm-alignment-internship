"""Benchmark and generation evaluation via lighteval/evaluate."""

import json
import math
from pathlib import Path

from src.data import load_split_dataset


def compute_perplexity(model, tokenizer, texts: list[str]) -> float:
    """Compute corpus-level perplexity: exp(mean cross-entropy loss, weighted by token count)."""
    total_loss = 0.0
    total_tokens = 0
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        num_tokens = inputs["input_ids"].shape[1] - 1  # shifted: n-1 next-token predictions
        if num_tokens < 1:
            continue  # a single token has no next-token target; loss would be NaN
        outputs = model(**inputs, labels=inputs["input_ids"])
        total_loss += outputs.loss.item() * num_tokens
        total_tokens += num_tokens
    return math.exp(total_loss / total_tokens)


def run_benchmark(
    config: dict, model_path: str | None = None, output_filename: str = "baseline_results.json"
) -> dict:
    """Compute perplexity of a model on the test split, and save the result to
    `config['paths']['output_dir']/output_filename`.

    `model_path` defaults to `config['model']['base_model_name']` (the base model, for the
    "before" baseline). Pass a local checkpoint directory (e.g. `results/checkpoints/final`)
    to evaluate a fine-tuned model instead, for the "after" comparison — same dataset, same
    metric, same code path, so the two numbers are directly comparable.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from src.utils import get_device

    dtype_by_precision = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}
    dtype = dtype_by_precision[config["training"]["precision"]]

    model_name = model_path or config["model"]["base_model_name"]
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=dtype)
    model.to(get_device())
    model.eval()

    splits = load_split_dataset(config)
    texts = splits["test"]["response"]

    with torch.no_grad():
        perplexity = compute_perplexity(model, tokenizer, texts)

    results = {
        "model": model_name,
        "dataset": config["data"]["dataset_name"],
        "metric": "perplexity",
        "split": "test",
        "num_examples": len(texts),
        "perplexity": perplexity,
    }

    output_path = Path(config["paths"]["output_dir"]) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    return results


def generate_samples(model, tokenizer, prompts: list[str], **generation_kwargs) -> list[str]:
    """Generate one completion per prompt in `prompts`, using an already-loaded `model`/`tokenizer`."""
    completions = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        output = model.generate(
            **inputs,
            pad_token_id=tokenizer.eos_token_id,
            **generation_kwargs,
        )
        new_tokens = output[0][inputs["input_ids"].shape[1] :]
        completions.append(tokenizer.decode(new_tokens, skip_special_tokens=True))
    return completions


def generate_batch(model, tokenizer, prompts: list[str], **generation_kwargs) -> list[str]:
    """Generate completions for all `prompts` at once.

    Decoder-only models must be left-padded for batched generation: the next
    token is always predicted from the last position, so padding on the right
    would push that position past the real content.
    """
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(prompts, return_tensors="pt", padding=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    output = model.generate(
        **inputs,
        pad_token_id=tokenizer.eos_token_id,
        **generation_kwargs,
    )
    prompt_length = inputs["input_ids"].shape[1]
    return [
        tokenizer.decode(output[i][prompt_length:], skip_special_tokens=True)
        for i in range(len(prompts))
    ]
