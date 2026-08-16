# Week 3 — ORPO: A Documented Negative Result

**Summary:** `trl.experimental.orpo.ORPOTrainer` could not be trained stably on Qwen2.5-0.5B on a Kaggle T4 GPU, despite five successive, targeted fixes. This is documented as an honest negative result (per Article 9 of the internship agreement) rather than resolved through further trial and error, given the time already invested.

## The diagnostic chain

1. **T4 (Turing architecture) lacks full hardware support for `bf16`.** `ORPOConfig`'s validation explicitly rejects it (`transformers.training_args._validate_args`), unlike `SFTConfig`/`DPOConfig`, which never hit this check in this project. Fix: switch to `fp16`.
2. **`fp16` training via `Trainer`'s built-in mixed precision needs `GradScaler`**, which expects fp32 master weights. Loading the model directly in `fp16` broke `GradScaler` (`"Attempting to unscale FP16 gradients"`). Fix: load the model in fp32, let `Trainer` handle casting.
3. **That still hit the same `GradScaler` error** — traced to a second, independent cause: `gradient_checkpointing`'s activation recomputation during backward is a documented common source of conflicts with `GradScaler`/fp16. Fix attempt: disable `Trainer`'s own `fp16` flag entirely (no `GradScaler`), load the model directly in `fp16`.
4. **Training then completed without crashing, but every diagnostic metric (`Nll Loss`, `Log Odds Ratio`, `Rewards/chosen`, `Rewards/rejected`) was `nan`** from the very first evaluation, in *two separate attempts*: once starting from the raw base model (train loss briefly ~3.1e11 before collapsing), and once from Week 2's SFT checkpoint (ruling out "undertrained base model" as the sole cause). Root cause: removing `GradScaler` to dodge step 2/3's crash also removed the only protection against `fp16` numerical underflow/overflow — trading a hard crash for a silent `nan`.
5. **Final attempt: restore `GradScaler` (fp16=True, fp32 weights) and disable `gradient_checkpointing`** instead, to remove the conflict from the other side. This produced a genuine `CUDA out of memory` error at `batch_size=1` — without `gradient_checkpointing`'s memory savings, the model and activations no longer fit in the T4's 16 GB, even at the smallest possible batch size.

## The conclusion

`GradScaler` (needed to keep `fp16` numerically stable) and `gradient_checkpointing` (needed to fit in the T4's memory) are **mutually exclusive requirements on this specific hardware/library combination** — satisfying one breaks the other. Both are individually well-documented, real constraints, not implementation mistakes on our side; the intersection is what made this specific method+hardware pairing infeasible within the available time.

## What this is still worth, scientifically

- Confirms the theoretical claim that ORPO needs no separate reference model (memory pressure came entirely from precision/checkpointing tradeoffs, never from a second resident model — unlike DPO's genuine two-model OOM).
- A concrete, transferable lesson: `trl.experimental` APIs carry real risk beyond just "the interface might change" — this one had an unresolved precision/memory conflict on older (pre-Ampere) GPU hardware.
- Directly informs the Week 3 comparison table: ORPO's practical compute requirements, on this hardware generation, are effectively higher than DPO's despite the theory suggesting the opposite (no reference model to hold).

## What DPO and LoRA achieved instead (for contrast)
| Method | Result |
| :--- | :--- |
| LoRA (r=16) | 13.795 perplexity — beats baseline (13.92) and Week 2 full-FT (14.61) |
| DPO (1000 pairs) | Rewards/accuracy 55.4% → 61.9%, stable training, no NaN |
| ORPO | Not trainable to completion on this hardware within available time |
