# Direct Preference Optimization: Your Language Model Is Secretly a Reward Model

- **Link:** arXiv:2305.18290 (Rafailov et al., 2023)
- **Read on:** 2026-08-18

## Problem
RLHF (as in InstructGPT) needs 3 separate stages — SFT, a separately-trained reward model, and RL (PPO) — each with its own infrastructure, and RL training is notoriously unstable. Can preference alignment skip the reward model and the RL loop entirely?

## Method
Start from the closed-form optimal policy for the KL-regularized RLHF objective: `π*(y|x) = π_ref(y|x)·exp(r(x,y)/β) / Z(x)`. Rearranging for `r`: `r(x,y) = β·log(π*(y|x)/π_ref(y|x)) + β·log Z(x)`. Substituting this into the reward model's Bradley-Terry loss, the `Z(x)` term cancels in the `chosen − rejected` difference (it depends only on `x`) — leaving a loss computable directly from the policy and a frozen reference copy, no separate reward model needed at all.

## Loss / Objective
```
L_DPO(θ) = −E[log(σ(β·log(πθ(yw|x)/π_ref(yw|x)) − β·log(πθ(yl|x)/π_ref(yl|x))))]
```
Same Bradley-Terry structure as the RM's own loss, with the "reward" replaced by a log-probability ratio against a frozen reference.

## Compute Budget
Needs **two full model copies resident in memory** during training (trainable policy + frozen reference) — this is what caused our first CUDA OOM on the DPO run, fixed by reducing `batch_size` to 2 and enabling `gradient_checkpointing`.

## Key Results
Our own small experiment (1000 pairs from `ultrafeedback_binarized`, starting from Week 2's SFT checkpoint): stable training, no NaN, `Rewards/accuracy` improved from 55.4% to 61.9% over 59 steps — a real, if modest (small dataset), preference-learning signal.

## Limitations
- Needs a reasonably capable starting policy (`π_ref`) — not designed to teach instruction-following from scratch.
- The two-model memory requirement is a real, non-trivial cost at scale.
- Like RLHF, only as good as the preference data's representativeness — the same "who are we aligning to" question from InstructGPT applies equally here.

## Takeaway
DPO's core trick — substituting the closed-form optimal policy back into the reward loss — turns an entire RL training loop into a single, DPOTrainer-style supervised-learning-shaped step. Implemented in `run_dpo()`, and empirically it worked cleanly on the first correctly-configured attempt, in contrast to ORPO's cascading environment issues.
