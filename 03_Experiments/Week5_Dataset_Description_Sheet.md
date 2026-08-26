# Week 5 — Dataset Description Sheet

Contract deliverable (Annex A, Week 5 — verbatim): "a dataset description sheet." One section per dataset used in the Native-vs-Translated DPO safety-alignment topic. Pre-filled with what's already verified (source, link, license status, schema, language coverage); technical descriptions to be added as they come in.

---

## 1. UbuntuGuard

- **Role in this project:** D1 (Native-DPO training source, via its PASS/FAIL pairs) and D2 (Refusal Rate evaluation, via its test split).
- **Source:** Abdullahi, T., Mgonzo, M., Owodunni, A. T., Singh, R., & Eickhoff, C. (2026). *UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages*. arXiv:2601.12696.
- **Link:** https://github.com/hemhemoh/UbuntuGuard (not on Hugging Face — data lives in the repo's `/data` directory as JSONL, e.g. `Ubuntu_guard_test_crosslingual.jsonl`)
- **Schema (from the repo):** `policy, transcript, label, metadata, row_id, country_code, language, topic, domain, sensitive_characteristic`
- **License:** ⚠️ **Unconfirmed.** No LICENSE file or declaration found in the repo as of 2026-08-24/26 verification — contradicts an earlier assumption of CC BY 4.0 carried in the proposal draft. Needs direct confirmation before relying on it for redistribution/training-data use.
- **Size:** ~8,091 original English queries; curated test set of 2,307 instances across 10 languages; training-split range 1,171-13,532 examples per language.
- **Languages:** English + Akan, Ewe, Hausa, Igbo, Luganda, Nyanja, Swahili, Tumbuka, Xhosa, Yoruba, Zulu.
- **Technical description (pending):** _awaiting details_

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
- [ ] Confirm UbuntuGuard's actual license directly (email authors / check for an updated repo commit)
- [ ] Confirm AfriHate's license from the HF dataset card
- [ ] Resolve the Hausa/Swahili gap in HealthBench-Africa's language coverage for the Over-Refusal evaluation
- [ ] Confirm IrokoBench's exact language list against the languages actually used in this project
- [ ] Decide how to stage/centralize these datasets on Kaggle (next step, once the technical descriptions below are in)
