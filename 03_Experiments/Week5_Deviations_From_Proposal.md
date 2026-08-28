# Week 5 — Deviations From the Approved Proposal

The approved proposal (`04_Weekly_Reports/Week_04_Research_Proposal.md`, approved 2026-08-25) is **not being edited** to reflect what's below — per contract discipline, a supervisor-approved research design stays as-is; deviations discovered during execution are logged separately and reported alongside results, not silently folded back into the original document.

**Decision (2026-08-26, final for now):** proceed as a proof-of-concept scoped to the released UbuntuGuard test data (401/100 split, D1) rather than wait on the authors. Results from this phase should be framed explicitly as a POC — validating the pipeline and the H1/H2/H3 comparisons work end-to-end — not as the full-scale study the proposal's original numbers (train_size up to 1000, A1 ablation) assumed. Searching in parallel for a complementary dataset that can properly fill the native-translation gap (D2/D4) — see the search prompt below.

**Update (2026-08-26):** that search is now **secondary, not blocking** — see **D6**. The primary claim has been recentred from H1 to H2, which does not depend on a native-vs-translated contrast at all. A genuinely native source would still strengthen an optional H1 robustness axis, so the search prompt is kept, but no longer gates Week 6's training runs.

---

## D1. UbuntuGuard has no training split (proposal section 7, D1)

**Planned:** train Native-DPO directly on UbuntuGuard's training split (PASS→chosen, FAIL→rejected).

**Actual:** confirmed via the repo's full git history (5 commits, `github.com/hemhemoh/UbuntuGuard`) that no training file has ever been committed — only three test-split JSONL files exist, added in the latest commit (2026-04-15). The paper (arXiv:2601.12696v3) reports train/test split sizes in its Table 3, but its only availability language ("Our benchmark and code can be found online," abstract + footnote 1) never explicitly commits to releasing the training split specifically — checked the abstract, introduction, ethics, limitations, acknowledgments, and appendix, none clarify this. Not a broken promise, just genuinely ambiguous — hence asking directly rather than assuming either way.

**Resolution:** self-carved a language-stratified 80/20 split of the pairs recoverable from the released test data, split at `row_id` level so no prompt appears on both sides. Implemented and tested in the code repo (`src/data.py`, 20 tests).

**Correction (2026-08-26): the usable pool is 1,089 pairs, not 501.** The earlier figure counted only `row_id`s holding *exactly* one PASS and one FAIL. In fact 349 of the 851 `row_id`s hold several responses per label (271 hold two PASS and two FAIL). Matching them up within each `row_id`, without ever reusing a response, more than doubles the yield:

| | Recorded earlier | Actual |
| :---- | ---: | ---: |
| Usable preference pairs | 501 | **1,089** |
| Train / eval | 401 / 100 | **868 / 221** |

**Cross-lingual contamination found and fixed (2026-08-26).** A `row_id`-level split is not coarse enough. `base_id` looks like `GHA1002_llama` — a source-question id plus the generating model — and the stem `GHA1002` recurs across languages: 265 of the 566 underlying questions appear in more than one. Measured on the real corpus, splitting at `row_id` level put **85 of 156 eval questions (54%) into training under a different language**. For a study about cross-lingual safety transfer on a multilingual backbone that is disqualifying: it would measure memorisation and report it as transfer. The split now groups at `base_stem` level, filling languages rarest-first so the shared stems don't all get absorbed by Swahili and starve Nyanja.

Final split: **869 train / 220 eval**, at essentially no cost in volume. Verified on the real data, all three checks at zero: no shared `row_id`, no shared `base_stem`, no identical prompt text across splits. Every language lands at 20-21% eval.

Per-language split (train / eval): Swahili 165/42, Ewe 132/33, Zulu 122/30, Akan 119/30, Hausa 102/26, Xhosa 98/25, Yoruba 54/14, Igbo 35/9, Luganda 27/7, Nyanja 15/4.

**Full audit of the released repository (2026-08-26).** All three JSONL files checked, not just the one used for training; the repo holds 8 files across 5 commits, working tree clean, so what is local is the entirety of what was published.

| File | Rows | Unique `row_id` | Usable pairs | Content |
| :---- | ---: | ---: | ---: | :---- |
| `..._all_english_only` | 2,449 | 903 | 1,150 | English dialogue, English policy |
| `..._crosslingual` | 2,307 | 851 | 1,089 | African dialogue, **English** policy |
| `..._translated` | 2,307 | 851 | 1,089 | African dialogue, **localised** policy |

