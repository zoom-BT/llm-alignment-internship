# 🎯 Week 4: Defining the Research Topic

**Calendar:** 2026-08-17 (Mon) – 2026-08-21 (Fri), per the contract — the first week this internship has actually landed on-calendar since Week 1.

## 🎯 Objective (contract, Annex A — verbatim)
> "The objective of Week 4 is to transform a broad theme concerning artificial intelligence alignment in an African context into a precise research question that can reasonably be investigated during the remaining four weeks."

## 💡 Potential themes (contract, Annex A — verbatim list, "may include")
- [ ] differences in safety behavior between English, French, and African languages;
- [x] the effect of translation on model safety refusals; — **selected**, this is H1 of the final proposal (native vs. machine-translated DPO safety data)
- [ ] the effect of code-switching on model safety behavior;
- [ ] differences in model behavior when using African varieties of French or English;
- [ ] biases associated with African names, locations, professions, institutions, or social situations;
- [x] ~~hallucinations concerning African institutions, public figures, historical events, or local knowledge~~ — piloted first (44-question African vs. matched-control set, two models), result was statistically inconclusive in both directions (Fisher p=0.72–0.74); documented in `03_Experiments/Week4_Pilot_Results.md`, not carried forward as the main topic
- [ ] model calibration and honesty on underrepresented African topics;
- [ ] conflicts between general alignment norms and preferences expressed by local evaluators;
- [x] limitations of automatically translated safety benchmarks; — also folded into the selected topic (Related Work axis 1)
- [ ] disagreement between automatic evaluators and human evaluators familiar with the studied context;
- [ ] trade-offs between safety refusals and usefulness in low-resource languages.

**Selected:** *Translated Safety Alignment vs. Native — DPO on African Multi-Lingual Foundation Models* (deliberately Harmless-only, not combined with Honest — see `04_Weekly_Reports/Week_04_Research_Proposal.md`).

## ✅ Research-Topic Selection Criteria (contract, Annex A — verbatim) — "The selected topic shall:"
- [x] formulate a precise research question; — section 3
- [x] contain at least one testable hypothesis; — H1/H2/H3, section 4
- [x] clearly identify the models to be studied; — M1 AfriqueQwen3.5-4B-50Langs, M2 Qwen3.5-4B-Base, section 6
- [x] use legally accessible data; — UbuntuGuard/AfriHate/HealthBench-Africa/Uhura-TruthfulQA/IrokoBench, all CC BY 4.0 or open on HF, verified by URL before inclusion
- [x] include an evaluation metric or procedure; — RR%, Over-RR%, F1-AfriHate, section 9
- [x] include at least one baseline; — B1-B4, section 8
- [x] be feasible with the available computing resources; — QLoRA on Kaggle 2×T4, section 12
- [x] allow a complete initial experiment to run in less than twelve hours; — estimated <2h end-to-end, section 12
- [x] avoid complex human-data collection where possible; — pre-annotated benchmarks + 10% manual cross-check by the intern, no external annotators
- [x] contain an identifiable contribution, even where the contribution is limited in scope. — C1-C3, section 5

## 📥 Deliverables (contract, Annex A — verbatim) — "By the end of Week 4, the Intern shall submit a two- to three-page research proposal containing:"
- [x] a provisional title;
- [x] the research context;
- [x] the research question;
- [x] the hypothesis;
- [x] the expected contribution;
- [x] related work;
- [x] the selected models;
- [x] the datasets;
- [x] the evaluation metrics;
- [x] the baselines;
- [x] the experimental protocol;
- [x] the planned ablation studies;
- [x] the estimated computing requirements;
- [x] the main risks and limitations;
- [x] the schedule for Weeks 5 to 8;
- [x] the figures and tables expected to appear in the manuscript.

All 15 sections present in `04_Weekly_Reports/Week_04_Research_Proposal.md` (English submission version; French working draft kept alongside as `Balbino Research Proposal .md`).

**Approval gate (verbatim):** "The final research topic shall be approved by the Supervisor before the main experiments begin." — **[x] cleared 2026-08-25.** Proposal presented at this week's supervision meeting; approved with minor formatting requests only (no changes to scope, hypotheses, or protocol) — not blocking. See `00_Admin_&_Roadmap/Week5_Checklist.md` for the resulting schedule.

## 🔒 What Week 3 already tells us, going into topic selection
- **LoRA is the practical default** for any experiment in this project: better result than full fine-tuning (13.795 vs. 14.61 perplexity) *and* the smaller footprint — no reason to default to full fine-tuning for the actual research topic's experiments.
- **QLoRA and ORPO both hit real hardware limits on a single T4** (bf16 unsupported, GradScaler/gradient_checkpointing conflicts, GPU quota exhaustion mid-week) — the research topic's experimental design should assume similar constraints, not assume unlimited compute.
- **RLHF's full pipeline (RM + PPO) is likely out of budget** for an 4-week research phase; DPO is the realistic alignment-method choice if the topic needs one at all.
- These constraints argue for a topic that's evaluation/analysis-heavy (e.g. bias/hallucination/calibration measurement) rather than one requiring another full round of expensive training experiments, unless the topic specifically needs one.

## 👉 Bridge to Week 5
Week 5 starts finalizing the data pipeline and baselines for whatever topic is approved — the tighter and more concrete this week's proposal is, the less re-work Week 5 needs.
