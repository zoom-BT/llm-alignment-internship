"""Dataset loading, splitting, and chat-message formatting for fine-tuning runs."""

from datasets import Dataset, DatasetDict, load_dataset


def split_dataset(dataset: Dataset, seed: int) -> DatasetDict:
    """Split `dataset` into reproducible 80/10/10 train/validation/test sets."""
    split_1 = dataset.train_test_split(test_size=0.2, seed=seed)
    split_2 = split_1["test"].train_test_split(test_size=0.5, seed=seed)
    return DatasetDict(
        {
            "train": split_1["train"],
            "validation": split_2["train"],
            "test": split_2["test"],
        }
    )


def load_split_dataset(config: dict) -> DatasetDict:
    """Load `config['data']['dataset_name']` and split it via `split_dataset`."""
    dataset_name = config["data"]["dataset_name"]
    seed = config["training"]["seed"]
    full = load_dataset(dataset_name, split="train")
    return split_dataset(full, seed=seed)


def format_as_chat_messages(example: dict) -> list[dict]:
    """Convert a raw Dolly-15k row into chat messages (user + assistant turns)."""
    user_content = example["instruction"]
    if example["context"]:
        user_content += f"\n\nContext: {example['context']}"
    return [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": example["response"]},
    ]