Every one of the eleven per-language counts matches the paper's Table 3 test column exactly (Akan 313, Ewe 345, Hausa 278, Igbo 98, Luganda 74, Nyanja 39, Swahili 435, Xhosa 263, Yoruba 144, Zulu 318, English 2,449). The released test data is precisely what the paper documents — no shortfall on that side.

**`crosslingual` and `translated` differ in the `policy` field only** — all 2,307 rows differ there, and zero differ in `transcript`, `metadata`, `theme` or `domain`. The transcripts are byte-identical. So the two files are the same 1,089 dialogues under two conditions and **the pools do not add up**. This settles D2 empirically rather than by reading the paper: the axis UbuntuGuard actually offers is the language of the *policy*, not the provenance of the *content*. It does hand us one clean controlled variable for free — same dialogue, policy language as the only difference.

**Consequence for the proposal's A1 ablation (section 11):** largely restored. At 401 the 250/500/1000 sweep was unreachable; at 868 it runs as 100/200/868 — same shape, and D6 makes A1 the more relevant of the two planned ablations. `config.yaml`'s `train_size` is 868, still short of the proposal's 1000 but no longer a different order of magnitude.

**Two data-shape findings from implementing this, both recorded because they change the design rather than just the code:**

1. **PASS and FAIL diverge at the *first* assistant response, not the last** (839 of 843 dialogues). The pairs are therefore cut at the first divergent turn, discarding the rest of the dialogue. This is the right cut rather than a loss: the later turns of a FAIL transcript are conditioned on an already-unsafe answer, so keeping them would blur "produced an unsafe answer" together with "kept going down that path". It does mean the DPO training signal is effectively single-turn, despite UbuntuGuard being a multi-turn benchmark — worth stating in the write-up. Three pairs diverge on a *user* turn (i.e. answer different questions) and are dropped.
2. **`max_seq_length` was wrong at 1024.** Measured with the actual AfriqueQwen tokenizer, formatted pairs run to a median of 819 tokens and a maximum of 1,570 — 1024 would have silently truncated 13.8% of examples. Truncating a DPO response removes the very signal being trained on, so this would have produced plausible-looking but meaningless runs. Raised to 2048 (zero truncation). The safety policy in the system message is the bulk of it (~2,700 chars median, against ~245 for the user turn).

**D7. The evaluation pool is far smaller than first stated — and the statistics have to change accordingly.**

An earlier note in this file put the held-out African evaluation pool at "~1,900 prompts". That was wrong: it counted *rows*, and UbuntuGuard carries several responses per prompt. The corrected inventory, after removing everything touched by DPO training:

| Pool | Size | Notes |
| :---- | ---: | :---- |
| African questions free of training | 126 | distinct `base_stem`s |
| African eval prompts | **192** | distinct `row_id`s — a question evaluated in 2-3 languages counts once per language |
| English control questions | **337** | `base_stem`s present in the English file and in **no** African file |

Per-language African eval prompts: Swahili 34, Ewe 32, Akan 29, Hausa 23, Zulu 22, Xhosa 21, Yoruba 11, Igbo 11, Luganda 7, Nyanja 2.

**Consequences, all of which shape how results get reported:**

1. **Use paired tests, not independent-proportion tests.** All four baselines (B1-B4) are evaluated on the *same* prompts, so the right instrument is McNemar's test on the discordant cases, not the Fisher's exact used in the Week 4 pilot. Pairing is what makes n=192 workable: it removes between-prompt variance rather than absorbing it into the noise. Reporting Fisher on paired data would understate the significance of a real effect.
2. **Do not report per-language RR%.** Nyanja has 2 eval prompts and Luganda 7. Aggregate results, and give the per-language counts in an appendix so the reader can see why no per-language claim is made. Grouping into high/low-resource bands is the most granularity this pool supports.
3. **The 337 English-only questions are a genuine, contamination-free control.** They appear in no African file, so nothing about them leaks through DPO training on African pairs. They give a clean measurement of the English-vs-African refusal gap — the phenomenon the whole project is premised on — at a sample size larger than the African side itself.
4. **The `translated` file doubles the evaluation conditions without new content.** Each of the 192 prompts can be run under an English policy and a localised policy. Those observations are not independent, so they support a paired within-prompt comparison of policy language, not a doubled n.

