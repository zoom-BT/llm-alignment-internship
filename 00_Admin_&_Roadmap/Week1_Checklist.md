# 🎯 Week 1: Building a Reproducible Fine-Tuning Pipeline

## 📥 Deliverables Checklist (Due: Friday 11:00 AM)
- [x] Code repository structured & initialized
- [x] `README.md` with installation & execution instructions
- [x] Dependency file (`requirements.txt` / `environment.yml`)
- [x] Experiment configuration file (`config.yaml`)
- [x] Inference script (`inference.py`) — as `generate_samples()`/`generate_batch()` in `src/evaluate.py`, not a standalone `inference.py`; the contract's Annex A only requires "an inference script," not that exact filename
- [x] Training script (`train.py`) — `src/train.py`, `run_sft()`
- [x] Evaluation script (`evaluate_model.py`) — as `src/evaluate.py` (`compute_perplexity()`, `run_benchmark()`), same naming note as above
- [x] Evaluation results before & after fine-tuning (`results.json`) — two files, `results/baseline_results.json` (13.92) and `results/finetuned_results.json` (75.41), rather than one merged file
- [x] Estimate of training time & compute resources used — in `Week_01_Report.md` §4
- [x] Short note describing main difficulties encountered — in `Week_01_Report.md` §5 (6 real bugs, not just typos)
- [x] Evidence that pipeline runs end-to-end in < 12 hours — ≈6h total, documented in `Week_01_Report.md` §4
- [ ] Send weekly report & deliverables via email (Friday at 11:00 AM) — report is ready; sending the email and adding the Supervisor as a GitHub collaborator (private repo) are still manual steps only I can do
- [ ] Prepare demo for Weekly Meeting (Friday at 12:00 PM) — presentation content drafted; slides not yet built, meeting not yet held

---

## 📚 Technical Concepts Matrix (Week 1)
- [x] Python environments & dependency management — deep dive (venv, `--system-site-packages`, isolation rationale)
- [x] Git & code repository workflow — deep dive (staging, commits, push, `.gitignore`)
- [x] Basic PyTorch mechanics (tensors, parameters, gradients, CUDA) — tensors/CUDA deep dive Monday; parameters & gradients deep dive Friday with a real single-parameter gradient-descent walkthrough
- [x] Transformer architecture fundamentals — deep dive (layers, multi-head attention, Q/K/V, real attention weights inspected)
- [x] Tokenizers, tokenization, and control tokens — deep dive (BPE built from scratch, special tokens)
- [x] Autoregressive language modeling & next-token prediction — deep dive, incl. the "first token"/BOS edge case
- [x] Base models vs. Instruction-tuned models — covered via Qwen2.5-0.5B base vs. `-Instruct` distinction during generation
- [x] Conversational formats & Chat Templates — deep dive
- [x] Dataset splits: train, validation, and test sets — deep dive, incl. a real duplication/contamination finding
- [x] Batches, epochs, learning rates, and optimizers (AdamW) — deep dive Friday: batch gradient averaging demonstrated, AdamW's momentum/variance internals inspected directly on a toy parameter
- [x] GPU memory (VRAM) management — deep dive (Monday's benchmark, repeated real memory-limit incidents)
- [x] Numerical precision: FP32, FP16, and BF16 — deep dive
- [x] Gradient accumulation — deep dive Friday: proved 4 accumulated micro-batches produce the exact same gradient as 1 real batch of 4
- [x] Gradient checkpointing — deep dive Friday: proved identical gradients with/without checkpointing on a toy 6-layer stack, confirming "trade compute for memory" costs no precision
- [x] Random seeds & strict reproducibility — deep dive
- [x] Model checkpoints saving/loading — deep dive Friday: save/load round-trip on a toy model, confirmed bit-exact recovery of weights
- [x] Metric logging & training curves (`wandb` / `tensorboard`) — TensorBoard configured, and a real training curve analyzed in depth (epoch-boundary drops as an overfitting signal)
- [x] Model & dataset licenses — Dolly-15k's CC BY-SA 3.0 discussed and documented