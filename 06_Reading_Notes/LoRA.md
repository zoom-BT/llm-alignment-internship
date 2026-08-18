# LoRA: Low-Rank Adaptation of Large Language Models

- **Link:** arXiv:2106.09685 (Hu et al., 2021)
- **Read on:** 2026-08-15 – 2026-08-18 (theory + implementation this week)

## Problem
Full fine-tuning updates every parameter of a pretrained model — for large models, this means storing a full gradient and optimizer state (AdamW: 2 extra moments) per parameter, at massive memory and storage cost per downstream task/checkpoint.

## Method
Freeze the pretrained weight matrix `W` (shape `d×k`) entirely. Add a trainable low-rank update `ΔW = B·A`, where `B` is `d×r`, `A` is `r×k`, and `r ≪ min(d,k)`. Forward pass: `h = Wx + (α/r)·BAx`. Only `B` and `A` are trained — `r·(d+k)` parameters instead of `d·k`. Hypothesis (validated empirically): the *update* needed to adapt a pretrained model to a new task has low intrinsic rank, even though `W` itself doesn't.

## Loss / Objective
No new loss — same task loss as full fine-tuning (causal LM cross-entropy for us), just computed with far fewer trainable parameters.

## Compute Budget
Verified on our own model: for Qwen2.5-0.5B's Q projection (896×896, r=16), LoRA uses `16×(896+896) = 28,672` params vs. `802,816` full — ~3.6% of that one matrix. Applied to Q/V projections across 24 layers: `1,081,344` trainable params, **0.22%** of the full 495M-parameter model (confirmed via `print_trainable_parameters()` on our actual run).

## Key Results
Our own experiment: LoRA (r=16) reached **13.795 perplexity** on Dolly-15k's test split — better than the baseline (13.92) *and* Week 2's corrected full fine-tuning (14.61), despite updating 450x fewer parameters. Likely explanation: less capacity to drift from the pretrained distribution means less catastrophic forgetting of general language-modeling ability.

## Limitations
- Only as good as the choice of `target_modules` — restricting adaptation to Q/V (the common default) may miss useful capacity in other layers (K, MLP) for harder tasks.
- Rank `r` is a hyperparameter with no principled way to set a priori; too small underfits, too large approaches full fine-tuning's cost.
- Doesn't reduce inference cost unless merged (`merge_and_unload()`) — an unmerged adapter adds a small forward-pass overhead.

## Takeaway
LoRA's real contribution isn't just "fewer trainable parameters" — in our own experiment it produced a *better* result than full fine-tuning, not just a cheaper one, by constraining how far the model can drift from what it already knew. Directly implemented as `build_peft_config()` in `src/train.py`, wired into the same `run_sft()` used for full fine-tuning via a single `full_finetune` flag.
