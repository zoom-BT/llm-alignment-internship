# 🎯 Week 5: Baselines, Data, and Experimental Infrastructure

**Calendar:** nominally 2026-08-24 (Mon) – 2026-08-28 (Fri) per the contract. In practice, Monday and Tuesday went to finalizing and presenting the Week 4 proposal (approved 2026-08-25, minor formatting requests only, not blocking) — so this week's actual task list compresses into Wednesday–Friday, with the remainder carrying into the following week. See [[Week4_Checklist.md]] for the approval-gate resolution.

## 🎯 Objective (contract, Annex A — verbatim)
> "WEEK 5: BASELINES, DATA, AND EXPERIMENTAL INFRASTRUCTURE — During Week 5, the Intern shall: finalize the data-processing pipeline; manually inspect dataset examples and labels; document the source and license of each dataset; construct the training, validation, and test splits where applicable; investigate duplication and contamination; implement the evaluation metrics; evaluate the selected models without modification; establish baseline performance; estimate the computing time, memory requirements, and financial cost where applicable; produce an initial table of results; verify that interrupted experiments can resume from checkpoints."

## ✅ Tasks (contract, verbatim) — mapped to this topic
- [ ] finalize the data-processing pipeline; — implement `build_dpo_dataset_from_pairs`'s real logic: UbuntuGuard PASS→chosen/FAIL→rejected into ChatML for Native-DPO, plus the NLLB-translated counterfactual (same English source content) for Translated-DPO
- [ ] manually inspect dataset examples and labels; — spot-check UbuntuGuard PASS/FAIL pairs, AfriHate hate/abusive/normal labels, HealthBench-Africa prompts across the target languages (Hausa, Yoruba, Swahili, Nigerian Pidgin)
- [x] document the source and license of each dataset; — done 2026-08-24 during the citation audit (UbuntuGuard/AfriHate/HealthBench-Africa/Uhura-TruthfulQA/IrokoBench, all CC BY 4.0 or open on HF, verified against arXiv/HF directly)
- [ ] construct the training, validation, and test splits where applicable; — UbuntuGuard's own train/test split (train for DPO, test reserved for RR% evaluation, no overlap); A1 ablation subsets (250/500/1000)
- [ ] investigate duplication and contamination; — confirm no overlap between UbuntuGuard's train and test splits; document why Native-DPO and Translated-DPO intentionally sharing source content is by design (isolates translation quality per H1), not contamination
- [ ] implement the evaluation metrics; — RR%, Over-RR%, F1-AfriHate (proposal section 9)
- [ ] evaluate the selected models without modification; — B1 (AfriqueQwen-Raw) and the Qwen3.5-4B-Base control, both unaligned
- [ ] establish baseline performance; — Baseline 1 (B1) numbers on UbuntuGuard/AfriHate/HealthBench-Africa
- [ ] estimate the computing time, memory requirements, and financial cost where applicable; — validate proposal section 12's estimate (<2h end-to-end) against a real Kaggle run
- [ ] produce an initial table of results;
- [ ] verify that interrupted experiments can resume from checkpoints. — confirm the `cleanup_checkpoint_dir`/`trainer.save_model` pattern carried over from Week 1-3 still works for this pipeline

## 📥 Deliverables (contract, verbatim)
- [ ] a dataset description sheet;
- [ ] a reproducible evaluation script;
- [ ] baseline results;
- [ ] a computing-resource estimate;
- [ ] an initial version of the main results table;
- [ ] a list of the principal failure modes.

## 📅 Day-by-day catch-up plan

- **Wed 26 Aug (done):** Repository split (`afrique-safety-dpo_alignment`, private, independent), reusable QLoRA/DPO infra carried over from Week 1-3 and re-tested (16/16 passing) — prerequisite scaffolding, not itself a listed Week 5 task.
- **Thu 27 Aug:** Dataset description sheet (source + license for all 5 datasets, building on 08-24's citation audit) + manual inspection of examples/labels + duplication/contamination check (train/test overlap; Native-vs-Translated shared-content rationale).
- **Fri 28 Aug:** Implement `build_dpo_dataset_from_pairs`'s real logic (finalizes the data-processing pipeline) + construct the DPO train/eval splits.
- **Carries into the following week:** implement the RR%/Over-RR%/F1 evaluation script, run it on B1 to establish baseline performance, validate the computing estimate against a real run, produce the initial results table, and confirm checkpoint-resume works. This is the bulk of the remaining scope and realistically doesn't fit in the two days left this week — matching Week 3's own lesson that idealized time estimates don't survive contact with real Kaggle/Colab runs.

## 🔒 Carried over from the Week 4 proposal
- Native-DPO dataset = UbuntuGuard's own training split (PASS→chosen, FAIL→rejected) — no manual writing in target languages required.
- Translated-DPO reuses the *same* English source content as Native-DPO, machine-translated, to isolate translation quality as the only variable (H1).
- Off-policy limitation already documented (proposal section 13): PASS/FAIL come from Llama-3.1-405B/Qwen3-235B, not the target model.

## 👉 Bridge to Week 6
Week 6 (Main Experiments — the actual B2/B3/B4 DPO training runs) cannot start until this week's baseline table and reproducible evaluation script are in hand.
