from datasets import Dataset, load_from_disk

from src.data import (
    format_as_chat_messages,
    split_dataset,
    tokenize_and_cache,
    tokenize_example,
)


class FakeTokenizer:
    """Minimal stand-in for a HF tokenizer: no network, just enough to test our own logic."""

    def apply_chat_template(self, messages, tokenize=False):
        return " ".join(m["content"] for m in messages)

    def __call__(self, text):
        words = text.split()
        return {"input_ids": [len(w) for w in words], "attention_mask": [1] * len(words)}


def test_split_dataset_gives_80_10_10_ratio():
    toy = Dataset.from_dict({"x": list(range(100))})
    splits = split_dataset(toy, seed=42)
    assert len(splits["train"]) == 80
    assert len(splits["validation"]) == 10
    assert len(splits["test"]) == 10


def test_split_dataset_has_no_overlap_between_splits():
    toy = Dataset.from_dict({"x": list(range(100))})
    splits = split_dataset(toy, seed=42)
    train_x = set(splits["train"]["x"])
    val_x = set(splits["validation"]["x"])
    test_x = set(splits["test"]["x"])
    assert train_x.isdisjoint(val_x)
    assert train_x.isdisjoint(test_x)
    assert val_x.isdisjoint(test_x)


def test_split_dataset_is_reproducible_with_same_seed():
    toy = Dataset.from_dict({"x": list(range(100))})
    first = split_dataset(toy, seed=42)
    second = split_dataset(toy, seed=42)
    assert list(first["train"]["x"]) == list(second["train"]["x"])


def test_format_as_chat_messages_builds_user_and_assistant_turns():
    example = {"instruction": "What is 2+2?", "context": "", "response": "4"}
    messages = format_as_chat_messages(example)
    assert messages == [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "4"},
    ]


def test_format_as_chat_messages_includes_context_when_present():
    example = {
        "instruction": "Summarize.",
        "context": "Some long text.",
        "response": "Short summary.",
    }
    messages = format_as_chat_messages(example)
    assert "Some long text." in messages[0]["content"]


def test_tokenize_example_returns_input_ids_and_attention_mask():
    example = {"instruction": "hi", "context": "", "response": "hello"}
    result = tokenize_example(FakeTokenizer(), example)
    assert "input_ids" in result
    assert "attention_mask" in result


def test_tokenize_and_cache_saves_to_disk_and_can_be_reloaded(tmp_path):
    toy = Dataset.from_dict(
        {
            "instruction": ["hi", "bye"],
            "context": ["", ""],
            "response": ["hello", "goodbye"],
        }
    )
    cache_dir = tmp_path / "tokenized_cache"

    result = tokenize_and_cache(toy, FakeTokenizer(), str(cache_dir))

    assert cache_dir.exists()
    reloaded = load_from_disk(str(cache_dir))
    assert reloaded["input_ids"] == result["input_ids"]
