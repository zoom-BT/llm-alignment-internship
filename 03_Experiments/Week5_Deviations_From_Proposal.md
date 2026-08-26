# Week 5 — Deviations From the Approved Proposal

The approved proposal (`04_Weekly_Reports/Week_04_Research_Proposal.md`, approved 2026-08-25) is **not being edited** to reflect what's below — per contract discipline, a supervisor-approved research design stays as-is; deviations discovered during execution are logged separately and reported alongside results, not silently folded back into the original document.

---

## D1. UbuntuGuard has no training split (proposal section 7, D1)

**Planned:** train Native-DPO directly on UbuntuGuard's training split (PASS→chosen, FAIL→rejected).

**Actual:** confirmed via the repo's full git history (5 commits, `github.com/hemhemoh/UbuntuGuard`) that no training file has ever been committed — only three test-split JSONL files exist, added in the latest commit (2026-04-15). The paper (arXiv:2601.12696v3) reports train/test split sizes in its Table 3 and doesn't state whether guardian models were trained on that split or when/whether it will be released publicly.

**Resolution:** self-carved a per-language stratified 80/20 split of the 501 clean PASS/FAIL pairs in the released test data (401 train / 100 eval, no `row_id` overlap between sides) — see `Week5_Dataset_Description_Sheet.md` for the full table. `config.yaml`'s `dpo.train_size` corrected from the proposal's 1000 to 401 accordingly.

**Consequence for the proposal's A1 ablation (section 11):** the 250/500/1000-example sweep is no longer reachable as written — 401 is the ceiling with this data. Not changing the proposal text; flagging it here so it's addressed explicitly when results are written up, or if a training split arrives from the authors before Week 6.

## D2. `crosslingual`/`translated` are not the same axis as Native-DPO/Translated-DPO (proposal section 7, D1)

**Planned:** Translated-DPO = the same content as Native-DPO, machine-translated (NLLB/Google Translate) instead of expert-translated, isolating translation *quality* as the only variable for H1.

**Actual:** UbuntuGuard's `crosslingual` and `translated` test files are the paper's own **Cross-lingual (LRL-EN)** and **Full Localization (LRL-LRL)** evaluation conditions — dialogue is in the local language in both; the only difference is whether the *safety policy* itself is left in English or also localized. This is a policy-language axis, not a translation-quality axis, and neither file was constructed as a machine-translated counterfactual of the other.

**Resolution (pending):** either (a) keep the proposal's original plan — take UbuntuGuard's English-source content and produce our own NLLB-translated counterfactual specifically for H1, using `crosslingual`/`translated` only for supplementary Refusal Rate evaluation, not as the H1 comparison itself; or (b) reframe H1's operationalization around the policy-language axis UbuntuGuard actually provides. Not decided yet — needs a decision before Week 6's DPO training runs, since it changes what H1 actually measures.

## D3. License clarified, but from the paper, not the repo

**Planned:** proposal cites UbuntuGuard as CC BY 4.0.

**Actual:** the GitHub repo has no LICENSE file (checked directly). The paper itself states "License: CC BY 4.0" — so the proposal's original citation was likely correct, just not verifiable from the repo alone. Confirming directly with the authors (email below) rather than relying on the paper statement alone for a deliverable that may eventually be shared with the Supervisor or beyond.

---

## Email to the UbuntuGuard authors (draft — not sent)

To: Tassallah Abdullahi <tassallahabdullahi@brown.edu> (corresponding author, per arXiv:2601.12696v3)

> Subject: UbuntuGuard — question about the training split and license
>
> Dear Dr. Abdullahi,
>
> I'm a research intern using UbuntuGuard for a project on DPO safety alignment for African-language foundation models, and I have two quick questions after working with the released repository (github.com/hemhemoh/UbuntuGuard).
>
> 1. The paper's Table 3 reports train/test split sizes per language, but the repository currently only contains the test-split files (`Ubuntu_guard_test_*.jsonl`). Is the training split planned for public release, and if so, is there a timeline? If it isn't being released, I'd appreciate confirmation so I can plan around a self-constructed split of the test data instead.
> 2. The paper states the dataset is released under CC BY 4.0, but the repository doesn't currently include a LICENSE file. Could you confirm this is still the intended license, or point me to where it's formally declared?
>
> Thank you for making this benchmark available — it's been very useful.
>
> Best regards,
> Balbino Tchoutzine

**Notes on the draft:** kept short and specific (two concrete questions, not a general request); addressed to the corresponding author listed on the paper rather than the GitHub commit author, since that's the more standard channel for this kind of question. Not sent — for review/editing before you send it yourself.
