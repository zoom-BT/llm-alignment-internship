# Week 4 — Hallucination Pilot: Results and Analysis

Full grading of `notebooks/pilot_results.json` (both models, all 44 questions) against the sourced ground truth in `pilot_questions.json`. Each answer graded as **correct**, **wrong-and-confident** (hallucination), or **vague-hedge** (declines to answer — not a hallucination, per the TruthfulQA-style distinction the pilot notebook set out to use). Hedges count as "not correct" for the accuracy tally below, but are kept separate from confident wrong answers in the failure-mode notes.

## Scores

| Model | African accuracy | Control accuracy | Gap |
|---|---|---|---|
| Gemma-4-E2B-it | 17/22 (77.3%) | 15/22 (68.2%) | +9.1 pp, **Africa higher** |
| Qwen2.5-3B-Instruct | 16/22 (72.7%) | 18/22 (81.8%) | −9.1 pp, **Control higher** |

**Correction:** an earlier informal count (before this pilot's results file existed in full) had reported Gemma as 16/22 African vs. 17/22 control. That was wrong — re-grading directly against `pilot_questions.json`'s `ground_truth` field gives 17/22 vs. 15/22, the opposite direction. This file is now the authoritative grading; the earlier number should not be cited.

## Statistical test

Fisher's exact test on each model's 2×2 table (correct/wrong × Africa/control):

- Gemma: `[[17,5],[15,7]]` → p = 0.74
- Qwen: `[[16,6],[18,4]]` → p = 0.72

Neither gap is remotely significant. With 22 items per cell, a single flipped answer moves the accuracy by 4.5 points — the pilot has essentially no power to detect anything short of a very large effect.

## Reading the result

**The hypothesis is not supported by this pilot.** Two models, tested independently, disagree on which group hallucinates more, and neither disagreement clears the bar of chance. This is a genuine negative-but-informative result, not a shortfall: it tells us the *pilot's* job — checking the pipeline works and the questions are answerable and gradeable — succeeded, but the pilot was never sized to test the hypothesis itself (22 items/group was chosen for a same-day feasibility check, not for statistical power).

**A cross-model, cross-region failure pattern worth carrying into the full proposal:** both models repeatedly substitute a national head of state for the leader of a *regional organization* — Gemma answered "Ahmadou Ahidjo" (Cameroon's president) for OAU's first Secretary-General; Qwen answered "Jomo Kenyatta" (Kenya's president) for the same question, and "Suharto" (Indonesia's president) for ASEAN's first Secretary-General. This role-confusion error appeared in both the African and the control question of the same category, on both models — a candidate generic failure mode (organizational-role vs. head-of-state conflation) independent of region, and a concrete thing a full-scale study could test for specifically rather than only measuring raw accuracy.

## What this means for the full Week 4 proposal

- Do not cite a directional hallucination gap as a finding — there isn't one yet, in either direction.
- If hallucination/calibration on African topics remains the chosen theme, the proposal's power analysis needs to size the question set well beyond 44 (order of magnitude more, or a paired/bootstrap design) before a gap of this size could be distinguished from noise.
- The role-confusion pattern is a legitimate secondary finding to mention as motivation for a more structured error taxonomy in the full study, not as evidence of a regional gap.
