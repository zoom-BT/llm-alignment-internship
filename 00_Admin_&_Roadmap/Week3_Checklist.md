# 🎯 Week 3: Alignment, Preference Learning, and Efficient Fine-Tuning

**⚠️ Schedule note:** per the contract, Week 3 runs 2026-08-10 to 2026-08-14. We're starting the practical work on 2026-08-14 (Week 2's InstructGPT deep-dive ran long) — flagged at the supervision meeting (Article 3 permits deadline adjustment for justified reasons). This checklist covers the full contract scope, triaged by priority so the essentials land even if the full 10-method survey doesn't fit.

## 📥 Deliverables Checklist (contract, Annex A)
- [x] ~~Comparison table: SFT, RLHF, PPO, RLOO, GRPO, DPO, KTO, ORPO, SimPO, RLAIF, Constitutional AI~~ — `04_Weekly_Reports/Week_03_Method_Comparison.md`
- [x] ~~Comparison: full fine-tuning vs. LoRA vs. QLoRA~~ — same file, section 2
- [x] Reading notes on the main methods studied — done for ~~LoRA, QLoRA, DPO, ORPO~~ (`06_Reading_Notes/`) and ~~PPO/RLHF~~ (via `InstructGPT.md`); **not done** for RLOO, GRPO, KTO, SimPO, RLAIF, Constitutional AI as standalone notes (covered conceptually in the comparison table and in conversation, not as dedicated per-paper notes)
- [x] ~~Code + configs for implemented experiments~~ — `src/train.py` (`run_sft` w/ LoRA+QLoRA, `run_dpo`, `run_orpo`) + 3 notebooks
- [x] ~~Short experimental report (results + failure cases)~~ — `Week_03_Method_Comparison.md` + `Week_03_ORPO_Negative_Result.md`
- [ ] ~20-minute oral presentation on method families + relevance to the future research project

## 📚 Theoretical Concepts Matrix (contract, Annex A §1-8)
- [x] ~~Sources of alignment feedback (demonstrations, pairwise preferences, binary, rankings, critiques, human/AI/rule-based/verifiable)~~ — via InstructGPT's data-collection sections
- [x] ~~SFT limitations (learning only from positive demonstrations)~~ — via InstructGPT + our own Week 1/2 results
- [ ] Rejection sampling / reward-ranked fine-tuning (RAFT) — not covered
- [x] ~~Pairwise reward models~~ — via InstructGPT's RM section (loss formula, Bradley-Terry)
- [x] ~~Outcome vs. process reward models~~ — ORM vs. PRM, tied to "Let's Verify Step by Step"
- [x] ~~Evaluator limitations: position bias, length bias, reward hacking~~ — reward hacking via InstructGPT's alignment-tax discussion; position/verbosity/self-preference bias covered separately
- [x] ~~RL for LMs: policy/trajectory/reward framing, KL regularization, reference model~~ — via InstructGPT's PPO section
- [x] ~~PPO vs. REINFORCE vs. RLOO vs. GRPO~~ — policy gradient theorem, baseline subtraction, leave-one-out, group-normalized advantage, all derived
- [x] DPO family: ~~DPO, KTO, ORPO, SimPO~~ (DPO and ORPO in depth with implementation; KTO and SimPO conceptually only, in the comparison table) — **IPO, SLiC-HF not covered**
- [x] ~~AI feedback / Constitutional AI / RLAIF~~ — mechanics and risks (judge bias reproduction) covered conceptually
- [x] Full FT vs. ~~adapters vs.~~ prefix/prompt tuning vs. ~~LoRA vs. QLoRA~~ — full FT/LoRA/QLoRA covered in depth (theory + implementation + results); **adapters and prefix/prompt tuning not covered**
- [x] ~~Alignment failure modes: sycophancy, excessive/insufficient refusal, preference overfitting, response-diversity loss~~ — covered with definitions and examples

## 🔧 Practical Work (contract, Annex A) — triaged

**Must-do (explicitly required, feasible on a single Kaggle T4):**
1. ~~SFT experiment using LoRA~~ — done: 13.795 perplexity, beats baseline and Week 2 full-FT
2. ~~Small DPO experiment on paired preference data~~ — done: `ultrafeedback_binarized`, 1000 pairs, Rewards/accuracy 55.4%→61.9%
3. ~~One additional preference method — ORPO~~ — attempted, **documented as an honest negative result** (`Week_03_ORPO_Negative_Result.md`), not a completed working run
4. ~~Compare ≥2 parameter-update methods~~ — done, all 3: full FT (14.61) vs. LoRA (13.795) vs. QLoRA (16.84)
5. Failure-case analysis on the new runs — done for ~~ORPO~~ (full negative-result writeup) and ~~DPO~~ (qualitative SFT-vs-DPO comparison, 3 prompts); **not done** as a full 20-example-style review (Week 2's depth) for LoRA/QLoRA outputs specifically

**If time permits (contract's own wording, lowest priority):**
6. One evaluator beyond the RM already studied — **theory covered** (LLM-as-judge mechanics/biases), **not implemented in code**
7. A small GRPO/RLOO/REINFORCE reproduction — **theory/math covered**, **not run in code**

## 🔒 Protocol
Same base model (Qwen2.5-0.5B), same dataset family (Dolly-15k) for continuity with Week 1/2's numbers, unless a method specifically requires paired preference data (DPO/ORPO used `ultrafeedback_binarized` instead, documented explicitly).

## 👉 Bridge to Week 4
Week 4 is topic selection — Week 3's method comparisons (SFT vs LoRA vs QLoRA vs DPO vs ORPO) directly inform what's computationally realistic for the actual research project. Notably: LoRA outperforming full fine-tuning, and QLoRA/ORPO's practical hardware constraints on a T4, are both concrete data points for scoping Week 4's proposal.
