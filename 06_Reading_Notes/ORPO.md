# ORPO: Monolithic Preference Optimization without Reference Model

- **Link:** arXiv:2403.07691 (Hong et al., 2024)
- **Read on:** 2026-08-18

## Problem
DPO still needs a reference model (double the memory) and generally assumes a prior SFT stage. Can preference optimization and instruction-following be learned in a *single* pass, on a *single* model, with no reference copy at all?

## Method
Combine a standard SFT loss (on the chosen response) with an **odds-ratio** preference term, computed entirely from the model being trained — no reference model, no separate SFT stage required beforehand (though we found this claim has practical limits — see Key Results).

## Loss / Objective
```
L_ORPO = L_SFT(yw) + λ·L_OR
L_OR = −log(σ(log(odds_θ(yw|x)) − log(odds_θ(yl|x))))       where  odds_θ(y|x) = P_θ(y|x) / (1 − P_θ(y|x))
```
`P_θ(y|x)` is the length-normalized sequence probability. Same Bradley-Terry log-sigmoid structure as the RM and DPO losses, applied to log-odds instead of a reward or a log-probability ratio.

## Compute Budget
No second resident model (unlike DPO) — but each training example still runs **both** chosen and rejected through the single model, roughly doubling per-example cost versus plain SFT. Not "free" just because there's no reference model.

## Key Results
**Our own attempt failed and is documented as an honest negative result** (`Week_03_ORPO_Negative_Result.md`). Training diverged to NaN from a raw base model (train loss ~3.1e11, collapsed to `nan`), and again — ruling out "undertrained base model" as the sole cause — from Week 2's SFT checkpoint. Root cause, diagnosed after 5 targeted fixes: on this hardware (T4, no full bf16 support), `fp16` training needs `GradScaler` for numerical stability, but `GradScaler` conflicts with `gradient_checkpointing` (a documented PyTorch issue) — and without `gradient_checkpointing`, the model didn't fit the T4's 16GB even at `batch_size=1`. `GradScaler` and `gradient_checkpointing` were mutually exclusive requirements on this specific hardware/library combination.

## Limitations
- The "no reference model needed" claim is about *architecture*, not training stability — we found ORPO can still diverge numerically depending on precision/memory settings.
- `trl.experimental.orpo` is explicitly marked unstable by TRL itself, compounding the above.
- Even when stable, still costs ~2x per-example compute versus SFT (chosen + rejected both processed).

## Takeaway
The "monolithic, no-reference-model" framing is a real theoretical property (verified — no `ref_model` parameter exists in `ORPOTrainer`), but it doesn't guarantee training stability on constrained, non-Ampere hardware. This is exactly the kind of negative result the internship agreement protects (Article 9) — the diagnostic chain itself (bf16 hardware limits → GradScaler → gradient_checkpointing conflict → OOM) is the real deliverable here, not a working checkpoint.
