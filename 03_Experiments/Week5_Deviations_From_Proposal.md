# Week 5 — Deviations From the Approved Proposal

The approved proposal (`04_Weekly_Reports/Week_04_Research_Proposal.md`, approved 2026-08-25) is **not being edited** to reflect what's below — per contract discipline, a supervisor-approved research design stays as-is; deviations discovered during execution are logged separately and reported alongside results, not silently folded back into the original document.

---

## D1. UbuntuGuard has no training split (proposal section 7, D1)

**Planned:** train Native-DPO directly on UbuntuGuard's training split (PASS→chosen, FAIL→rejected).

**Actual:** confirmed via the repo's full git history (5 commits, `github.com/hemhemoh/UbuntuGuard`) that no training file has ever been committed — only three test-split JSONL files exist, added in the latest commit (2026-04-15). The paper (arXiv:2601.12696v3) reports train/test split sizes in its Table 3, but its only availability language ("Our benchmark and code can be found online," abstract + footnote 1) never explicitly commits to releasing the training split specifically — checked the abstract, introduction, ethics, limitations, acknowledgments, and appendix, none clarify this. Not a broken promise, just genuinely ambiguous — hence asking directly rather than assuming either way.

**Resolution:** self-carved a per-language stratified 80/20 split of the 501 clean PASS/FAIL pairs in the released test data (401 train / 100 eval, no `row_id` overlap between sides) — see `Week5_Dataset_Description_Sheet.md` for the full table. `config.yaml`'s `dpo.train_size` corrected from the proposal's 1000 to 401 accordingly.

**Consequence for the proposal's A1 ablation (section 11):** the 250/500/1000-example sweep is no longer reachable as written — 401 is the ceiling with this data. Not changing the proposal text; flagging it here so it's addressed explicitly when results are written up, or if a training split arrives from the authors before Week 6.

## D2. `crosslingual`/`translated` are not the same axis as Native-DPO/Translated-DPO (proposal section 7, D1)

**Planned:** Translated-DPO = the same content as Native-DPO, machine-translated (NLLB/Google Translate) instead of expert-translated, isolating translation *quality* as the only variable for H1.

**Actual:** UbuntuGuard's `crosslingual` and `translated` test files are the paper's own **Cross-lingual (LRL-EN)** and **Full Localization (LRL-LRL)** evaluation conditions — dialogue is in the local language in both; the only difference is whether the *safety policy* itself is left in English or also localized. This is a policy-language axis, not a translation-quality axis, and neither file was constructed as a machine-translated counterfactual of the other.

**Resolution (pending):** either (a) keep the proposal's original plan — take UbuntuGuard's English-source content and produce our own NLLB-translated counterfactual specifically for H1, using `crosslingual`/`translated` only for supplementary Refusal Rate evaluation, not as the H1 comparison itself; or (b) reframe H1's operationalization around the policy-language axis UbuntuGuard actually provides. Not decided yet — needs a decision before Week 6's DPO training runs, since it changes what H1 actually measures.

## D3. License clarified, but from the paper, not the repo

**Planned:** proposal cites UbuntuGuard as CC BY 4.0.

**Actual:** the GitHub repo has no LICENSE file (checked directly). The paper itself states "License: CC BY 4.0" — so the proposal's original citation was likely correct, just not verifiable from the repo alone. Confirming directly with the authors (email, drafted in conversation, not stored here) rather than relying on the paper statement alone for a deliverable that may eventually be shared with the Supervisor or beyond.

## D4. UbuntuGuard's local-language content is itself machine-translated

**Planned:** Native-DPO would use content that is natively/expertly grounded in the target language, contrasted against a machine-translated (NLLB) counterfactual for H1.

**Actual:** per the paper's own methodology, the 155 domain experts authored the *original English* queries only — the translation into the 10 African languages was done with **Google Translate**, quality-filtered via automated GEMBA-MQM scoring plus validation from just 4 native speakers (Tumbuka dropped for failing the 70% quality threshold). UbuntuGuard's `crosslingual`/`translated` content is machine-translated content, not native/expert-authored content.

**Consequence:** compounds D2 — using UbuntuGuard's local-language files as "Native-DPO" would mean comparing one machine translation (Google Translate, quality-filtered) against another (our own NLLB), not "native vs. translated" as H1 intends. Reinforces option (a) from D2's resolution: keep UbuntuGuard's local-language files for supplementary RR% evaluation only, and build the actual H1 comparison from English-source content translated two ways (expert vs. machine) ourselves, if a genuinely native-quality source can't be found.

## D5. PASS/FAIL labels were never human-validated

**Planned:** treat UbuntuGuard's PASS/FAIL labels as reliable ground truth for DPO chosen/rejected pairs.

**Actual:** per the paper's own methodology, PASS/FAIL dialogues were generated entirely by Llama-3.1-405B/Qwen3-235B and passed through *automated structural checks only* — no human ever verified that a "FAIL" dialogue genuinely violates its policy, or that a "PASS" dialogue genuinely complies. Separately, translation quality was calibrated by a single native speaker per language on just 20 sampled pairs (80 total, 4 of 10 languages: Swahili, Igbo, Yoruba, Hausa) — the paper states this explicitly as a limitation ("relies on a single human validator for a subset of four languages due to the scarcity of available expert native speakers"), and the resulting 70% threshold was then applied automatically, with zero human validation, to the remaining six languages (Zulu, Xhosa, Ewe, Akan, Luganda, Nyanja).

**Consequence:** the DPO training signal itself (not just the language of the text) carries unverified label quality — a real risk to flag in our own risk/limitations section (proposal section 13) when results are written up, and a natural fourth question for the author email (added).

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
