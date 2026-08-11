# Week 2 — Hyperparameter Table (Week 1 vs. Week 2 Corrected Recipe)

Same model (`Qwen/Qwen2.5-0.5B`), same dataset/split/seed, same `src/evaluate.py` — only `config.yaml`'s `training:` section changed. Full diff: `git log -p -- config.yaml` (commit `df1c337`).

| Hyperparameter | Week 1 | Week 2 | Why it changed |
| :--- | :--- | :--- | :--- |
| `learning_rate` | `2.0e-4` | `2.0e-5` | An order of magnitude lower. `2e-4` is a reasonable value for LoRA (only a small fraction of parameters updated), but too aggressive for *full* fine-tuning of all ~500M parameters — the leading suspect for Week 1's overfitting (13.92 → 75.41 perplexity). |
| `warmup_ratio` | *(unset — TRL default: 0)* | `0.03` | Ramps the learning rate up gradually over the first 3% of steps instead of applying the full rate from step 1, protecting the pretrained weights from a too-aggressive first update. |
| `lr_scheduler_type` | *(unset — TRL default: `linear`)* | `cosine` | Smooth cosine decay to 0 by the end of training, instead of a flat/linear rate throughout. |
| `eval_strategy` / `eval_steps` | *(unset — TRL default: `"no"`, meaning never)* | `"steps"` / `100` | Week 1 never computed a validation loss during training — overfitting was invisible until the final test-set number. Week 2 checks every 100 steps. |
| `load_best_model_at_end` / `metric_for_best_model` | *(unset — TRL default: `False` / `None`)* | `True` / `"eval_loss"` | At the end of training, restores the checkpoint with the lowest validation loss seen, not just whatever the last step happened to produce. |
| `early_stopping_patience` | *(no callback — trains the full fixed epoch count regardless)* | `3` (via `EarlyStoppingCallback`) | Stops training if validation loss hasn't improved for 3 consecutive evaluations, instead of committing to a fixed epoch count decided in advance. |
| `num_epochs` | `3` (fixed target) | `3` (ceiling only) | Same number, different role: Week 1 trained all 3 epochs unconditionally; Week 2 treats 3 as an upper bound and lets early stopping decide the real stopping point. |
| `batch_size` / `gradient_accumulation_steps` | `4` / `4` | `4` / `4` | Unchanged — not implicated in the overfitting diagnosis. |
| `gradient_checkpointing` | `true` | `true` | Unchanged. |
| `max_seq_length` | `512` | `512` | Unchanged — protocol requires it stay identical for a fair before/after comparison. |
| `precision` | `bf16` | `bf16` | Unchanged. |
| `seed` | `42` | `42` | Unchanged — same train/val/test split as Week 1. |

## Result of the change
| | Perplexity (test split, 1,502 examples) |
| :--- | :--- |
| Baseline (no fine-tuning) | 13.92 |
| Week 1 recipe | 75.41 |
| Week 2 recipe | 14.61 |

See [`Week_02_Error_Analysis.md`](Week_02_Error_Analysis.md) for the qualitative breakdown behind this number.
