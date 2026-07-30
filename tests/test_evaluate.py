import torch

from src.evaluate import generate_batch, generate_samples


class FakeGenerationTokenizer:
    eos_token_id = 0

    def __call__(self, text, return_tensors=None):
        return {"input_ids": torch.tensor([[1, 2, 3]])}

    def decode(self, ids, skip_special_tokens=True):
        return "fake completion"


class FakeGenerationModel:
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
