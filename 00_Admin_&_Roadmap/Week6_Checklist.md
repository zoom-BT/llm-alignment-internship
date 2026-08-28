# 🎯 Week 6: Main Experiments

**Calendar:** 2026-08-31 (Mon) – 2026-09-04 (Fri) per the contract. Tasks are tracked against this nominal calendar regardless of which day the work actually gets done — see [[Week5_Checklist.md]] for what carries over.

## 🎯 Objective (contract, Annex A — verbatim)
> "WEEK 6: MAIN EXPERIMENTS — During Week 6, the Intern shall execute the central experiments required to test the research hypothesis. The Intern shall: modify only one major experimental variable at a time where reasonably possible; use consistent datasets and metrics across comparisons; record all random seeds; use multiple random seeds where computationally feasible; retain essential checkpoints and configuration files; document failed and interrupted experiments; inspect individual examples in addition to aggregate metrics; verify that any apparent improvement does not result from data leakage; compare the results with the base model and the selected baselines."

## ⏮️ Carried over from Week 5 — all four blocked on the same first GPU session
- [ ] evaluate the selected models without modification; — B1 (AfriqueQwen-Raw) and Qwen3.5-4B-Base on the guardian task
- [ ] establish baseline performance;
- [ ] estimate the computing time, memory requirements, and financial cost where applicable;
- [ ] verify that interrupted experiments can resume from checkpoints.

Plus the two Week 5 deliverables that depend on them: baseline results, and an initial version of the main results table.

## ✅ Tasks (contract, verbatim) — mapped to this topic
- [ ] modify only one major experimental variable at a time where reasonably possible; — B3 vs B4 differ **only** in the backbone (Qwen-Base vs AfriqueQwen); same data, same hyperparameters, same seed. That single-variable design is what makes H2 attributable
- [ ] use consistent datasets and metrics across comparisons; — every arm scored on the same held-out slice with the same guardian macro F1; the English control uses the same axis filter as the African slice
- [ ] record all random seeds; — `config.yaml` `training.seed`, and the split seed it derives (`split_three_way` uses `seed` and `seed + 1`)
- [ ] use multiple random seeds where computationally feasible; — at minimum 3 seeds for B3/B4, since the whole claim is a difference between them and a one-seed difference is not evidence
- [ ] retain essential checkpoints and configuration files; — LoRA adapters only (tens of MB, not GB), plus the exact `config.yaml` per run
- [ ] document failed and interrupted experiments; — continue the D-series in `03_Experiments/Week5_Deviations_From_Proposal.md` or open a Week 6 experiment log
- [ ] inspect individual examples in addition to aggregate metrics; — the eval writes `records_*.jsonl` with every raw completion for exactly this; read the English-control rows by hand
- [ ] verify that any apparent improvement does not result from data leakage; — already enforced in code at `base_stem` level and verified at zero; re-verify per run rather than assuming it holds
- [ ] compare the results with the base model and the selected baselines. — B1/B3/B4, paired via McNemar (`src/metrics.py`), not an unpaired test

## 📥 Deliverables (contract, verbatim)
- [ ] the experimental scripts; — `src/run_guardian_eval.py` exists; the judge/agent training entry point still needs writing
- [ ] the configuration files;
- [ ] the training and evaluation curves; — `save_training_curves` in `src/train.py`
- [ ] the result tables;
- [ ] qualitative examples; — from `records_*.jsonl`, English control first since those are readable
- [ ] the experiment log;
- [ ] a summary of the provisional conclusions.

## 📅 Order of work

The sequencing matters: it is built so that a result exists even if the week runs short on compute.

| Step | What | Why in this order |
| :---- | :---- | :---- |
| 1 | Smoke test, `--limit 20`, both backbones | Costs two minutes. Reveals whether a base model follows the answer format at all, and whether `DPOTrainer` accepts a `qwen3_5` multimodal checkpoint — both unknowns that would otherwise surface mid-run |
| 2 | Train the compliance judge on the judge slice (Qwen-Base) | Self-contained, and its macro F1 is a publishable result on its own. Everything downstream is bounded by this number |
| 3 | Measure the judge: African slice, English control, per language | Produces the instrument's stated precision, per `Judge_Validation_Protocol.md` |
| 4 | B1 baseline | Closes the four carried-over Week 5 tasks |
| 5 | B3 and B4 DPO runs, ≥3 seeds | The actual H2 comparison |
| 6 | Evaluate both on the Honest **and** Harmless axes | D9's cross-axis transfer question |

## ⚠️ Known risks going in
- **`DPOTrainer` on a multimodal checkpoint.** Both backbones are `model_type: qwen3_5` with a `vision_config`. `AutoModelForCausalLM` maps to the text-only variant, but TRL's behaviour on such a checkpoint is untested here. Step 1 exists to find out cheaply.
- **A base model may not follow the answer format.** `Qwen3.5-4B-Base` is not instruction-tuned. If the unparseable-output rate is high, the judge needs an SFT pass on the response format before DPO. The eval warns above 20%.
- **Transformers version on the Kaggle image.** `qwen3_5` needs >= 5.12.1; older images fail to load the model outright. `pip install -U transformers` first.
- **Internet must be enabled** in the notebook settings — Kaggle's model entries are pointers to Hugging Face, not offline copies. An `HF_TOKEN` in Kaggle Secrets avoids rate limiting.

## 🧭 Still open, and not GPU-blocked
- [ ] Send the drafted email to UbuntuGuard's corresponding author (licence confirmation, training split, label validation) — draft in `03_Experiments/Week5_Author_Email_DRAFT.local.md`, gitignored
- [ ] Verify **LSR** (Faruna 2026, arXiv:2603.19273) against its own source — a West African cross-lingual refusal-degradation benchmark found in the systematic review, absent from the dataset sheet
- [ ] AfriHate's exact per-language split sizes
- [ ] HealthBench-Africa's licence

## 👉 Bridge to Week 7
Week 7 (Robustness, Ablations, and Analysis) takes the A1 volume ablation — reachable at 100/200/868 now that the pair pool is 1,089 rather than the 401 first recorded — and the per-axis breakdown from D9.
