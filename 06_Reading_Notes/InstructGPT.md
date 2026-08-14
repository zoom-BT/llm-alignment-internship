# Training language models to follow instructions with human feedback (InstructGPT)

- **Link:** arXiv:2203.02155 (Ouyang et al., 2022)
- **Read on:** 2026-08-05 – 2026-08-14 (section-by-section, with supervisor-defense-level detail on the formulas)

## Problem

Pretrained LMs optimize next-token prediction on internet text — a proxy objective different from what users actually want ("follow my instruction, helpfully and safely"). This gap is **misalignment**. Desired behavior is defined via the **HHH framework** (Helpful, Honest, Harmless — Askell et al., 2021).

## Method

Three-step pipeline, all starting from a single pretrained **GPT-3** checkpoint (Brown et al., 2020), tested at 3 sizes (1.3B / 6B / 175B):

1. **SFT** — fine-tune GPT-3 on labeler-written demonstrations (supervised, causal LM loss). 16 epochs, cosine LR decay, dropout 0.2. Model selection by RM score on validation, not validation loss (loss overfits after 1 epoch, but RM score/human preference keep improving).
2. **Reward Model (RM)** — SFT model with final unembedding layer swapped for a scalar output. Trained on labeler **rankings** of K=4–9 responses per prompt (→ C(K,2) pairwise comparisons per prompt, batched together per-prompt for efficiency and to avoid overfitting from correlated pairs). Only 6B RMs used (175B unstable, less suited as PPO's value function).
3. **RL (PPO)** — SFT model fine-tuned via PPO in a single-step "bandit" environment (1 prompt → 1 response → reward from RM → done), with a per-token **KL penalty** vs. the frozen SFT model (prevents reward hacking). Value function initialized from the RM. `PPO-ptx` variant mixes in a pretraining-data log-likelihood term to fix the alignment tax; "InstructGPT" = PPO-ptx by default.

**Data:** 3 distinct datasets — SFT (~13k prompts), RM (~33k), PPO (~31k) — sourced mostly from real OpenAI API/Playground traffic (bootstrapped: the very first SFT model was trained entirely on labeler-written prompts+answers, since no instruction-following model existed yet to generate real traffic). ~40 contractors (Upwork/ScaleAI), screened, inter-annotator agreement ~73% (held-out labelers: 77%). Baselines compared: SFT, GPT-3, GPT-3 few-shot-prompted, and GPT-3 fine-tuned on FLAN/T0 (~1M examples each — still underperform SFT's 13k, proving *quality of human feedback* beats *volume of academic instruction data*).

## Loss / Objective

**RM loss** (Bradley-Terry pairwise ranking loss):
```
loss(θ) = −(1/C(K,2)) · E_(x,yw,yl)~D [ log(σ(rθ(x,yw) − rθ(x,yl))) ]
```
Equivalent to `σ(rw−rl) = e^rw/(e^rw+e^rl)` — the classic Bradley-Terry win-probability form (chess/sports ranking). Normalized post-hoc so labeler demonstrations score 0 on average (loss is shift-invariant, so this fixes an otherwise arbitrary reference point).

**PPO objective:**
```
objective(φ) = E_(x,y)~π_RL [ rθ(x,y) − β·log(π_RL(y|x)/π_SFT(y|x)) ] + γ·E_x~D_pretrain [ log(π_RL(x)) ]
```
Reward from the RM, minus a KL-divergence penalty against the frozen SFT policy (the `β` term — keeps the model from exploiting RM blind spots), plus an optional pretraining-mix term (`γ`, PPO-ptx only) that is literally the standard causal LM log-likelihood computed on pretraining-distribution text.

## Compute Budget

| Model | Compute |
| :--- | :--- |
| SFT-175B | 4.9 petaflops/s-days |
| PPO-ptx-175B | 60 petaflops/s-days |
| GPT-3 pretraining (reference) | 3,640 petaflops/s-days |

Even the most expensive alignment technique here (PPO-ptx) costs **~1.6%** of pretraining — yet beats a 100x model-size increase in human preference. Headline conclusion: aligning existing models is currently more cost-effective than training bigger ones.

## Key Results

- 1.3B InstructGPT **preferred over 175B GPT-3** (same architecture — only training differs)
- 175B InstructGPT preferred 85±3% vs. raw GPT-3, 71±4% vs. few-shot GPT-3
- TruthfulQA: ~2x more truthful/informative answers; with permission to abstain ("I have no comment"), PPO models use it appropriately instead of confidently guessing — a calibration win, not just a knowledge win
- Toxicity: ~-25%, but **only when explicitly prompted to be respectful** — no default improvement without that instruction
- No improvement on bias (Winogender/CrowS-Pairs, entropy-based metric) — and the entropy metric itself conflates "more decisive" with "more biased," a limitation the authors flag themselves
- Alignment tax (SQuAD/DROP/HellaSwag/WMT regressions) — largely, not fully, mitigated by PPO-ptx
- Generalizes to non-English and code instructions despite <5% representation in fine-tuning data
- **Counter-intuitive finding:** on the API-distribution hallucination metric, plain SFT actually hallucinates *less* than PPO/PPO-ptx — plausibly because SFT imitates human-written (grounded) demonstrations directly, while PPO explores freely against an imperfect RM that may reward "sounding complete" over strict factuality (reward hacking)

**Cross-check against our own Week 2 work (Qwen2.5-0.5B, SFT only, no RLHF):** our 20-example qualitative review (2026-08-05/06) independently reproduced two of this paper's core findings at a tiny scale — (1) style learned without knowledge gained (our "House Tyrell" example: correct terse-motto *format*, wrong *fact* — same pattern as InstructGPT's style-vs-knowledge distinction), and (2) repetition/degeneration failure modes reduced but not eliminated by better training (our test perplexity, 14.61, stayed above the 13.92 baseline — partly explained by residual degenerate completions, structurally similar to InstructGPT's own "still makes simple mistakes" section).

## Limitations

- **Whose preferences?** Aligned to ~40 English-speaking, US/Southeast-Asia contractors, themselves guided by instructions written by OpenAI researchers, sourced from a non-representative customer base (API access originally waitlist-seeded from OpenAI's own employee network). Not a claim that this is "the right" reference group — just a demonstration that *a* group can be aligned to.
- **Not fully safe:** still hallucinates, still produces toxic/biased/sexual/violent content without explicit prompting. Most serious: **follows harmful instructions too readily** — prompted to be "maximally biased," InstructGPT generates *more* toxic output than equivalently-sized raw GPT-3. Better instruction-following ≠ better safety when the user's intent itself is harmful.
- **Methodological:** most comparisons labeled by only 1 contractor (no disagreement signal); averaging preferences may erase the views of groups disproportionately affected by a given output.
- Excessive hedging, blindness to false premises, and degradation under many simultaneous constraints all persist post-alignment.

## Takeaway

RLHF (SFT → RM → PPO) is a **cheap, empirically validated way to reshape a pretrained model's behavior/style** toward a specific reference group's preferences — it does not add new world knowledge, and it does not resolve *who* the target preferences should belong to, nor guarantee safety against a malicious user. It is directly the template our own `run_sft()` implements (step 1 of 3), and a preview of what an eventual `run_dpo()` (already stubbed in `src/train.py`) would extend toward — DPO being a more modern, RL-free way of reaching a similar preference-alignment goal without training a separate reward model.
