# 🎯 Week 3: Alignment, Preference Learning, and Efficient Fine-Tuning

**⚠️ Schedule note:** per the contract, Week 3 runs 2026-08-10 to 2026-08-14. We're starting the practical work on 2026-08-14 (Week 2's InstructGPT deep-dive ran long) — to be flagged honestly at the next supervision meeting (Article 3 permits deadline adjustment for justified reasons). This checklist covers the full contract scope, triaged by priority so the essentials land even if the full 10-method survey doesn't fit.

## 📥 Deliverables Checklist (contract, Annex A)
- [ ] Comparison table: SFT, RLHF, PPO, RLOO, GRPO, DPO, KTO, ORPO, SimPO, RLAIF, Constitutional AI
- [ ] Comparison: full fine-tuning vs. LoRA vs. QLoRA
- [ ] Reading notes on the main methods studied
- [ ] Code + configs for implemented experiments
- [ ] Short experimental report (results + failure cases)
- [ ] ~20-minute oral presentation on method families + relevance to the future research project

## 📚 Theoretical Concepts Matrix (contract, Annex A §1-8)
- [x] Sources of alignment feedback (demonstrations, pairwise preferences, binary, rankings, critiques, human/AI/rule-based/verifiable) — largely covered via InstructGPT's data-collection sections
- [x] SFT limitations (learning only from positive demonstrations) — covered via InstructGPT + our own Week 1/2 results
- [ ] Rejection sampling / reward-ranked fine-tuning (RAFT)
- [x] Pairwise reward models — covered in depth via InstructGPT's RM section (loss formula, Bradley-Terry)
- [ ] Outcome vs. process reward models
- [ ] Evaluator limitations: position bias, length bias, reward hacking (reward hacking already covered via InstructGPT's alignment-tax discussion)
- [x] RL for LMs: policy/trajectory/reward framing, KL regularization, reference model — covered in depth via InstructGPT's PPO section
- [ ] PPO vs. REINFORCE vs. RLOO vs. GRPO — PPO itself is done; the other 3 are new
- [ ] DPO family: DPO, IPO, KTO, ORPO, SimPO, SLiC-HF
- [ ] AI feedback / Constitutional AI / RLAIF
- [ ] Full FT vs. adapters vs. prefix/prompt tuning vs. LoRA vs. QLoRA
- [ ] Alignment failure modes: sycophancy, excessive/insufficient refusal, preference overfitting, response-diversity loss

## 🔧 Practical Work (contract, Annex A) — triaged

**Must-do (explicitly required, feasible on a single Kaggle T4):**
1. SFT experiment using LoRA — reuse `run_sft()`, add a `peft_config`, compare to Week 1/2's full-FT numbers (13.92 baseline / 75.41 Week1 / 14.61 Week2)
2. Small DPO experiment on paired preference data — needs a chosen/rejected dataset (decide source: constructed from Dolly, or a small existing preference set)
3. One additional preference method — **ORPO** chosen as the pragmatic pick (no separate reference model or RM needed, single training run, cheapest of the DPO-family options)
4. Compare ≥2 parameter-update methods — full FT (already have) vs. LoRA (new) vs. QLoRA (new, if time permits)
5. Failure-case analysis on the new runs (reuse the qualitative-review pipeline from Week 2)

**If time permits (contract's own wording, lowest priority):**
6. One evaluator beyond the RM already studied (LLM-as-judge is the cheapest option — no training required)
7. A small GRPO/RLOO/REINFORCE reproduction

## 🔒 Protocol
Same base model (Qwen2.5-0.5B), same dataset family (Dolly-15k) for continuity with Week 1/2's numbers, unless a method specifically requires paired preference data (DPO/ORPO), in which case document the new dataset's source/license explicitly.

## 👉 Bridge to Week 4
Week 4 is topic selection — Week 3's method comparisons (SFT vs LoRA vs QLoRA vs DPO vs ORPO) directly inform what's computationally realistic for the actual research project.
