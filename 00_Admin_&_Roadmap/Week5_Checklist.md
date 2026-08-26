# 🎯 Week 5: Baselines, Data, and Experimental Infrastructure

**Calendar:** 2026-08-24 (Mon) – 2026-08-28 (Fri) per the contract. Tasks below are tracked against this nominal calendar regardless of which day the underlying work actually happened to get done — see [[Week4_Checklist.md]] for the approval-gate resolution (cleared 2026-08-25).

## 🎯 Objective (contract, Annex A — verbatim)
> "WEEK 5: BASELINES, DATA, AND EXPERIMENTAL INFRASTRUCTURE — During Week 5, the Intern shall: finalize the data-processing pipeline; manually inspect dataset examples and labels; document the source and license of each dataset; construct the training, validation, and test splits where applicable; investigate duplication and contamination; implement the evaluation metrics; evaluate the selected models without modification; establish baseline performance; estimate the computing time, memory requirements, and financial cost where applicable; produce an initial table of results; verify that interrupted experiments can resume from checkpoints."

## ✅ Tasks (contract, verbatim) — mapped to this topic
- [ ] finalize the data-processing pipeline; — implement `build_dpo_dataset_from_pairs`'s real logic: UbuntuGuard PASS→chosen/FAIL→rejected into ChatML for Native-DPO, plus the NLLB-translated counterfactual (same English source content) for Translated-DPO
- [ ] manually inspect dataset examples and labels; — spot-check UbuntuGuard PASS/FAIL pairs, AfriHate hate/abusive/normal labels, HealthBench-Africa prompts across the target languages (Hausa, Yoruba, Swahili, Nigerian Pidgin)
- [ ] document the source and license of each dataset; — in progress in `03_Experiments/Week5_Dataset_Description_Sheet.md`; two license/coverage flags open (UbuntuGuard's license unconfirmed, HealthBench-Africa doesn't cover Hausa/Swahili)
- [x] construct the training, validation, and test splits where applicable; — UbuntuGuard ships no training split (confirmed via full git history, not just a stale README); self-carved a per-language 80/20 row_id split instead (401 train / 100 eval pairs) — see `Week5_Dataset_Description_Sheet.md`. A1 ablation now capped by this pool (max ~401, not the proposal's original 1000)
- [x] investigate duplication and contamination; — confirmed no `row_id` appears on both sides of the 401/100 split; documented why Native-DPO (crosslingual) and Translated-DPO (translated) sharing the same `row_id`s on each side is by design, not contamination
- [ ] implement the evaluation metrics; — RR%, Over-RR%, F1-AfriHate (proposal section 9)
- [ ] evaluate the selected models without modification; — B1 (AfriqueQwen-Raw) and the Qwen3.5-4B-Base control, both unaligned
- [ ] establish baseline performance; — Baseline 1 (B1) numbers on UbuntuGuard/AfriHate/HealthBench-Africa
- [ ] estimate the computing time, memory requirements, and financial cost where applicable; — validate proposal section 12's estimate (<2h end-to-end) against a real Kaggle run
- [ ] produce an initial table of results;
- [ ] verify that interrupted experiments can resume from checkpoints. — confirm the `cleanup_checkpoint_dir`/`trainer.save_model` pattern carried over from Week 1-3 still works for this pipeline

## 📥 Deliverables (contract, verbatim)
- [ ] a dataset description sheet; — `03_Experiments/Week5_Dataset_Description_Sheet.md`
- [ ] a reproducible evaluation script;
- [ ] baseline results;
- [ ] a computing-resource estimate;
- [ ] an initial version of the main results table;
- [ ] a list of the principal failure modes.

## 📅 Schedule

| Day | Task(s) |
| :---- | :---- |
| Mon 24 | Dataset description sheet (source + license) + manual inspection of examples/labels |
| Tue 25 | Duplication/contamination check + construct train/validation/test splits |
| Wed 26 | Finalize the data-processing pipeline |
| Thu 27 | Implement the evaluation metrics + evaluate the selected models without modification |
| Fri 28 | Establish baseline performance, validate the computing estimate, produce the initial results table, verify checkpoint-resume, list principal failure modes |

## 🔒 Carried over from the Week 4 proposal
- Native-DPO dataset = UbuntuGuard's own training split (PASS→chosen, FAIL→rejected) — no manual writing in target languages required.
- Translated-DPO reuses the *same* English source content as Native-DPO, machine-translated, to isolate translation quality as the only variable (H1).
- Off-policy limitation already documented (proposal section 13): PASS/FAIL come from Llama-3.1-405B/Qwen3-235B, not the target model.

## 👉 Bridge to Week 6
Week 6 (Main Experiments — the actual B2/B3/B4 DPO training runs) cannot start until this week's baseline table and reproducible evaluation script are in hand.
