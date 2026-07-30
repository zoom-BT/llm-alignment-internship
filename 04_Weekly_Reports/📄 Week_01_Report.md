# Week 1 Research & Progress Report
**Intern:** Balbino Cabrel TCHOUTZINE TCHETNKOU  
**Supervisor:** Mr. Pascal Junior TIKENG NOTSAWO  
**Date:** Friday, July 31, 2026  

## 1. Executive Summary

This week set up a complete, reproducible fine-tuning pipeline from scratch: a version-controlled repository (git + GitHub), a Python environment (`.venv`, `requirements.txt`), and four core modules (`src/data.py`, `src/train.py`, `src/evaluate.py`, `src/utils.py`), each backed by unit tests (18 passing) and covered by CI (lint + tests on every push). The pipeline covers the full loop required by the internship program: tokenization, chat-template formatting, reproducible dataset splitting, text generation (single and batched), baseline evaluation (perplexity), and supervised fine-tuning (SFT) via `trl.SFTTrainer`. Three real, non-trivial bugs were found and fixed along the way (not just typos) — see Section 5. All GPU-dependent work (VRAM benchmarking, baseline evaluation, training) ran on Kaggle (T4), since the local machine has no GPU and limited RAM; local work was restricted to code development, testing, and light CPU-only inference.

## 2. Experimental Setup & Hardware Resources
- **Model Selected:** Qwen/Qwen2.5-0.5B (base, not instruction-tuned) — chosen for fast iteration; full fine-tuning is affordable at this size, so no LoRA/QLoRA yet (planned for Week 3)
- **Dataset:** databricks/databricks-dolly-15k (15,011 examples, human-written instruction/response pairs, CC BY-SA 3.0), split reproducibly 80/10/10 (train/validation/test) with a fixed seed (42)
- **Hardware/GPU Used:** Kaggle, single NVIDIA Tesla T4 (16 GB) — local machine (AMD Ryzen 5 3500U, 13.9 GB RAM, no GPU) used only for development, testing, and CPU inference
- **Precision:** BF16

## 3. Results: Pre vs. Post Fine-Tuning
| Metric | Baseline (Pre-Training) | Fine-Tuned (Post-Training) | Delta |
| :--- | :--- | :--- | :--- |
| **Perplexity** (full 1,502-example test split) | 13.92 | *pending — training in progress* | *pending* |

## 4. Pipeline Reproducibility & Execution Time
- Total End-to-End Pipeline Runtime: *pending — full SFT training currently running on Kaggle; will be filled in once complete, with a check against the <12h requirement*

## 5. Main Technical Challenges & Solutions Encountered
1. **Batched generation silently corrupted by right-padding.** Decoder-only models predict the next token from the last sequence position; the tokenizer's default right-padding pushes that position past the real content for shorter prompts in a batch, producing garbled output for a random subset of examples with no error raised. Fixed by forcing `tokenizer.padding_side = "left"` in `generate_batch()`.
2. **`NaN` silently poisoning the perplexity calculation.** A one-token response has no valid next-token target, so the model returns `NaN` loss for it; since `NaN * 0 == NaN` in floating point, a single degenerate example corrupted the entire running sum. Fixed by skipping any text that tokenizes to fewer than 2 tokens.
3. **Compute silently running on the wrong device.** None of the generation/evaluation functions moved the model or its inputs to GPU — harmless locally (CPU is the only option), but would have silently run everything on CPU even on Kaggle's T4. Fixed by using `model.device` and a shared `get_device()` utility throughout.
4. **Kaggle's "T4 x2" accelerator caused a `DataParallel` device-mismatch crash.** Hugging Face's `Trainer` auto-wraps the model in `torch.nn.DataParallel` whenever more than one GPU is visible, which conflicted with our own single-device placement. Fixed by restricting the session to one GPU via `CUDA_VISIBLE_DEVICES=0`, set before `torch` is imported.
5. **Local resource constraints caused real (not code) crashes.** Loading the model in FP32 (~1.9 GB) segfaulted with the local machine's RAM often near its limit; switching to BF16 (~950 MB) resolved it. This confirmed the decision to keep all GPU-dependent work on Kaggle rather than local CPU.
6. **Intermittent network instability** caused a stalled model download and Hugging Face Hub connection timeouts; resolved by retrying once connectivity was confirmed (falling back to locally cached data where available).

## 6. Deliverables Links
- **GitHub Repository:** https://github.com/zoom-BT/llm-alignment-internship (private — access to be granted to the Supervisor)
- **Hugging Face Hub Model/Adapter:** not yet published — optional per Annex A; to be decided once the fine-tuned checkpoint is evaluated