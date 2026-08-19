# 🎯 Week 4: Defining the Research Topic

**Calendar:** 2026-08-17 (Mon) – 2026-08-21 (Fri), per the contract — the first week this internship has actually landed on-calendar since Week 1.

## 🎯 Objective (contract, Annex A — verbatim)
> "The objective of Week 4 is to transform a broad theme concerning artificial intelligence alignment in an African context into a precise research question that can reasonably be investigated during the remaining four weeks."

## 💡 Potential themes (contract, Annex A — verbatim list, "may include") — not yet narrowed down, needs a dedicated discussion
- [ ] differences in safety behavior between English, French, and African languages;
- [ ] the effect of translation on model safety refusals;
- [ ] the effect of code-switching on model safety behavior;
- [ ] differences in model behavior when using African varieties of French or English;
- [ ] biases associated with African names, locations, professions, institutions, or social situations;
- [ ] hallucinations concerning African institutions, public figures, historical events, or local knowledge;
- [ ] model calibration and honesty on underrepresented African topics;
- [ ] conflicts between general alignment norms and preferences expressed by local evaluators;
- [ ] limitations of automatically translated safety benchmarks;
- [ ] disagreement between automatic evaluators and human evaluators familiar with the studied context;
- [ ] trade-offs between safety refusals and usefulness in low-resource languages.

**Not selected yet** — this needs its own focused conversation (motivations, what's genuinely feasible with a 0.5-1B-class model and no dedicated human-annotation budget), not a unilateral pick. First Monday task.

## ✅ Research-Topic Selection Criteria (contract, Annex A — verbatim) — "The selected topic shall:"
- [ ] formulate a precise research question;
- [ ] contain at least one testable hypothesis;
- [ ] clearly identify the models to be studied;
- [ ] use legally accessible data;
- [ ] include an evaluation metric or procedure;
- [ ] include at least one baseline;
- [ ] be feasible with the available computing resources;
- [ ] allow a complete initial experiment to run in less than twelve hours;
- [ ] avoid complex human-data collection where possible;
- [ ] contain an identifiable contribution, even where the contribution is limited in scope.

## 📥 Deliverables (contract, Annex A — verbatim) — "By the end of Week 4, the Intern shall submit a two- to three-page research proposal containing:"
- [ ] a provisional title;
- [ ] the research context;
- [ ] the research question;
- [ ] the hypothesis;
- [ ] the expected contribution;
- [ ] related work;
- [ ] the selected models;
- [ ] the datasets;
- [ ] the evaluation metrics;
- [ ] the baselines;
- [ ] the experimental protocol;
- [ ] the planned ablation studies;
- [ ] the estimated computing requirements;
- [ ] the main risks and limitations;
- [ ] the schedule for Weeks 5 to 8;
- [ ] the figures and tables expected to appear in the manuscript.

**Approval gate (verbatim):** "The final research topic shall be approved by the Supervisor before the main experiments begin." — flag this explicitly at this week's supervision meeting, don't just proceed unilaterally.

## 🔒 What Week 3 already tells us, going into topic selection
- **LoRA is the practical default** for any experiment in this project: better result than full fine-tuning (13.795 vs. 14.61 perplexity) *and* the smaller footprint — no reason to default to full fine-tuning for the actual research topic's experiments.
- **QLoRA and ORPO both hit real hardware limits on a single T4** (bf16 unsupported, GradScaler/gradient_checkpointing conflicts, GPU quota exhaustion mid-week) — the research topic's experimental design should assume similar constraints, not assume unlimited compute.
- **RLHF's full pipeline (RM + PPO) is likely out of budget** for an 4-week research phase; DPO is the realistic alignment-method choice if the topic needs one at all.
- These constraints argue for a topic that's evaluation/analysis-heavy (e.g. bias/hallucination/calibration measurement) rather than one requiring another full round of expensive training experiments, unless the topic specifically needs one.

## 👉 Bridge to Week 5
Week 5 starts finalizing the data pipeline and baselines for whatever topic is approved — the tighter and more concrete this week's proposal is, the less re-work Week 5 needs.
