from datasets import Dataset

from src.data import format_as_chat_messages, split_dataset


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
