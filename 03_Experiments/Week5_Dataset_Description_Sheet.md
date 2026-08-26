# Week 5 — Dataset Description Sheet

Contract deliverable (Annex A, Week 5 — verbatim): "a dataset description sheet." One section per dataset used in the Native-vs-Translated DPO safety-alignment topic. Pre-filled with what's already verified (source, link, license status, schema, language coverage); technical descriptions to be added as they come in.

---

## 1. UbuntuGuard

- **Role in this project:** originally planned as D1 (Native-DPO training source) and D2 (Refusal Rate evaluation) — **see the blocker flagged below.**
- **Source:** Abdullahi, T., Mgonzo, M., Owodunni, A. T., Singh, R., & Eickhoff, C. (2026). *UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages*. arXiv:2601.12696.
- **Link:** https://github.com/hemhemoh/UbuntuGuard (not on Hugging Face — data lives in the repo's `/data` directory as JSONL)
- **License:** ⚠️ **Confirmed absent.** Checked the actual cloned repo directly (2026-08-26): no LICENSE file, no license mention anywhere in `README.md`. Contradicts the earlier CC BY 4.0 assumption carried in the proposal draft — do not treat this as CC BY 4.0 until the authors confirm otherwise (e.g. by email or a repo update).
- **⚠️ Blocker: no training split shipped yet.** The repo's own `README.md` states *"Data and Code Coming Soon......."* — as of this clone, `/data` contains only three **test** files:
  - `Ubuntu_guard_test_all_english_only.jsonl` — 2,449 lines, English only
  - `Ubuntu_guard_test_crosslingual.jsonl` — 2,307 lines, 10 African languages
  - `Ubuntu_guard_test_translated.jsonl` — 2,307 lines, same languages/labels as crosslingual
  
  The paper's abstract mentions a training split (1,171-13,532 examples/language), but it is **not present in this repository as cloned**. The proposal's Native-DPO plan (train on UbuntuGuard's PASS/FAIL pairs) currently has no data to run on unless (a) the authors release the training split later, or (b) we deliberately repurpose part of the test data for training — which would need explicit justification against the "investigate duplication and contamination" task, since RR% evaluation was supposed to use this same test data.
- **Schema (from `README.md`, richer than the version noted 2026-08-24):** `policy, transcript, label (PASS/FAIL), metadata ({'num_rules':int,'violated_policies':[...]}), row_id, base_id, country_code, country, language, topic, theme, domain, sensitive_characteristic`. Only `policy`, `transcript`, `label` are required for evaluation; the rest support per-dimension breakdowns.
- **Verified content (crosslingual + translated splits, counted directly):**
  - Label balance: ~52% PASS / 48% FAIL, consistent across all three files.
  - Languages (crosslingual/translated): Swahili (435), Ewe (345), Zulu (318), Akan (313), Hausa (278), Xhosa (263), Yoruba (144), Igbo (98), Luganda (74), Nyanja (39).
  - Countries: Ghana (658), South Africa (581), Nigeria (520), Kenya (435), Uganda (74), Malawi (39).
  - 2,307 lines collapse to **851 unique `row_id`s** (each `row_id` = one underlying prompt, evaluated against 1-4 conditions/models): 501 have exactly one PASS + one FAIL entry (directly usable as a DPO chosen/rejected pair), 271 have 4 entries, 71 have 3, 8 are unpaired (single entry, unusable for DPO as-is).
  - **`crosslingual` vs `translated` are not simple duplicates:** same `row_id`s, same label counts, but the `policy` text differs — in the sampled row, `crosslingual`'s policy stayed in **English** while `translated`'s policy was itself translated into the target language (Swahili in the sample). This is a different axis than what the proposal assumed ("expert translation vs. NLLB translation") — it looks more like "policy language kept English vs. policy also translated," not two translation-quality tiers of the same content. Needs a closer read of the paper's methodology section before mapping either file onto Native-DPO or Translated-DPO.
- **Decision (2026-08-26):** proceed with the released test data rather than wait — carve our own train/eval split out of it, since no training split has ever been committed to the repo (confirmed via full git history, not just current file listing; see below). In parallel, emailing the author (Paul Okewunmi, commit author on the repo) to ask whether a training split is coming or already exists elsewhere.
- **Git history check (rules out "just a stale README"):** every file ever added, across all 5 commits: `.gitignore`, `README.md` (initial commit) -> `translate_gmt.py` -> `evaluate.py` + the 3 test JSONL files (`Add code and data for model evaluation`, 2026-04-15). The "Data and Code Coming Soon......." line is indeed stale *for the evaluation side* (that commit added real eval code/data without removing the placeholder line) — but no training file has ever existed in this repo at any point, so the training-split gap itself is real, not a documentation lag.
- **Our own train/eval split (row_id-level, to avoid contamination):** using the 501 `row_id`s that have exactly one PASS + one FAIL entry (unambiguous chosen/rejected pairs), split 80/20 **per language** (proportional, not global, so low-count languages like Nyanja aren't wiped out of one side):

  | Language | Total pairs | Train | Eval |
  | :---- | ---: | ---: | ---: |
  | Ewe | 99 | 79 | 20 |
  | Akan | 89 | 71 | 18 |
  | Swahili | 76 | 61 | 15 |
  | Zulu | 59 | 47 | 12 |
  | Xhosa | 55 | 44 | 11 |
  | Hausa | 52 | 42 | 10 |
  | Yoruba | 29 | 23 | 6 |
  | Igbo | 21 | 17 | 4 |
  | Luganda | 15 | 12 | 3 |
  | Nyanja | 6 | 5 | 1 |
  | **Total** | **501** | **401** | **100** |

  A `row_id` assigned to train never appears in eval (and vice versa) — this is what "investigate duplication and contamination" resolves to for this dataset. The 271 four-entry and 71 three-entry `row_id`s (multiple PASS/FAIL variants per prompt) are held out of this initial split; revisit as a way to grow the training pool if 401 pairs proves too small once DPO training actually runs.
  - `crosslingual`'s train/eval split doubles as `translated`'s, since both files share the same `row_id`s — keeps Native-DPO (crosslingual) and Translated-DPO (translated) using the *same* underlying prompts on each side, matching the confound-isolation design from 2026-08-24.
- **Technical description (pending):** _awaiting further details_

---

## 2. AfriHate

- **Role in this project:** D2 (hate-speech/moderation F1 evaluation).
- **Source:** Muhammad, S. H., et al. (2025). *AfriHate: A Multilingual Collection of Hate Speech and Abusive Language Datasets for African Languages*. arXiv:2501.08284.
- **Link:** https://huggingface.co/datasets/afrihate/afrihate
- **Schema:** `id, tweet, label` (`Hate`, `Abusive`, or `Normal`)
- **License:** _to confirm — not yet checked directly against the HF dataset card_
- **Languages:** 15 African languages.
- **Technical description (pending):** _awaiting details_

---

## 3. HealthBench-Africa Extension

- **Role in this project:** D3 (Over-Refusal Rate / utility evaluation, benign health queries).
- **Source:** Tonative-Research, extension of OpenAI's HealthBench.
- **Link:** https://huggingface.co/datasets/tonative/healthbench-africa-extension
- **Schema:** `prompt_id, translated_prompt, rubrics, example_tags, translation_language, translated_at`
- **License:** "Follows the licensing terms of the original dataset" (OpenAI HealthBench) — not fully specified on the dataset card.
- **Size:** ~2,000 rows.
- **Languages:** Igbo, Yoruba, Nigerian Pidgin, Kikuyu. **⚠️ Does not cover Hausa or Swahili** — two of the proposal's stated target languages (section 13, "Restricted Linguistic Scope" lists Hausa, Yoruba, Swahili, Nigerian Pidgin). Over-refusal checks may need to be restricted to Igbo/Yoruba/Pidgin/Kikuyu, or a complementary source found for Hausa/Swahili.
- **Status:** marked "experimental" / "under active development" on the dataset card — translations may still change.
- **Technical description (pending):** _awaiting details_

---

## 4. Uhura-TruthfulQA

- **Role in this project:** D3 (Over-Refusal Rate / utility evaluation, culture & knowledge questions).
- **Source:** Masakhane initiative; translation of TruthfulQA.
- **Link:** https://huggingface.co/datasets/masakhane/uhura-truthfulqa
- **License:** MIT.
- **Languages:** Amharic, Hausa, Northern Sotho (Sepedi), Yoruba, Zulu.
- **Technical description (pending):** _awaiting details_

---

## 5. IrokoBench (subsets)

- **Role in this project:** D3 (Over-Refusal Rate / utility evaluation, general knowledge/reasoning).
- **Source:** Masakhane initiative.
- **Link:** https://huggingface.co/collections/masakhane/irokobench-665a21b6d4714ed3f81af3b1
- **License:** CC BY-SA 4.0.
- **Composition:** AfriXNLI (natural language inference), AfriMMLU (multiple-choice knowledge QA), AfriMGSM (math reasoning).
- **Languages:** 16 African languages (includes Ewe, Lingala, Luganda, Twi, Wolof among others — full list to confirm against the specific subsets used).
- **Technical description (pending):** _awaiting details_

---

## Open items before this sheet is complete
- [x] **Decide how to handle UbuntuGuard's missing training split** — resolved 2026-08-26: proceed with a self-carved, per-language 80/20 row_id split of the released test data (401 train / 100 eval pairs), documented above. Email to the author pending in parallel, not blocking.
- [ ] Confirm UbuntuGuard's actual license directly (email authors / check for an updated repo commit)
- [ ] Read UbuntuGuard's methodology section to correctly map `crosslingual` vs `translated` onto (or replace) the proposal's Native-DPO/Translated-DPO distinction
- [ ] Confirm AfriHate's license from the HF dataset card
- [ ] Resolve the Hausa/Swahili gap in HealthBench-Africa's language coverage for the Over-Refusal evaluation
- [ ] Confirm IrokoBench's exact language list against the languages actually used in this project
- [ ] Decide how to stage/centralize these datasets on Kaggle (next step, once the technical descriptions below are in)
