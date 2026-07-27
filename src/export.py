"""Merge a LoRA adapter into its base model and convert to GGUF for local Ollama testing."""

from pathlib import Path


def merge_lora(base_model_name: str, adapter_path: str, output_dir: str) -> Path:
    """Merge the LoRA weights at `adapter_path` into `base_model_name`, saving to `output_dir`."""
    raise NotImplementedError("Wire up once the first LoRA adapter exists.")


def convert_to_gguf(merged_model_dir: str, llama_cpp_dir: str, output_path: str) -> Path:
    """Shell out to llama.cpp's convert script to produce a GGUF file at `output_path`."""
    raise NotImplementedError("Wire up once llama.cpp is available locally.")