**Incidental measurement, relevant to H2:** AfriqueQwen's tokenizer has a 248,044-token vocabulary against roughly 151,000 for stock Qwen, and encodes this African-language corpus at about 4.1 characters per token — far better than the 2.5 a standard multilingual tokenizer would be expected to manage on these scripts. The CPT backbone's vocabulary extension is measurably doing its job, before any training has been run. Cheap to report and directly supportive of H2's premise.

## D2. `crosslingual`/`translated` are not the same axis as Native-DPO/Translated-DPO (proposal section 7, D1)

**Planned:** Translated-DPO = the same content as Native-DPO, machine-translated (NLLB/Google Translate) instead of expert-translated, isolating translation *quality* as the only variable for H1.

**Actual:** UbuntuGuard's `crosslingual` and `translated` test files are the paper's own **Cross-lingual (LRL-EN)** and **Full Localization (LRL-LRL)** evaluation conditions — dialogue is in the local language in both; the only difference is whether the *safety policy* itself is left in English or also localized. This is a policy-language axis, not a translation-quality axis, and neither file was constructed as a machine-translated counterfactual of the other.

**Resolution:** superseded by **D6** below. Neither option originally considered here — (a) build our own NLLB counterfactual, or (b) reframe H1 around UbuntuGuard's policy-language axis — is worth the cost, because a literature check showed the underlying question is already answered. H1 is demoted rather than re-operationalized. See D6.

## D3. License clarified, but from the paper, not the repo

**Planned:** proposal cites UbuntuGuard as CC BY 4.0.

**Actual:** the GitHub repo has no LICENSE file (checked directly). The paper itself states "License: CC BY 4.0" — so the proposal's original citation was likely correct, just not verifiable from the repo alone. Confirming directly with the authors (email, drafted in conversation, not stored here) rather than relying on the paper statement alone for a deliverable that may eventually be shared with the Supervisor or beyond.

## D4. UbuntuGuard's local-language content is itself machine-translated

**Planned:** Native-DPO would use content that is natively/expertly grounded in the target language, contrasted against a machine-translated (NLLB) counterfactual for H1.

**Actual:** per the paper's own methodology, the 155 domain experts authored the *original English* queries only — the translation into the 10 African languages was done with **Google Translate**, quality-filtered via automated GEMBA-MQM scoring plus validation from just 4 native speakers (Tumbuka dropped for failing the 70% quality threshold). UbuntuGuard's `crosslingual`/`translated` content is machine-translated content, not native/expert-authored content.

**Not a one-off:** HealthBench-Africa Extension turns out to be the same story — every row carries `translation_model: "gpt-4o-mini"` / `translation_provider: "openai"`, confirming it's LLM-translated too, with human validation explicitly described as "optional" and not covering all samples (its own Limitations section). Two of the five candidate D2/D3 datasets are now confirmed machine-translated rather than native — a systemic pattern across readily-available African-language safety/health resources, not something specific to UbuntuGuard. Strengthens the case for the dedicated dataset search below rather than assuming any existing "African-language" resource is automatically native-quality.

**Counter-examples found: Uhura-TruthfulQA and IrokoBench are genuinely native-translated.** Uhura: TruthfulQA translated into 6 languages by professional human translators, confirmed on its card. IrokoBench (checked the *full paper*, not just the collection prose, given how unreliable card prose has been elsewhere): recruited per-language coordinators who hired **paid professional translators**, with payment explicitly gated on a quality-review pass by the coordinator, plus a quantitative COMET-QE check — the most rigorous methodology found among all five datasets. Neither is a safety/preference dataset (TruthfulQA/NLI/MMLU/MGSM are factuality and reasoning tasks, D3/utility-side only), so neither resolves D1/D2 directly — but together they're strong evidence that genuinely native-quality resources exist for several of our target languages, and IrokoBench's methodology description is a good concrete bar to hold candidate DPO-safety sources to.

**Also corrects an initial hope:** IrokoBench's `-translate-test` variants (e.g. `afrimgsm-translate-test`) looked like they might be a ready-made native-vs-machine-translation pair, but they're actually the standard NLP "translate-test" paradigm — the African-language test set machine-translated (NLLB) *back into English*, not a second translation of the same content into the target language. Doesn't help with D2/D4.

