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
  - 2,307 lines collapse to **851 unique `row_id`s** (each `row_id` = one underlying prompt, evaluated against 1-4 conditions/models): 501 have exactly one PASS + one FAIL entry, 271 have 4 entries (two PASS, two FAIL), 71 have 3, 8 are unpaired (single entry, unusable for DPO). The multi-entry ones are usable too — see the split below — provided no single response is matched into two different pairs.
  - **`crosslingual` vs `translated`, per the paper's own terminology (arXiv:2601.12696v3):** these are the paper's **Cross-lingual (LRL-EN)** and **Full Localization (LRL-LRL)** evaluation conditions — dialogue is in the local language in both; the only difference is whether the *policy* stays in English (Cross-lingual) or is also localized (Full Localization). A third condition, **English Baseline (EN-EN)**, corresponds to `Ubuntu_guard_test_all_english_only.jsonl`. **This is not the same axis as the proposal's Native-DPO vs. Translated-DPO** (expert-translated vs. NLLB-machine-translated *training data*) — it's about which language the *safety policy* is written in, not about translation quality of a shared source. Repurposing it as a proxy for H1 is a documented deviation from the proposal, not what the benchmark was built to measure — see `Week5_Deviations_From_Proposal.md`.
- **Decision (2026-08-26):** proceed with the released test data rather than wait — carve our own train/eval split out of it, since no training split has ever been committed to the repo (confirmed via full git history, not just current file listing; see below). The paper's own Table 3 reports train/test split sizes per language, and its data statement says "Our benchmark and code can be found online" (pointing at the GitHub repo) — but no train file is actually there, and the paper doesn't say whether guardian models were trained on it or when/whether the train split will be released. Emailing the corresponding author (Tassallah Abdullahi, tassallahabdullahi@brown.edu) to ask directly — draft in `Week5_Deviations_From_Proposal.md`.
- **Git history check (rules out "just a stale README"):** every file ever added, across all 5 commits: `.gitignore`, `README.md` (initial commit) -> `translate_gmt.py` -> `evaluate.py` + the 3 test JSONL files (`Add code and data for model evaluation`, 2026-04-15). The "Data and Code Coming Soon......." line is indeed stale *for the evaluation side* (that commit added real eval code/data without removing the placeholder line) — but no training file has ever existed in this repo at any point, so the training-split gap itself is real, not a documentation lag.
- **Our own train/eval split (row_id-level, to avoid contamination).** Superseded the earlier plan of using only the 501 unambiguous `row_id`s: the 349 `row_id`s holding several responses per label yield valid extra pairs too, provided no response is ever matched twice. Pairing greedily within each `row_id` gives **1,089 usable pairs, not 501** — the earlier figure discarded roughly half the corpus. Split 80/20 **per language** (proportional, not global, so low-count languages like Nyanja aren't wiped out of one side):

  | Language | Total pairs | Train | Eval |
  | :---- | ---: | ---: | ---: |
  | Swahili | 207 | 160 | 47 |
  | Ewe | 165 | 133 | 32 |
  | Zulu | 152 | 119 | 33 |
  | Akan | 149 | 119 | 30 |
  | Hausa | 128 | 104 | 24 |
  | Xhosa | 123 | 99 | 24 |
  | Yoruba | 68 | 56 | 12 |
  | Igbo | 44 | 35 | 9 |
  | Luganda | 34 | 29 | 5 |
  | Nyanja | 19 | 14 | 5 |
  | **Total** | **1,089** | **868** | **221** |

  Implemented and tested in the code repo (`src/data.py`, 20 tests), not done by hand. A `row_id` assigned to train never appears in eval — this is what "investigate duplication and contamination" resolves to for this dataset, and it is enforced in code rather than assumed. Verified on the real data: zero `row_id` overlap **and** zero identical prompts across the two splits. The second check is the one that matters here: two pairs carved from the same `row_id` share a prompt verbatim, so splitting at pair level instead of `row_id` level would have leaked training prompts straight into evaluation.

  **Pair construction:** PASS and FAIL transcripts diverge at the *first* assistant response in 839 of 843 dialogues, so pairs are cut there — prompt = safety policy (system) + opening user turn, chosen = the compliant response, rejected = the violating one. The rest of each dialogue is discarded, because a FAIL transcript's later turns are conditioned on an already-unsafe answer. Three pairs diverge on a user turn (different questions on each side) and are dropped.

  **Two parsing traps in this data**, both worth knowing before anyone re-reads these files: turns are marked `User:` / `Agent:` (not `Assistant:`), with `Agent:` usually indented rather than at column 0; and `metadata` is a *Python* dict repr with single quotes, so `json.loads` raises on it — needs `ast.literal_eval`.
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
- **Source:** Masakhane initiative; TruthfulQA (Lin et al., 2022) translated by **professional human translators** (not machine translation — a genuine positive contrast to UbuntuGuard/HealthBench-Africa, both confirmed machine-translated). See the Uhura paper: *A Benchmark for Evaluating Scientific Question Answering and Truthfulness in Low-Resource African Languages*.
- **Link:** https://huggingface.co/datasets/masakhane/uhura-truthfulqa
- **License:** MIT (explicitly confirmed on the dataset card).
- **⚠️ Card inconsistency resolved, then re-verified against the API (2026-08-28):** the card's prose says "six languages" but names only five (Amharic, Hausa, Northern Sotho/Sepedi, Yoruba, Zulu). The sixth is **Swahili**. Confirmed authoritatively via `datasets-server.huggingface.co/splits`, which lists **14 configs = 7 languages × 2 tasks**: `am, ha, nso, sw, yo, zu` (six African) **plus `en`**. A later re-check through a page summariser returned a list that dropped Swahili and counted English as the sixth — that reading is wrong; the API is the authority here. Same drift pattern as AfriHate's `tweet`/`text` and HealthBench-Africa's `ideal_responses`/`ideal_completions_data`. **This closes part of the Hausa/Swahili gap flagged for HealthBench-Africa** — Uhura covers both, just not for the health domain specifically.
- **Language overlap with UbuntuGuard: Hausa, Swahili, Yoruba, Zulu** (4 languages present in both), which is the usable intersection for any controlled comparison across the two datasets.
- **Loading:** configs are named `{language_code}_{task}` (e.g. `am_generation`, `am_multiple_choice`, `sw_generation`, ...) — language and task are combined in one config string, not separate `load_dataset` arguments: `load_dataset("masakhane/uhura-truthfulqa", "am_generation")`.
- **Two task formats per language:**
  - `multiple_choice`: `question`, `mc1_targets` (dict: `choices` list of 4-5 strings, `labels` list with a single `1` for the correct choice, rest `0`).
  - `generation`: `type` (Adversarial/Non-Adversarial), `category` (e.g. Law, Health, Sociology), `question`, `best_answer`, `correct_answers` (list), `incorrect_answers` (list), `source` (URL).
- **Splits (per config):** `train` is 8 everywhere; **`test` varies by language and is not 809**. Total rows per language, verified via the size API: `en` 817, `nso` 817, `am` 815, `yo` 815, `sw` 813, `ha` 799, `zu` 761 — so `ha`'s test split is 791, confirmed by actually loading it. English matches the original TruthfulQA's 817 questions exactly; the African configs fall short, so the translations are **not** a complete 1:1 rendering of all 817 in every language. Do not assume parallel question sets across languages, and read the split size from the config rather than hard-coding one.
- **Pair yield:** loading `ha_generation` gives 791 rows → **791 usable pairs**, i.e. every row carries both a `best_answer` and at least one `incorrect_answer`. No attrition, unlike UbuntuGuard where 2,307 rows collapse to 1,089 pairs.
- **✅ Usable directly as an Honest-axis DPO training source.** The `generation` config carries `best_answer`, `correct_answers` (1 entry) and `incorrect_answers` (3 entries) — verified on real `ha_generation` rows, not inferred from the card. That is a ready-made preference pair (chosen = `best_answer`, rejected = an entry from `incorrect_answers`) with no generation and no judging step required. Combined with the MIT licence and the professional human translation, this is the cleanest training-pair source found across all six datasets.
- **⚠️ But the *content* is Western, not African.** Sampled 100 real `ha_generation` rows: categories are stock TruthfulQA (Misconceptions, Sociology, Health, Conspiracies, Paranormal, Indexical Error), and `source` URLs are 52% `en.wikipedia.org`, plus `ourworldindata.org`, `snopes.com`, `webmd.com`. Sample questions concern food prices in America, purchasing power in Canada, who built the first autobahn, and UFO conspiracies. Uhura is TruthfulQA **translated**, not culturally re-grounded.
- **Consequence — Uhura and UbuntuGuard are orthogonal, and must not be pooled.** They differ on two independent dimensions at once:

  | | African-grounded content | Western-grounded content |
  | :---- | :---- | :---- |
  | **Human translation** | *(no dataset found — this is the D2/D4 gap)* | **Uhura-TruthfulQA** |
  | **Machine translation** | **UbuntuGuard (misinformation theme)** | *(n/a)* |

  Merging them would not produce "more Honest training data"; it would mix two constructs. Kept apart, they give an ablation that isolates precisely what continued pre-training is supposed to contribute — **local knowledge**. Prediction: an African-CPT backbone gains more on African-grounded truthfulness (UbuntuGuard misinformation) than on translated Western truthfulness (Uhura), because the former requires facts about that place and the latter does not.

---

## 5. IrokoBench (subsets)

- **Role in this project:** D3 (Over-Refusal Rate / utility evaluation, general knowledge/reasoning).
- **Source:** Adelani, D. I., et al. (2024). *IrokoBench: A New Benchmark for African Languages in the Age of Large Language Models*. arXiv:2406.03368 (Masakhane initiative).
- **Link:** https://huggingface.co/collections/masakhane/irokobench-665a21b6d4714ed3f81af3b1
- **License:** CC BY-SA 4.0 — confirmed directly from the paper's own release statement ("We will release IrokoBench on GitHub under the CC BY-SA 4.0 licence upon acceptance").
- **✅ Genuinely native/professional translation — the strongest-verified source of the five.** Checked the full paper text directly (not just abstract/card prose, given how unreliable that's been for the other four datasets): "We recruited language coordinators for each of the 16 African languages and French, and asked them to recruit **professional translators**." Translators were **paid** (amounts vary by country, e.g. "$549.78 for the translation of 1020 XNLI samples in South Africa, $355.86 in Nigeria"), translated from English (or from French for Ewe/Lingala/Wolof translators, being Francophone-region languages), and **payment was gated on quality**: "Language coordinators reviewed and corrected any poorly translated sentences. Translators received payment only after this phase." Quality was also checked quantitatively via COMET QE scores (AfriCOMET) between the human translation and the source. A real counter-example, alongside Uhura-TruthfulQA, to D2/D4's pattern of "African-language" datasets turning out to be LLM-translated.
- **Composition:** AfriXNLI (natural language inference), AfriMMLU (multiple-choice knowledge QA), AfriMGSM (math reasoning, subset of GSM8k).
- **⚠️ "translate-test" variants are NOT a native-vs-machine-translation counterfactual pair (corrects an initial hope):** each task also has a `-translate-test` dataset (e.g. `masakhane/afrimgsm-translate-test`), but per its own card this is "translations of the GSM8k dataset from 16 African languages and 1 high resource language **into English** using NLLB" — i.e. the African-language test set machine-translated *back into English*, for the standard NLP "translate-test" evaluation paradigm (comparing a multilingual model on native text vs. an English-only model on machine-translated-to-English text). Not the same content translated two ways into the target language — doesn't resolve D2/D4.
- **Language count, resolved:** sources disagree (16, 17, or 18 depending on the page) because task coverage varies — the paper's own figure is **17 native African languages + English + French**, but individual task datasets don't all cover the full 17 (e.g. AfriMGSM's actual language table lists only 15 African codes + en + fr = 17 configs total, not the full 17 African + 2).
- **AfriMGSM specifics (verified directly against the dataset card):**
  - **⚠️ Corrected 2026-09-02 against the datasets-server API — the card's language list is wrong.** The real configs are **19**, in three-letter ISO codes: `amh, eng, ewe, fra, hau, ibo, kin, lin, lug, orm, sna, sot, swa, twi, vai, wol, xho, yor, zul`. Not 17, and not the two-letter codes (`ha`, `sw`, `en`) the card's table lists — Hausa is `hau`, Swahili `swa`. Third dataset in this sheet whose card prose contradicts its own data; query the API rather than reading the table.
  - Splits: every language has `train`: 8, `test`: 250 (mirrors the original GSM8k subset sizes used).
  - Schema (per-language data, richer than the base card's simple "question, answer" description): `question` (string), `answer` (full chain-of-thought string), `answer_number` (int, clean numeric target), `equation_solution` (string, the arithmetic expression) — the two extra fields aren't mentioned in the card's own "Data Fields" section.
  - License: Apache-2.0 stated on this specific dataset's own card (vs. the collection-level CC BY-SA 4.0 from the paper) — minor license inconsistency between the collection and the individual dataset card, worth a note but not treated as contradictory (Apache-2.0 is compatible with/a subset of what CC BY-SA 4.0 permits for this kind of use).

---

## 6. LSR — Linguistic Safety Robustness

- **Role in this project:** methodology reference for cross-lingual refusal measurement, **not** a training or bulk-evaluation source.
- **Source:** Faruna, G. A. (2026). *LSR: Linguistic Safety Robustness Benchmark for Low-Resource West African Languages.* arXiv:2603.19273, submitted 27 February 2026. Single author.
- **Link:** `Faruna01/lsr-benchmark` (HF Datasets); live dashboard at `Faruna01/lsr-dashboard` (HF Spaces).
- **License:** CC-BY-SA 4.0.
- **Languages:** Yoruba, Hausa, Igbo, **Igala**.
- **What it measures:** cross-lingual refusal degradation, via a **dual-probe protocol** — matched English and target-language probes submitted to the same model — scored with **Refusal Centroid Drift (RCD)**, quantifying how much of a model's English refusal behaviour is lost when the harmful intent is expressed in the target language.
- **Reported findings:** on Gemini 2.5 Flash, English refusal holds at ~90%; across the four West African languages it falls to **35-55%**, with Igala worst at RCD = 0.55.
- **⚠️ Very small: 14 probes**, across four harm categories. This is a proof-of-concept benchmark, not a corpus. Useful for its *method*, not its volume — do not plan to train or to compute per-language statistics on it.
- **⚠️ Construction method not stated.** The paper does not say whether the target-language probes were natively authored, human-translated or machine-translated. Same unanswered question as UbuntuGuard's (D4); treat as unknown rather than assuming.
- **Only one model evaluated**, and it is closed (Gemini 2.5 Flash). No open model, and no African-CPT model, has been measured with this protocol.
- **Why it matters to us anyway:** the dual-probe design is an independent validation of the English-control logic already built into our evaluation — measure the same question in English and in the target language, and treat the *gap* as the result. RCD is a ready-made, citable name for that gap.

---

## 7. TukaBench

- **Role in this project:** strong candidate for **D1** (source prompts to build our own on-policy DPO pairs), **D2** (Refusal Rate evaluation — better language overlap than UbuntuGuard), and **D3** (Over-Refusal, via `afri-jbb-benign` — covers Hausa and Swahili, which HealthBench-Africa doesn't).
- **Source:** Akinode, V., Li, S., Hamidouche, W., Zamir, W., Becker-Reshef, I., & Adelani, D. I. (2026). *TukaBench: A Culturally Grounded Jailbreak Benchmark for African Languages*. arXiv:2606.01322 — Mila (Quebec AI Institute), McGill University, Microsoft AI for Good Research Lab. **Same institution (McGill-NLP) as our target model (AfriqueQwen3.5-4B-50Langs)** — a good sign of ecosystem/tooling compatibility.
- **Link:** https://huggingface.co/datasets/McGill-NLP/tukabench
- **License:** ⚠️ **CC-BY-NC 4.0 — non-commercial research use only** (explicit on the card: "Released under CC-BY-NC 4.0. Non-commercial research use only."). More restrictive than the other four datasets (Apache-2.0/MIT/CC BY-SA 4.0) — fine for this research internship, but flag before any use beyond that.
- **Composition (3 configs, 100 prompts each, 8 languages = 2,400 rows total):**
  - `afri-jbb-harm`: JailbreakBench's 100 harmful prompts, human-translated, Western context preserved.
  - `afri-jbb-benign`: JBB's 100 benign control prompts, human-translated — for over-refusal measurement.
  - `afri-jbb-culture`: the same harmful prompts rewritten into African cultural contexts (locally relevant named entities/scenarios) before translation.
- **Schema:** `Index, Goal (English source), Goal_Translation (target-language version, equal to Goal for the eng split)`.
- **Languages/splits:** `eng, amh, hau, ibo, nya, swh, xho, yor` — 7 African + English. Good overlap with our target set (Hausa, Yoruba, Swahili all present, unlike HealthBench-Africa).
- **Construction (hybrid MT + guaranteed human correction — stronger than UbuntuGuard/HealthBench-Africa's "optional"/absent validation, short of IrokoBench/Uhura's fully-human translation):** (1) machine translation — Google Translate for 6 languages, `AfriqueQwen-8B` (with MAFAND few-shot examples) for Yoruba specifically, since Google Translate didn't reliably preserve Yoruba diacritics; (2) quality estimation via SSA-COMET-QE, flagging anything below 0.50; (3) **human post-editing by two native-speaker annotators per language**, correcting the machine output (and, for `afri-jbb-culture`, performing the cultural adaptation itself). Not purely native-authored, but every row is guaranteed human-corrected, not just spot-checked.
- **⚠️ No raw pre-edit machine-translation output is released** — only the final human-post-edited `Goal_Translation`. Checked directly: doesn't provide a native-vs-raw-MT counterfactual pair either, same limitation as Uhura/IrokoBench for D2/D4's purposes.
- **Relevant finding from the paper itself (useful context, not our own result):** across closed and open models, prompting in African languages reduces refusal relative to English, and culturally-adapted prompts (`afri-jbb-culture`) reduce it further still — direct prior evidence for the general phenomenon our own H1 is built around. The paper also reports **reduced LLM-as-a-judge reliability in low-resource languages** — a methodological warning worth weighing against our own proposal's "automated classification + 10% manual cross-check" evaluation procedure (section 9); the 10% figure may be worth revisiting given this finding.
- **Note:** the paper's abstract describes four experimental conditions (including GPT-5.2-validated human-curated prompts and code-switched prompts), but the public HF release only ships the three configs above — the other two conditions from the paper aren't in this dataset as released.

---

## Open items before this sheet is complete
- [x] **Decide how to handle UbuntuGuard's missing training split** — resolved 2026-08-26: proceed with a self-carved, per-language 80/20 row_id split of the released test data (**868 train / 221 eval** pairs), implemented and tested in `src/data.py`, documented above. Email to the author pending in parallel, not blocking.
- [x] Confirm UbuntuGuard's actual license — paper states CC BY 4.0 (arXiv:2601.12696v3); repo just lacks a LICENSE file. Email to the author also asks for confirmation/a repo update.
- [x] Read UbuntuGuard's methodology section — `crosslingual`/`translated` are the paper's Cross-lingual (LRL-EN) and Full Localization (LRL-LRL) conditions, a policy-language axis, not a translation-quality axis. Repurposing them for H1 is a documented deviation, not a natural fit — see `Week5_Deviations_From_Proposal.md`.
- [x] Confirm AfriHate's license — `apache-2.0`, confirmed directly against the HF dataset card
- [ ] Check AfriHate's exact per-language split sizes via the `datasets` library (not stated on the card)
- [x] Resolve the Hausa/Swahili gap for the Over-Refusal evaluation — partially: Uhura-TruthfulQA covers both (its "six languages" claim was under-documented, actually includes Swahili). Still a gap specifically for the *health* domain, since HealthBench-Africa itself doesn't cover Hausa/Swahili.
- [ ] Confirm HealthBench-Africa's license directly (still only an indirect "follows the original" statement)
- [x] Confirm IrokoBench's exact language list — resolved: paper's own figure is 17 native African languages + English + French; per-task datasets (e.g. AfriMGSM) don't all cover the full set, explaining the 16/17/18 discrepancies across different pages
- [ ] Decide how to stage/centralize these datasets on Kaggle (next step, once the technical descriptions below are in)
