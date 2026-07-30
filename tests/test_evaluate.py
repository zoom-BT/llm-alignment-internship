import math

import torch

from src.evaluate import compute_perplexity, generate_batch, generate_samples


class FakeGenerationTokenizer:
    eos_token_id = 0

    def __call__(self, text, return_tensors=None):
        return {"input_ids": torch.tensor([[1, 2, 3]])}

    def decode(self, ids, skip_special_tokens=True):
        return "fake completion"


class FakeGenerationModel:
    device = torch.device("cpu")

    def generate(self, input_ids, pad_token_id=None, **kwargs):
        # Simulates appending 2 newly generated tokens after the prompt tokens.
        return torch.cat([input_ids, torch.tensor([[4, 5]])], dim=1)


def test_generate_samples_returns_one_completion_per_prompt():
    completions = generate_samples(
        FakeGenerationModel(), FakeGenerationTokenizer(), ["prompt one", "prompt two"]
    )
    assert len(completions) == 2
    assert all(c == "fake completion" for c in completions)


def test_generate_samples_forwards_generation_kwargs():
    seen_kwargs = {}

    class RecordingModel(FakeGenerationModel):
        def generate(self, input_ids, pad_token_id=None, **kwargs):
            seen_kwargs.update(kwargs)
            return super().generate(input_ids, pad_token_id=pad_token_id, **kwargs)

    generate_samples(
        RecordingModel(), FakeGenerationTokenizer(), ["prompt"], temperature=0.7, do_sample=True
    )
    assert seen_kwargs == {"temperature": 0.7, "do_sample": True}


class FakeBatchTokenizer:
    eos_token_id = 0
    eos_token = "<eos>"
    pad_token = None
    padding_side = "right"  # deliberately wrong default, like real tokenizers

    def __call__(self, prompts, return_tensors=None, padding=None):
        return {"input_ids": torch.tensor([[1, 2] for _ in prompts])}

    def decode(self, ids, skip_special_tokens=True):
        return "batch completion"


class FakeBatchModel:
    device = torch.device("cpu")

    def generate(self, input_ids, pad_token_id=None, **kwargs):
        extra = torch.tensor([[9, 9] for _ in range(input_ids.shape[0])])
        return torch.cat([input_ids, extra], dim=1)


def test_generate_batch_forces_left_padding():
    tokenizer = FakeBatchTokenizer()
    generate_batch(FakeBatchModel(), tokenizer, ["a", "b", "c"])
    assert tokenizer.padding_side == "left"


def test_generate_batch_returns_one_completion_per_prompt():
    completions = generate_batch(FakeBatchModel(), FakeBatchTokenizer(), ["a", "b", "c"])
    assert len(completions) == 3
    assert all(c == "batch completion" for c in completions)


class FakePerplexityTokenizer:
    def __call__(self, text, return_tensors=None):
        # One token per character - simplistic but deterministic and controllable.
        return {"input_ids": torch.tensor([[0] * len(text)])}


class VariableLossModel:
    """Returns a different fixed loss depending on the input length, to test weighting."""

    device = torch.device("cpu")

    def __call__(self, input_ids, labels=None):
        class Output:
            pass

        out = Output()
        out.loss = torch.tensor(2.0 if input_ids.shape[1] <= 2 else 1.0)
        return out


def test_compute_perplexity_weights_by_token_count_not_by_text_count():
    # "aaaa" -> 4 tokens -> 3 predicted positions, loss=1.0
    # "bb"   -> 2 tokens -> 1 predicted position,  loss=2.0
    # weighted mean loss = (1.0*3 + 2.0*1) / (3+1) = 1.25, NOT the naive (1.0+2.0)/2 = 1.5
    ppl = compute_perplexity(VariableLossModel(), FakePerplexityTokenizer(), ["aaaa", "bb"])
    assert ppl == math.exp(1.25)


class ModelWithNaNOnSingleToken:
    """A single-token input has no valid next-token target; a real model returns NaN loss for it."""

    device = torch.device("cpu")

    def __call__(self, input_ids, labels=None):
        class Output:
            pass

        out = Output()
        out.loss = torch.tensor(float("nan") if input_ids.shape[1] <= 1 else 1.0)
        return out


def test_compute_perplexity_skips_texts_with_fewer_than_2_tokens():
    # "a" -> 1 token -> no predicted position, must be skipped (would otherwise poison the sum with NaN)
    # "bb" -> 2 tokens -> 1 predicted position, loss=1.0
    ppl = compute_perplexity(ModelWithNaNOnSingleToken(), FakePerplexityTokenizer(), ["a", "bb"])
    assert not math.isnan(ppl)
    assert ppl == math.exp(1.0)