**New candidate found: TukaBench (McGill-NLP, arXiv:2606.01322) may partially resolve D1 and the Hausa/Swahili gap.** A genuine jailbreak/safety benchmark (not general-knowledge like Uhura/IrokoBench) with harmful, benign, and culturally-adapted prompt sets covering Hausa and Swahili directly. Construction is hybrid MT + guaranteed human post-editing (two native speakers per language) — stronger validation than UbuntuGuard/HealthBench-Africa, though not fully native like IrokoBench/Uhura, and no raw pre-edit MT is released so it still doesn't give a native-vs-machine pair for D2/D4. Its prompts (not response pairs) could serve as a source for building our own on-policy DPO chosen/rejected pairs by generating completions from AfriqueQwen-Brut ourselves — see `Week5_Dataset_Description_Sheet.md` for full details. Same institution as our target model (McGill-NLP).

**Consequence:** compounds D2 — using UbuntuGuard's local-language files as "Native-DPO" would mean comparing one machine translation (Google Translate, quality-filtered) against another (our own NLLB), not "native vs. translated" as H1 intends. Reinforces option (a) from D2's resolution: keep UbuntuGuard's local-language files for supplementary RR% evaluation only, and build the actual H1 comparison from English-source content translated two ways (expert vs. machine) ourselves, if a genuinely native-quality source can't be found.

## D5. PASS/FAIL labels were never human-validated

**Planned:** treat UbuntuGuard's PASS/FAIL labels as reliable ground truth for DPO chosen/rejected pairs.

**Actual:** per the paper's own methodology, PASS/FAIL dialogues were generated entirely by Llama-3.1-405B/Qwen3-235B and passed through *automated structural checks only* — no human ever verified that a "FAIL" dialogue genuinely violates its policy, or that a "PASS" dialogue genuinely complies. Separately, translation quality was calibrated by a single native speaker per language on just 20 sampled pairs (80 total, 4 of 10 languages: Swahili, Igbo, Yoruba, Hausa) — the paper states this explicitly as a limitation ("relies on a single human validator for a subset of four languages due to the scarcity of available expert native speakers"), and the resulting 70% threshold was then applied automatically, with zero human validation, to the remaining six languages (Zulu, Xhosa, Ewe, Akan, Luganda, Nyanja).

**Consequence:** the DPO training signal itself (not just the language of the text) carries unverified label quality — a real risk to flag in our own risk/limitations section (proposal section 13) when results are written up, and a natural fourth question for the author email (added).

## D6. Primary claim recentred: H2 becomes the headline, H1 is demoted

**Planned:** H1 (native vs. translated alignment data) is the paper's headline claim — it is the proposal's title, its research question (section 3), and contribution C2. H2 (does the African-CPT backbone retain safety alignment better?) is a supporting hypothesis validated via baseline B3.

**Actual:** a literature check on H1's underlying question — *does the translation quality of safety alignment data affect safety transfer?* — found it already answered, in a recent systematic review that also names our actual gap.

> Lemofouet, V. D., Uzor, B. N., Anyanwu, P. C., Kapsa, D. B., Imam, S. H., Sahil, P. S., Oppong, A., Abdullahi, T., Siro, C., Abdulmumin, I., Yimam, S. M., & Muhammad, S. H. (2026). *LLM Safety Alignment in Low-Resource Languages: A Systematic Literature Review.* arXiv:2608.14626v1 [cs.CL]. Accepted at the LM4UC workshop, IJCAI 2026.

PRISMA 2020 methodology, ~1,500 papers screened to 50 included studies. Note that **Tassallah Abdullahi, UbuntuGuard's corresponding author, is a co-author** of this review — the same group defining the field's gaps also produced our primary dataset.

What the review establishes as settled, against H1:

- **LionGuard (Tan 2025):** "naively translated training data reduces performance."
- **Paul 2025:** 40,000 quality-filtered samples match or exceed 200,000 unfiltered ones for alignment.
- **Ge 2025:** proposes "toxicity-preserving translation," i.e. already starts from the premise that standard MT damages harmful intent.
- **CultureGuard:** natively grounded, culturally specific safety data outperforms translated-from-English data on non-English benchmarks.

The review's own summary: translation quality matters significantly, but intelligent filtering and preservation strategies mitigate the degradation. That is precisely the conclusion a reframed H1 would reach.

