# 🎯 Week 4: Defining the Research Topic

**Calendar:** 2026-08-17 (Mon) – 2026-08-21 (Fri), per the contract — the first week this internship has actually landed on-calendar since Week 1.

## 🎯 Objective (contract, Annex A)
Turn a broad theme in AI alignment in an African context into a **precise, feasible research question** for the remaining 4 weeks (Weeks 5-8).

## 💡 Candidate themes (contract's own list — not yet narrowed down, needs a dedicated discussion)
- Differences in safety behavior between English, French, and African languages
- Effect of translation on model safety refusals
- Effect of code-switching on model safety behavior
- Differences in model behavior with African varieties of French/English
- Biases tied to African names, locations, professions, institutions, social situations
- Hallucinations about African institutions, public figures, historical events, local knowledge
- Model calibration/honesty on underrepresented African topics
- Conflicts between general alignment norms and local evaluator preferences
- Limitations of automatically translated safety benchmarks
- Disagreement between automatic evaluators and human evaluators familiar with the context
- Trade-offs between safety refusals and usefulness in low-resource languages

**Not selected yet** — this needs its own focused conversation (motivations, what's genuinely feasible with a 0.5-1B-class model and no dedicated human-annotation budget), not a unilateral pick. First Monday task.

## ✅ Selection criteria (contract, Annex A) — the topic must satisfy all of these
- [ ] Precise research question
- [ ] At least one testable hypothesis
- [ ] Clearly identified models
- [ ] Legally accessible data
- [ ] An evaluation metric or procedure
- [ ] At least one baseline
- [ ] Feasible with available computing resources
- [ ] A complete initial experiment runs in under 12 hours
- [ ] Avoids complex human-data collection where possible
- [ ] An identifiable contribution, even if limited in scope

## 📥 Deliverables (contract, Annex A)
A 2-3 page research proposal containing:
- [ ] Provisional title
- [ ] Research context
- [ ] Research question
- [ ] Hypothesis
- [ ] Expected contribution
- [ ] Related work
- [ ] Selected models
- [ ] Datasets
- [ ] Evaluation metrics
- [ ] Baselines
- [ ] Experimental protocol
- [ ] Planned ablation studies
- [ ] Estimated computing requirements
- [ ] Main risks and limitations
- [ ] Schedule for Weeks 5-8
- [ ] Figures/tables expected in the final manuscript

**Approval gate:** the final topic must be approved by the Supervisor before Week 5's main experiments begin — flag this explicitly at this week's supervision meeting, don't just proceed unilaterally.

## 🔒 What Week 3 already tells us, going into topic selection
- **LoRA is the practical default** for any experiment in this project: better result than full fine-tuning (13.795 vs. 14.61 perplexity) *and* the smaller footprint — no reason to default to full fine-tuning for the actual research topic's experiments.
- **QLoRA and ORPO both hit real hardware limits on a single T4** (bf16 unsupported, GradScaler/gradient_checkpointing conflicts, GPU quota exhaustion mid-week) — the research topic's experimental design should assume similar constraints, not assume unlimited compute.
- **RLHF's full pipeline (RM + PPO) is likely out of budget** for an 4-week research phase; DPO is the realistic alignment-method choice if the topic needs one at all.
- These constraints argue for a topic that's evaluation/analysis-heavy (e.g. bias/hallucination/calibration measurement) rather than one requiring another full round of expensive training experiments, unless the topic specifically needs one.

## 👉 Bridge to Week 5
Week 5 starts finalizing the data pipeline and baselines for whatever topic is approved — the tighter and more concrete this week's proposal is, the less re-work Week 5 needs.
