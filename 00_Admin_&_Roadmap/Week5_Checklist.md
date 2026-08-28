# 🎯 Week 5: Baselines, Data, and Experimental Infrastructure

**Calendar:** 2026-08-24 (Mon) – 2026-08-28 (Fri) per the contract. Tasks below are tracked against this nominal calendar regardless of which day the underlying work actually happened to get done — see [[Week4_Checklist.md]] for the approval-gate resolution (cleared 2026-08-25).

## 🎯 Objective (contract, Annex A — verbatim)
> "WEEK 5: BASELINES, DATA, AND EXPERIMENTAL INFRASTRUCTURE — During Week 5, the Intern shall: finalize the data-processing pipeline; manually inspect dataset examples and labels; document the source and license of each dataset; construct the training, validation, and test splits where applicable; investigate duplication and contamination; implement the evaluation metrics; evaluate the selected models without modification; establish baseline performance; estimate the computing time, memory requirements, and financial cost where applicable; produce an initial table of results; verify that interrupted experiments can resume from checkpoints."

## ✅ Tasks (contract, verbatim) — mapped to this topic
- [x] finalize the data-processing pipeline; — implemented in the code repo's `src/data.py` (50 tests, runs without a GPU): UbuntuGuard transcripts → DPO pairs, HHH axis stratification, guardian-task builder, Uhura-TruthfulQA pair builder, three-way contamination-free split. The NLLB counterfactual was dropped from the critical path (D6)
- [ ] manually inspect dataset examples and labels; — spot-check UbuntuGuard PASS/FAIL pairs, AfriHate hate/abusive/normal labels, HealthBench-Africa prompts across the target languages (Hausa, Yoruba, Swahili, Nigerian Pidgin)
- [ ] document the source and license of each dataset; — in progress in `03_Experiments/Week5_Dataset_Description_Sheet.md`; two license/coverage flags open (UbuntuGuard's license unconfirmed, HealthBench-Africa doesn't cover Hausa/Swahili)
- [x] construct the training, validation, and test splits where applicable; — UbuntuGuard ships no training split (confirmed via full git history, not just a stale README); self-carved a language-stratified split at `base_stem` level instead. **1,089 usable pairs → 869 train / 220 eval** (the earlier 401/100 figure counted only row_ids holding exactly one PASS and one FAIL, discarding half the corpus). On the guardian task: 461 judge / 1,373 agent / 473 eval. See `Week5_Dataset_Description_Sheet.md`
- [x] investigate duplication and contamination; — **found a real leak and fixed it.** A `row_id`-level split put 85 of 156 eval questions (54%) into training under a different language, because 265 of 566 underlying questions recur across languages. Splitting at `base_stem` level closes it; verified on the real corpus at zero shared `row_id`, zero shared `base_stem`, zero identical prompt text. Also confirmed `crosslingual` and `translated` differ in the `policy` field only (2,307/2,307 rows), so their pools do not add up
- [~] implement the evaluation metrics; — **metric redefined, implementation deferred to Week 6.** RR% as specified does not measure anything on UbuntuGuard, which is a guardian/classification benchmark scored by accuracy and macro F1 (D8). The metric is now the guardian's macro F1, doubling as the stated precision of the compliance detector. Its data plumbing is built and tested; the scoring run needs a GPU
- [ ] evaluate the selected models without modification; — **deferred to Week 6**, blocked on the metric redefinition and on GPU access
- [ ] establish baseline performance; — **deferred to Week 6**, follows directly from the run above
- [ ] estimate the computing time, memory requirements, and financial cost where applicable; — **deferred to Week 6**, needs a real Kaggle run. One input already measured: formatted pairs peak at 1,570 tokens, so `max_seq_length` is 2048, not the 1024 originally assumed
- [ ] produce an initial table of results;
- [ ] verify that interrupted experiments can resume from checkpoints. — **deferred to Week 6**, needs a real training run to interrupt

## 📥 Deliverables (contract, verbatim)
- [ ] a dataset description sheet; — `03_Experiments/Week5_Dataset_Description_Sheet.md`
- [x] a reproducible evaluation script; — `src/run_guardian_eval.py` in the code repo, plus `src/metrics.py`. Runnable as `python -m src.run_guardian_eval --model <name> [--english-control]`; 78 tests, everything except generation covered without a GPU. Validation procedure in `03_Experiments/Judge_Validation_Protocol.md`
- [ ] baseline results; — deferred to Week 6
- [ ] a computing-resource estimate; — deferred to Week 6
- [ ] an initial version of the main results table; — deferred to Week 6
- [x] a list of the principal failure modes. — `03_Experiments/Week5_Deviations_From_Proposal.md`, D1-D9

## 📅 Schedule

| Day | Task(s) |
| :---- | :---- |
| Mon 24 | Dataset description sheet (source + license) + manual inspection of examples/labels |
| Tue 25 | Duplication/contamination check + construct train/validation/test splits |
| Wed 26 | Finalize the data-processing pipeline |
| Thu 27 | Implement the evaluation metrics + evaluate the selected models without modification |
| Fri 28 | Establish baseline performance, validate the computing estimate, produce the initial results table, verify checkpoint-resume, list principal failure modes |

## 🔒 Carried over from the Week 4 proposal — superseded during the week
- ~~Native-DPO dataset = UbuntuGuard's own training split~~ — no training split exists (D1); split carved from the released test data instead.
- ~~Translated-DPO reuses the same English source content, machine-translated, to isolate translation quality (H1)~~ — dropped from the critical path (D6): H1's question is already answered in the literature, and the headline claim moved to H2.
- Off-policy limitation still stands (proposal section 13): PASS/FAIL come from Llama-3.1-405B/Qwen3-235B, not the target model.

## ⚠️ Deviations to raise at supervision
Nine recorded in `03_Experiments/Week5_Deviations_From_Proposal.md`. Six are data-level findings; three change the approved proposal itself:
- **D6** — headline claim recentred from H1 (native vs. translated) to H2 (does the CPT backbone retain alignment better?). Changes the research question, contribution C2 and the title.
- **D8** — UbuntuGuard is a guardian/classification benchmark, not a generation one. RR% as specified in section 9 does not measure anything on this data; the metric becomes the guardian's macro F1, which doubles as the stated precision of the compliance detector.
- **D9** — oriented on the Honest axis with Harmless as the contrast. The corpus is 45% misinformation against 25% stereotypes/hate speech, and Harmless-only would leave 216 training pairs across ten languages.

Models, experimental protocol and compute budget are unchanged by all three.

## 👉 Bridge to Week 6
Four contract tasks carry over — evaluate the models without modification, establish baseline performance, estimate compute, verify checkpoint-resume — all four blocked on the same thing: a first GPU session. They fold into Week 6's opening run rather than being re-planned separately.

Week 6 order of work:
1. Train and measure the compliance judge on the guardian task (Qwen-Base backbone, judge slice only). Self-contained, uses the authors' own evaluation script, and yields a publishable result on its own.
2. B1 baseline on the same metric, closing the four carried-over tasks.
3. B2/B3/B4 DPO runs on the Honest axis, evaluated on both axes.
