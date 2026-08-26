# Week 5 — Dataset Description Sheet

Contract deliverable (Annex A, Week 5 — verbatim): "a dataset description sheet." One section per dataset used in the Native-vs-Translated DPO safety-alignment topic. Pre-filled with what's already verified (source, link, license status, schema, language coverage); technical descriptions to be added as they come in.

---

## 1. UbuntuGuard

- **Role in this project:** originally planned as D1 (Native-DPO training source) and D2 (Refusal Rate evaluation) — **see the blocker flagged below.**
- **Source:** Abdullahi, T., Mgonzo, M., Owodunni, A. T., Singh, R., & Eickhoff, C. (2026). *UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages*. arXiv:2601.12696.
- **Link:** https://github.com/hemhemoh/UbuntuGuard (not on Hugging Face — data lives in the repo's `/data` directory as JSONL)
- **License:** the paper itself (arXiv:2601.12696v3) states "License: CC BY 4.0" at the top — restores the proposal's original assumption. The GitHub repo just never got a `LICENSE` file added; a repo hygiene gap, not evidence the data is unlicensed. Confirming directly with the authors anyway (see the email below) before relying on this for anything beyond internal research use.
- **⚠️ Blocker: no training split in the released data, and no public-release commitment either way.** The paper's only availability language is "Our benchmark and code can be found online" (abstract) and a footnote pointing to the GitHub repo — neither explicitly promises the Table 3 training split specifically; "benchmark" most likely just means what's needed to reproduce the reported F1 scores (i.e. the test split). As of this clone, `/data` contains only three **test** files:
  - `Ubuntu_guard_test_all_english_only.jsonl` — 2,449 lines, English only
  - `Ubuntu_guard_test_crosslingual.jsonl` — 2,307 lines, 10 African languages
  - `Ubuntu_guard_test_translated.jsonl` — 2,307 lines, same languages/labels as crosslingual
  
  The paper's Table 3 reports an exact training split per language (642-1,899 for African languages, 13,532 for English — see the full table in `Week5_Deviations_From_Proposal.md`), but it is **not present in this repository as cloned**. The proposal's Native-DPO plan (train on UbuntuGuard's PASS/FAIL pairs) currently has no data to run on unless (a) the authors release the training split later, or (b) we deliberately repurpose part of the test data for training — which would need explicit justification against the "investigate duplication and contamination" task, since RR% evaluation was supposed to use this same test data.
- **Schema (from `README.md`, richer than the version noted 2026-08-24):** `policy, transcript, label (PASS/FAIL), metadata ({'num_rules':int,'violated_policies':[...]}), row_id, base_id, country_code, country, language, topic, theme, domain, sensitive_characteristic`. Only `policy`, `transcript`, `label` are required for evaluation; the rest support per-dimension breakdowns.
- **Verified content (crosslingual + translated splits, counted directly):**
  - Label balance: ~52% PASS / 48% FAIL, consistent across all three files.
  - Languages (crosslingual/translated): Swahili (435), Ewe (345), Zulu (318), Akan (313), Hausa (278), Xhosa (263), Yoruba (144), Igbo (98), Luganda (74), Nyanja (39).
  - Countries: Ghana (658), South Africa (581), Nigeria (520), Kenya (435), Uganda (74), Malawi (39).
  - 2,307 lines collapse to **851 unique `row_id`s** (each `row_id` = one underlying prompt, evaluated against 1-4 conditions/models): 501 have exactly one PASS + one FAIL entry (directly usable as a DPO chosen/rejected pair), 271 have 4 entries, 71 have 3, 8 are unpaired (single entry, unusable for DPO as-is).
  - **`crosslingual` vs `translated`, per the paper's own terminology (arXiv:2601.12696v3):** these are the paper's **Cross-lingual (LRL-EN)** and **Full Localization (LRL-LRL)** evaluation conditions — dialogue is in the local language in both; the only difference is whether the *policy* stays in English (Cross-lingual) or is also localized (Full Localization). A third condition, **English Baseline (EN-EN)**, corresponds to `Ubuntu_guard_test_all_english_only.jsonl`. **This is not the same axis as the proposal's Native-DPO vs. Translated-DPO** (expert-translated vs. NLLB-machine-translated *training data*) — it's about which language the *safety policy* is written in, not about translation quality of a shared source. Repurposing it as a proxy for H1 is a documented deviation from the proposal, not what the benchmark was built to measure — see `Week5_Deviations_From_Proposal.md`.
- **Decision (2026-08-26):** proceed with the released test data rather than wait — carve our own train/eval split out of it, since no training split has ever been committed to the repo (confirmed via full git history, not just current file listing; see below). The paper's own Table 3 reports train/test split sizes per language, and its data statement says "Our benchmark and code can be found online" (pointing at the GitHub repo) — but no train file is actually there, and the paper doesn't say whether guardian models were trained on it or when/whether the train split will be released. Emailing the corresponding author (Tassallah Abdullahi, tassallahabdullahi@brown.edu) to ask directly — draft in `Week5_Deviations_From_Proposal.md`.
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
- **Schema:** `id, tweet, label` (`Hate`, `Abusive`, or `Normal`). Note: the HF card's own "How to Use" code example inconsistently shows a `text` field and a lowercase `"abusive"` label — confirmed this mismatch exists on the actual card itself, not introduced by us; use `tweet`/capitalized labels per the field table, not the example.
- **License:** confirmed `apache-2.0` (checked directly against the HF dataset card, 2026-08-26).
- **Languages / configs (15, ISO 639-3 codes, each independently loadable via `load_dataset("afrihate/afrihate", "<code>")`):** Algerian Arabic (`arq`), Amharic (`amh`), Igbo (`ibo`), Kinyarwanda (`kin`), Hausa (`hau`), Moroccan Arabic (`ary`), Nigerian Pidgin (`pcm`), Oromo (`orm`), Somali (`som`), Swahili (`swa`), Tigrinya (`tir`), Twi (`twi`), isiXhosa (`xho`), Yoruba (`yor`), isiZulu (`zul`).
- **Split sizes:** not stated on the HF dataset card — need to check directly with the `datasets` library if exact per-language/per-split counts are needed before running the F1 evaluation.
- **Baseline models reported in the source paper (context only, not our target models):** AfriBERTa-large, AfriTeVa V2 base, AfroXLMR, AfroXLMR-76L, SetFit (LabSE), InkubaLM-0.4B, mT0-small, BLOOMZ-7B, Mistral-7B, Aya-23-35B, LLaMA-3.1 (8B/70B), Gemma-2 (9B/27B) — no results table on the card itself, only prose ("performance varies significantly by language").
- **Motivation (source's own framing):** built to address Global South hate-speech-detection failure modes — absence of moderation or over-censorship, context-free keyword spotting, missed targeted campaigns against minorities, and over-surveillance of high-profile accounts relative to vulnerable communities.

---

## 3. HealthBench-Africa Extension

- **Role in this project:** D3 (Over-Refusal Rate / utility evaluation, benign health queries).
- **Source:** Tonative-Research, extension of OpenAI's HealthBench (~5,000 clinically-grounded prompts, expert-defined rubrics).
- **Link:** https://huggingface.co/datasets/tonative/healthbench-africa-extension
- **⚠️ Size correction:** only **500 examples** in the (single) `train` split — a subset sampled from the 5,000-prompt original, not the ~2,000 noted earlier (that number came from an imprecise summary, not a direct check). Dataset size: 42,371,072 bytes (~40.4 MB). No separate validation/test split exists; the whole 500-example set would be used purely for our own Over-Refusal evaluation, not for training.
- **⚠️ Translations are machine-generated, not native/expert:** the data itself carries `translation_model: "gpt-4o-mini"` and `translation_provider: "openai"` fields on every row — confirms this is LLM-translated content, same pattern as UbuntuGuard (D2/D4). A third dataset now confirmed machine-translated rather than natively authored; reinforces that finding genuinely native-translated data is a systemic gap across these candidate sources, not a one-off.
- **Human validation:** the dataset card describes a "dual evaluation framework" (LLM-as-judge + human evaluation by medically-trained, target-language-fluent professionals), but its own Methodology section calls this "optional," and Limitations states "human evaluation may not yet cover all samples" — partial/inconsistent coverage, not guaranteed for every row.
- **Schema (actual data preview, richer than and partly inconsistent with the README's own "Features" list):** `prompt_id, english_prompt, translated_prompt, prompt (list, chat-formatted with role/content/translated_content), rubrics, example_tags, ideal_completions_data (dict: ideal_completion, ideal_completions_group, ideal_completions_ref_completions, translated_ideal_completion, translated_ref_completions), canary, translation_info (dict: lang/model/provider/translated_at — duplicates the top-level translation_language/translation_model/translation_provider/translated_at fields), language`. The README's "Features" section lists a simpler `ideal_responses (list)` field that doesn't match the `ideal_completions_data` dict actually observed — another dataset-card/real-data mismatch, similar to AfriHate's `tweet`/`text` one; trust the observed preview over the prose description.
- **License:** still not explicitly stated anywhere on the card — "follows the licensing terms of the original dataset" (OpenAI HealthBench) is the closest statement, not a formal declaration. Still open.
- **Languages:** Igbo, Yoruba, Nigerian Pidgin, Kikuyu. **⚠️ Does not cover Hausa or Swahili** — two of the proposal's stated target languages (section 13, "Restricted Linguistic Scope" lists Hausa, Yoruba, Swahili, Nigerian Pidgin). Over-refusal checks may need to be restricted to Igbo/Yoruba/Pidgin/Kikuyu, or a complementary source found for Hausa/Swahili.
- **Status:** explicitly "an ongoing research effort" per its own README — "translations and evaluations may be further refined over time."

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
- [x] Confirm UbuntuGuard's actual license — paper states CC BY 4.0 (arXiv:2601.12696v3); repo just lacks a LICENSE file. Email to the author also asks for confirmation/a repo update.
- [x] Read UbuntuGuard's methodology section — `crosslingual`/`translated` are the paper's Cross-lingual (LRL-EN) and Full Localization (LRL-LRL) conditions, a policy-language axis, not a translation-quality axis. Repurposing them for H1 is a documented deviation, not a natural fit — see `Week5_Deviations_From_Proposal.md`.
- [x] Confirm AfriHate's license — `apache-2.0`, confirmed directly against the HF dataset card
- [ ] Check AfriHate's exact per-language split sizes via the `datasets` library (not stated on the card)
- [ ] Resolve the Hausa/Swahili gap in HealthBench-Africa's language coverage for the Over-Refusal evaluation
- [ ] Confirm HealthBench-Africa's license directly (still only an indirect "follows the original" statement)
- [ ] Confirm IrokoBench's exact language list against the languages actually used in this project
- [ ] Decide how to stage/centralize these datasets on Kaggle (next step, once the technical descriptions below are in)
