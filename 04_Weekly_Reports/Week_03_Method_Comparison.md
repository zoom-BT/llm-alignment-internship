# Week 3 — Method Comparison Tables

## 1. Alignment methods: SFT, RLHF family, DPO family, AI feedback

| Method | Feedback type | Reference model? | Explicit reward model? | Online/offline | Key idea | Compute cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SFT** | Demonstrations | No | No | Offline | Standard causal LM cross-entropy on human-written ideal responses | Low |
| **RLHF** (framework) | Pairwise preferences → RM → RL | Yes (KL penalty) | Yes (trained separately) | Online (policy generates during training) | General 3-stage pipeline: SFT → reward model → RL fine-tuning | High (3 stages, 2 resident models during RL) |
| **PPO** | (via RLHF's reward model) | Yes | Yes (external, from RLHF stage 2) | Online | Clipped surrogate objective + KL penalty against the SFT policy; actor-critic (learned value function baseline) | High — policy + value + reward + reference model |
| **REINFORCE** | (via a reward signal) | Optional | Depends on setup | Online | Base policy-gradient theorem: `∇J = E[∇log π(y\|x)·R(x,y)]`; high variance without a baseline | Low algorithmically, but noisy — needs many samples |
| **RLOO** | (via a reward signal) | Optional (KL penalty optional) | Depends on setup | Online | REINFORCE + leave-one-out baseline from K samples of the same prompt — no learned critic needed | Medium — no value network, but K generations per prompt |
| **GRPO** | (via a reward signal, often verifiable) | Yes (KL penalty) | Optional (often rule-based/verifiable) | Online | Like RLOO but normalizes advantage by group mean **and** std; keeps PPO's clipping | Medium — no critic, but K generations per prompt |
| **DPO** | Pairwise preferences (chosen/rejected) | Yes | No (implicit, via the policy itself) | Offline | Closed-form optimal-policy substitution turns the RM's Bradley-Terry loss into a loss on `β·log(π/π_ref)` directly | Medium — 2 model copies (policy + frozen reference) |
| **KTO** | Independent binary labels (desirable/undesirable, **not paired**) | Yes | No | Offline | Inspired by prospect theory (loss aversion — humans weight losses more than equivalent gains); works when only thumbs-up/down feedback exists, no explicit A-vs-B comparisons | Medium — still needs a reference model |
| **ORPO** | Pairwise preferences | **No** | No | Offline | `L_SFT + λ·L_OR`, odds-ratio loss computed entirely from the policy itself — SFT and preference optimization in one pass, one model | Low — single model, no reference copy |
| **SimPO** | Pairwise preferences | **No** | No | Offline | Reference-free like ORPO, but no SFT term either — uses length-normalized sequence log-probability directly as the implicit reward, plus a target reward margin | Low — single model |
| **RLAIF** | AI-generated preferences | Yes (same as RLHF) | Yes (AI-generated labels feed a trained RM, or an LLM judge is used directly) | Online or offline depending on setup | Same as RLHF, but an AI model replaces human labelers — cheaper to scale, but risks reproducing the judge model's own biases/errors | Same as RLHF, plus judge-model inference cost |
| **Constitutional AI** | Written principles + AI self-critique | Optional | No (self-generated via critique/revision) | Offline (SFT phase) then online/offline (RL phase) | Model critiques and revises its own outputs against a written "constitution", then trains on the revised outputs (and/or uses the same mechanism to generate preference pairs for RLAIF) | Medium — critique/revision passes add inference cost |

**Our own experiments this week, for direct grounding:**
- **SFT** — Weeks 1-2, full fine-tuning, corrected recipe: 14.61 perplexity.
- **DPO** — small run (1000 pairs, `ultrafeedback_binarized`), stable training, `Rewards/accuracy` 55.4% → 61.9%.
- **ORPO** — attempted, documented as an honest negative result (`Week_03_ORPO_Negative_Result.md`): `GradScaler` (needed for fp16 stability) and `gradient_checkpointing` (needed to fit the T4's memory) turned out mutually exclusive on this hardware/library combination.

## 2. Parameter-update methods: full fine-tuning vs. LoRA vs. QLoRA

| Method | Trainable params | GPU memory | Training time | Storage | Risk of forgetting |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Full fine-tuning** | 100% (~495M) | Highest (weights + gradients + AdamW state for every parameter) | Baseline | ~1GB checkpoint | Higher — every parameter can drift from pretrained values |
| **LoRA** (r=16, Q/V only) | 0.22% (1,081,344) | Much lower — frozen base needs no gradient/optimizer state | Comparable per-step, but usually converges from a cheaper starting point | A few MB (adapter only) | Lower — most of the pretrained model stays untouched |
| **QLoRA** (r=16, NF4) | 0.22% (identical to LoRA — quantization affects the frozen base's storage, not what's trainable) | Lowest — frozen base stored in 4-bit | **Slower per step** (on-the-fly dequantization overhead) | Smallest (4-bit base + small adapter) | Lower (same as LoRA), but the frozen base itself carries some precision loss |

**Our own results:**

| | Perplexity (Dolly-15k test, 1502 examples) |
| :--- | :--- |
| Baseline (no fine-tuning) | 13.92 |
| Week 1 full fine-tuning (broken hyperparameters) | 75.41 |
| Week 2 full fine-tuning (corrected) | 14.61 |
| **LoRA (r=16)** | **13.795** — best result of the project, beats the baseline |
| **QLoRA (r=16, NF4)** | 16.84 — worse than LoRA, consistent with the training-time validation loss gap (~2.432 vs. ~2.255) |

**Interpretation:** LoRA's constrained update (0.22% of parameters) preserved the base model's general language-modeling ability better than full fine-tuning did, even after Week 2's careful hyperparameter correction — a small, concrete illustration of the "risk of forgetting" comparison axis the contract asks about. QLoRA's 4-bit compression of the frozen base cost some of that precision back, in exchange for an even smaller memory footprint — a tradeoff that matters far more at larger model scales than at 0.5B, where LoRA already fits comfortably without quantization.
