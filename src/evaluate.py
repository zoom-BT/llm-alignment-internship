"""Benchmark and generation evaluation via lighteval/evaluate."""


def run_benchmark(config: dict):
    """Score a checkpoint against the benchmark(s) named in config['eval']['benchmarks']."""
    raise NotImplementedError("Wire up once the first checkpoint exists.")


def generate_samples(config: dict, prompts: list[str]):
    """Generate completions for `prompts` from the checkpoint in `config['eval']`."""
    raise NotImplementedError("Wire up once the first checkpoint exists.")
