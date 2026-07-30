"""Benchmark and generation evaluation via lighteval/evaluate."""


def run_benchmark(config: dict):
    """Score a checkpoint against the benchmark(s) named in config['eval']['benchmarks']."""
    raise NotImplementedError("Wire up once the first checkpoint exists.")


def generate_samples(model, tokenizer, prompts: list[str], **generation_kwargs) -> list[str]:
    """Generate one completion per prompt in `prompts`, using an already-loaded `model`/`tokenizer`."""
    completions = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(
            **inputs,
            pad_token_id=tokenizer.eos_token_id,
            **generation_kwargs,
        )
        new_tokens = output[0][inputs["input_ids"].shape[1] :]
        completions.append(tokenizer.decode(new_tokens, skip_special_tokens=True))
    return completions
