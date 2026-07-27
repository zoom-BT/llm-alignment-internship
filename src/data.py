"""Dataset loading, tokenization, and chat-template helpers for fine-tuning runs.

Implemented incrementally as specific datasets and base models are chosen
during the internship; see 06_Reading_Notes/ and 03_Experiments/ for the
decisions driving each iteration.
"""


def load_dataset_from_config(config: dict):
    """Load and return a Hugging Face dataset described by config['paths']['data_dir']."""
    raise NotImplementedError("Wire up once the first dataset is chosen.")


def build_chat_template(tokenizer, config: dict):
    """Attach/verify the chat template used to format prompts for `tokenizer`."""
    raise NotImplementedError("Wire up once the first base model is chosen.")
