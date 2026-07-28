# Local Testing via Ollama

## Why

No local GPU. Full training happens remotely (Kaggle/Colab); this note
describes how a checkpoint trained remotely gets tested locally on CPU.

## Steps

1. Fine-tune remotely; a LoRA adapter checkpoint is produced.
2. Download the adapter locally.
3. `src/export.py::merge_lora` merges the adapter into the base model's
   full weights.
4. `src/export.py::convert_to_gguf` shells out to llama.cpp's conversion
   script to produce a `.gguf` file (quantized, CPU-friendly).
5. Fill `ollama/Modelfile.template` with the `.gguf` path and a system
   prompt, then `ollama create <name> -f ollama/Modelfile.template`.
6. `ollama run <name>` to chat with the fine-tuned model on CPU.

## Open questions

- Which quantization level (Q4_K_M, Q5_K_M, ...) balances quality vs.
  local RAM/latency — to determine empirically once the first model is
  merged.
