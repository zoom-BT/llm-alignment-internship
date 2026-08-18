# QLoRA: Efficient Finetuning of Quantized LLMs

- **Link:** arXiv:2305.14314 (Dettmers et al., 2023)
- **Read on:** 2026-08-18

## Problem
LoRA still requires the *frozen* base model to be loaded at full precision (bf16/fp32), which for large models is itself the dominant memory cost — LoRA reduces trainable parameters, not the base model's memory footprint.

## Method
Store the frozen base weights in **4-bit NF4** (NormalFloat4 — a quantization format designed for weights that are roughly normally distributed, unlike uniform 4-bit) instead of bf16/fp32. Add **double quantization**: quantize the per-block scaling constants themselves (not just the weights), squeezing out additional memory. LoRA adapters (`B`, `A`) are still trained at full precision on top of this frozen, quantized base — only the base's *storage* changes, not what's trainable.

## Loss / Objective
Identical to LoRA — no new loss. Compute happens by dequantizing NF4 blocks back to a working precision (bf16 in our implementation) on the fly for each forward/backward pass.

## Compute Budget
Confirmed on our own run: identical trainable-parameter count to plain LoRA (`1,081,344`, 0.22%) — quantization changes only the frozen base's storage, not the adapter. Training was **slower per step** than plain LoRA (on-the-fly dequantization overhead) — a real, measured tradeoff: memory savings cost training time, not just accuracy.

## Key Results
Our own experiment: QLoRA (r=16, NF4) reached **16.84 perplexity**, worse than plain LoRA's 13.795 and Week 2's full fine-tuning's 14.61 — consistent with a higher validation loss observed during training (~2.432 vs. LoRA's ~2.255). The 4-bit compression of the frozen base cost real precision, not a free lunch.

## Limitations
- `bitsandbytes`' 4-bit quantization is **CUDA-only** — cannot run on CPU at all, a hard platform constraint we hit directly when Kaggle's GPU quota ran out mid-project (worked around via Google Colab).
- `merge_and_unload()` on a 4-bit base has known rough edges in `peft` (requires dequantizing first) — we evaluated the quantized model + adapter directly instead, without merging.
- The memory savings matter far more at large model scales; at 0.5B, plain LoRA already fits comfortably without needing quantization at all — QLoRA's real value proposition targets much bigger models than the one we used.

## Takeaway
QLoRA answers a different question than LoRA does: not "can I make an adapter small" (LoRA already does that) but "can I fit an enormous *base* model into limited memory at all." At our small scale, that question doesn't need answering — hence QLoRA underperforming LoRA here isn't a flaw in the method, it's evidence we didn't need it for this experiment.