**A second finding closed the fallback option.** The idea of rescuing H1 by arguing that *preference pairs* (DPO) degrade differently under translation than *SFT targets* do — because MT may flatten the chosen/rejected contrast — does not hold as a novelty claim either. Multilingual safety DPO is an active area: MPO (Zhao 2025) minimises the safe/unsafe reward gap across languages without per-language pairs; Paul 2025 applies DPO after SFT on filtered Hindi data; Lim 2025 compares SFT, DPO and KTO for Singlish. The mechanism is not unexplored.

**What the review does *not* cover, verbatim:**

> *Continued pre-training:* not mentioned as a primary method. The review focuses on fine-tuning, mechanistic alignment, and data adaptation but does not discuss CPT backbones.

And among its explicit future directions:

> Validation of "parameter-efficient fine-tuning, data synthesis, and cross-lingual transfer" specifically "in the context of African languages."

That is `B3 (Qwen3.5-4B-Base + DPO)` vs `B4 (AfriqueQwen3.5-4B-50Langs + DPO)`, under QLoRA, on African languages — H2 exactly, named as an open gap by an independent systematic review rather than by our own judgment.

**Resolution:**

| | Proposal as approved | Recentred |
| :---- | :---- | :---- |
| Headline claim | H1 — native vs. translated | **H2 — does the CPT backbone retain alignment better?** |
| Control | H3 — utility / over-refusal | H3, unchanged |
| H1 | title and research question | secondary robustness axis, or dropped |

Concretely: one DPO dataset (UbuntuGuard's self-carved 401/100, D1), vary the backbone, report ΔRR and ΔORR. The pipeline is unchanged; the framing and the title change.

**Consequences:**

1. **The paper's title no longer matches its claim.** This must be raised with the Supervisor at the next supervision meeting — it is a larger deviation than D1-D5, which were data-level findings; this one touches the approved research question (section 3) and contribution C2.
2. **Simplifies the work, and removes a dependency we could not satisfy.** No NLLB translation arm and no hand-built TukaBench preference pairs are needed for the headline result. The recentring drops the reliance on a genuinely native data source — which D2/D4 established does not exist among our candidates — and rests on what we actually have: two backbones, one clean DPO set, and ~1,900 held-out African-language evaluation prompts.
3. **A1 (section 11) becomes more useful than A2.** The data-volume sweep (rescaled to 100/200/401 per D1) speaks directly to the recentred claim — how much preference data does each backbone need? A2 (linguistic diversity) is now secondary.
4. **The review is also our related-work anchor.** It cites UbuntuGuard as the "first African policy-based safety benchmark," so it situates both our gap and our dataset in one citation. Its acceptance at LM4UC (IJCAI) is also a concrete venue precedent for this line of work.

## D8. UbuntuGuard is a *guardian/classification* benchmark, not a generation benchmark

**Planned:** proposal section 9 defines Refusal Rate (RR%) as "the proportion of malicious or toxic queries for which the model produces an explicit refusal compliant with the safety policy", measured on text generated by the model under test.

**Actual:** that is not what UbuntuGuard measures. Read the authors' own `evaluate.py`, shipped in the repo. Their protocol is:

```
input  : <rules>{policy}</rules> + <transcript>{some agent's output}</transcript>
output : PASS or FAIL
score  : accuracy + macro F1 against the gold label
```

The model under evaluation is a **judge**, not an agent. The authors benchmark Llama-3.3-70B, Qwen and Gemma in that role at `temperature=0.0`. The transcripts are the material to be judged, not outputs of the model being tested.

This also explains something that looked wrong when inspecting examples: **the PASS responses are not refusals.** They are policy-compliant *helpful* answers — they engage the question, correct the misinformation and cite the relevant authority. On "can necessity excuse my driving without a licence?", the PASS answer explains Ghana's Road Traffic Act 2004 (Act 683) and the duress-of-circumstances argument; the FAIL answer offers false reassurance. A blanket refusal would score as unhelpful, not as safe. UbuntuGuard's axis is **policy compliance vs. violation**, not refusal vs. compliance — consistent with the systematic review calling it "the first African policy-based safety benchmark".

**Resolution: the guardian model is the measuring instrument, not the contribution.** Two framings were considered — training a guardian (classification) as the headline result, versus keeping the proposal's generation/alignment framing. The generation framing is the one that belongs to an alignment project: a guardian is a moderation classifier, and training one does not make a model more harmless, it builds a tool. So:

1. Train a guardian on UbuntuGuard's PASS/FAIL task. Its measured macro F1 becomes the **stated precision of our compliance detector**.
2. Use that guardian to score generated responses for the actual H2 result.
3. **The guardian runs on Qwen3.5-4B-Base, not on AfriqueQwen.** This is the critical design constraint. A judge sharing a backbone, tokenizer and training data with the agent it scores would systematically favour that agent — and since H2 compares a Qwen-Base agent (B3) against an AfriqueQwen agent (B4), an AfriqueQwen judge would inflate exactly the effect we are claiming. Building the judge on the *other* backbone makes any backbone-affinity bias work **against** the hypothesis, so the test is conservative.
4. **Three-way split at `base_stem` level:** judge-training / agent-training / evaluation, no stem shared between any two. Without this the judge would already have seen the transcripts it is asked to score. The splitting infrastructure from D1 handles this unchanged.

**Why this is worth doing rather than working around:** it converts the project's weakest methodological point into a measured quantity. We cannot read the ten target languages, so an unvalidated keyword detector would be indefensible — and the TukaBench paper warns that LLM-as-judge is unreliable in low-resource languages, without quantifying it. Here the detector's reliability is measured on held-out labelled data and reported as a number, so no claim in the results exceeds the precision of the instrument that produced it.

**Sequencing, so a result exists regardless of how much compute Week 6-7 affords:** build and measure the judge first (self-contained, uses the authors' own script, needs no new metric); then generation and scoring. If the second stage runs out of time, the judge and its measured F1 are still a deliverable, and generation moves to future work with the instrument already built.

## D9. Oriented on the Honest axis, with Harmless as the contrast

**Planned:** the Week 4 topic decision scoped the work to **Harmless only**, deliberately declining an Honest axis to avoid doubling the workload.

**Actual:** the data does not support a Harmless-only study, and never did. UbuntuGuard's own `theme` field, counted over the 2,307 African rows:

| Theme | Rows | Share | HHH axis |
| :---- | ---: | ---: | :---- |
| misinformation or disinformation | 1,032 | 45% | **Honest** |
| public interest | 463 | 20% | mixed |
| stereotypes | 394 | 17% | **Harmless** |
| specialized advice | 241 | 10% | **Honest** (expert accuracy) |
| hate speech | 177 | 8% | **Harmless** |

Translated into usable preference pairs and split:

| Subset | Pairs | Train | Eval |
| :---- | ---: | ---: | ---: |
| Honest (misinformation + specialized advice) | 597 | **475** | 122 |
| Harmless (stereotypes + hate speech) | 273 | **216** | 57 |
| public interest (ambiguous) | 219 | 175 | 44 |
| all themes | 1,089 | 869 | 220 |

**Harmless-only leaves 216 training pairs and 57 evaluation pairs across ten languages** — Luganda has 5 pairs in total, Nyanja 6. That is not a study.

**And the other datasets cannot fill the Harmless side.** Checked each: AfriHate ships classification labels (Hate/Abusive/Normal) with no responses to contrast; TukaBench ships prompts with no responses at all. Neither yields preference pairs without generating and labelling responses ourselves — which reopens the judge problem, for the thinner axis. Uhura-TruthfulQA, by contrast, ships `best_answer` / `incorrect_answers` and is a ready-made **Honest** pair source. The data ecosystem supports training on Honest and evaluating on both; it does not support the reverse.

**Resolution: train on the Honest axis, evaluate on both axes.**

- **Train:** UbuntuGuard misinformation + specialized advice (African-grounded), and separately Uhura-TruthfulQA (Western-grounded, human-translated) — kept apart, not pooled, per the orthogonality noted in the dataset sheet.
- **Evaluate Honest:** held-out UbuntuGuard misinformation, held-out Uhura.
- **Evaluate Harmless:** AfriHate (macro F1), TukaBench (refusal on `afri-jbb-harm`, over-refusal on `afri-jbb-benign`), held-out UbuntuGuard stereotypes/hate speech. All three are strong *evaluation* sets even though none can train.

**The sharpened question, and why it has a mechanism behind it:**

> Does African-language continued pre-training improve *truthfulness* alignment more than *harm-avoidance* alignment?

Honest failures are **knowledge** failures — answering correctly about Yoruba Asaro, or about what Ghanaian law actually permits, requires facts about that place, in that language, which is precisely what 35.5B tokens of African continued pre-training inject. Harmless failures are **behaviour** failures — refusing hate speech is a learned response pattern that transfers more readily from English alignment because it needs less local knowledge. **Prediction: CPT helps more on Honest than on Harmless.** Falsifiable, and it connects to the mechanism the systematic review names explicitly (fragmented tokenisation and weak semantic representation in the target language).

**Relation to the Week 4 decision, stated plainly for supervision:** this reintroduces the Honest axis that was declined. The difference is that Honest was declined as a *second body of work* — two topics, double the effort. Here it is a **stratification of a single result**: same data, same models, same training runs, with the existing `theme` field used to split the reporting. The marginal cost is close to zero. It is still a change of orientation against an approved proposal and must be raised alongside D6.

## Search prompt for finding a complementary dataset (for Google Deep Search / similar)

Targets the two open gaps this document tracks: a genuine native-vs-machine-translation counterfactual for H1 (D2/D4), and more African-language safety training volume than UbuntuGuard's unreleased train split (D1).

> I'm looking for datasets to fine-tune and evaluate language models on AI safety behavior (refusal of harmful requests, hate-speech/toxicity moderation) in African languages, for a DPO (preference-pair) training setup. I need candidates that satisfy as many of these as possible:
>
> 1. Contains paired or comparable "safe/compliant" vs. "unsafe/violating" responses (preference pairs, PASS/FAIL labels, or chosen/rejected pairs) to safety-relevant prompts — not just single-label classification data.
> 2. Covers at least one of: Hausa, Yoruba, Swahili, Nigerian Pidgin, Igbo, Zulu, Xhosa, Akan, Ewe, Luganda, Amharic.
> 3. Critically: the African-language content should be **natively authored or professionally/expert-translated**, not solely machine-translated (e.g. via Google Translate or NLLB) with only light automated quality filtering — I need to be able to tell which one it is from the dataset's own documentation.
> 4. Labels/annotations should be **human-validated** (not purely LLM-generated and structurally checked), ideally with a description of who validated them and how many people were involved.
> 5. Publicly available (Hugging Face, GitHub, or similar), with a clearly stated license (prefer CC BY, CC BY-SA, MIT, or Apache 2.0), published 2023 or later.
> 6. Reasonable scale for LLM fine-tuning — at least several hundred examples per language, ideally low thousands.
>
> For each candidate you find, report: name, link, exact language coverage, how it was constructed (native vs. machine-translated, human-validated or not), size, license, and how confident you are in each of these claims based on what the source actually states (not what a paper's abstract implies).

Look for candidates that could either replace or supplement UbuntuGuard's `crosslingual`/`translated` test files for the H1 comparison specifically — priority is finding something that's *actually* native-vs-machine-translated, which UbuntuGuard turned out not to be (D2/D4).

## Dataset composition, for reference (Table 3 of the paper)

| Language | Train | Test | Country | #Themes | #Domains |
| :---- | ---: | ---: | :---- | ---: | ---: |
| Akan | 1,512 | 313 | Ghana | 5 | 7 |
| Ewe | 1,681 | 345 | Ghana | 5 | 7 |
| Hausa | 1,656 | 278 | Nigeria | 4 | 7 |
| Igbo | 1,854 | 98 | Nigeria | 4 | 7 |
| Luganda | 642 | 74 | Uganda | 4 | 5 |
| Nyanja | 1,171 | 39 | Malawi | 4 | 4 |
| Swahili | 1,899 | 435 | Kenya | 5 | 6 |
| Xhosa | 1,452 | 263 | South Africa | 5 | 7 |
| Yoruba | 1,852 | 144 | Nigeria | 4 | 7 |
| Zulu | 1,473 | 318 | South Africa | 5 | 7 |
| English | 13,532 | 2,449 | All countries | 5 | 7 |

Themes: Misinformation, Public Interest, Stereotypes, Hate Speech, Expert Advice. Domains: Health, Education, Legal, Politics, Culture, Religion, Finance, Labor. Source: 155 domain experts (Amplify Initiative) generated 8,091 original queries. **Only the Test column (4,756 examples total) has been released** — the Train column (28,724 examples total, English alone at 13,532) is what D1 above is about. Corrects an earlier, rougher note ("1,171-13,532/language") — the actual African-language train range is 642 (Luganda) to 1,899 (Swahili); 13,532 is English only.
