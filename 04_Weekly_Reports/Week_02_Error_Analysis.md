# Week 2 — Error Analysis (Qualitative Review of 20 Examples)

**Model:** Week 2 fine-tuned checkpoint (LR 2e-5, warmup+cosine, early stopping) vs. `Qwen/Qwen2.5-0.5B` baseline
**Raw data:** [`results/qualitative_examples.json`](../results/qualitative_examples.json) — all 20 prompts, references, and both models' completions in full.

## Methodology
20 examples were drawn from the held-out **test** split (never seen in training), stratified across Dolly-15k's 8 categories (2-3 per category) so no single task type dominates the sample. For each, both the baseline and the Week 2 fine-tuned model generated a completion from the identical chat-templated prompt, using **greedy decoding** (`do_sample=False`) so the comparison is deterministic rather than noisy across runs.

## Summary

| Outcome | Count | Examples |
| :--- | :--- | :--- |
| ✅ Clear improvement | 6 | electricity bill, Tassa/Sitar, audiologists, lacavore diet, baseball team, Dune spice |
| ❌ Regression (fine-tuned worse than baseline) | 5 | movie list, GA-without-UI, US presidents, Sweden economy, "plants are green" |
| ⚠️ Suspected memorization | 2 | cricket rules, cardiac surgery |
| 🤷 Knowledge gap, unaffected by fine-tuning | 3 | Alexander's battles, Eric Brewer, Instagram followers |
| 🤷 Style learned, fact still wrong | 2 | House Tyrell, tree nuts |
| = Comparable / ambiguous | 2 | movie classification, electronic music |

## Findings

### 1. Instruction-following (format compliance) improved clearly
The fine-tuned model is consistently better at respecting explicit format instructions the baseline ignores — e.g. "in a concise bulleted list" (audiologists) is only honored by the fine-tuned model; numbered-list requests (electricity bill) come back tighter and on-topic instead of trailing off mid-sentence at the baseline's token limit. This is the clearest signal of *learning a response style* rather than new knowledge.

### 2. Repetition/degeneration loops are reduced, not eliminated
The baseline degenerates into infinite loops on 4/20 prompts (Tassa/Sitar, lacavore diet, baseball team, Eric Brewer) — repeating a token, a phrase, or leaking a `system` role artifact indefinitely. The fine-tuned model fixes 3 of those 4, but **introduces its own loop on 2 other prompts** it hadn't previously failed on (movie list → hallucinated "Godfather Part III...VIII"; GA-without-UI → the same sentence repeated ~10 times). Net effect: the failure mode persists at roughly the same rate (2/20 = 10%), just on different prompts. **This is the most actionable finding**: these degenerate completions have very high per-token loss on repeated/nonsensical continuations, which is a plausible partial explanation for why test perplexity (14.61) still sits above the baseline (13.92) despite the overfitting fix.

### 3. Regressions concentrate in information-extraction and closed-book factual tasks
On both information_extraction examples given real source context (US presidents, Sweden economy), the fine-tuned model answers *worse* than the baseline — hallucinating names not in the passage, or answering a different, easier question than the one asked. The baseline, despite being wordier, stays closer to the source text (it partly regurgitates the passage, which happens to contain the right answer). This suggests the SFT run may be trading some context-grounding for a terser, more "confident-sounding" style — worth watching in Week 3.

### 4. Knowledge gaps are a model-capacity ceiling, not a fine-tuning failure
On niche factual recall (Eric Brewer, Alexander's battles, Instagram follower counts), *both* models hallucinate confidently and similarly. A 0.5B model's parametric knowledge is simply too small to hold this; no amount of instruction-tuning on 12k examples adds world knowledge it doesn't already have from pretraining. The Instagram case is notable: baseline and fine-tuned produce the *same* degenerate "@elonmusk" hallucination — proof the pattern is inherited from the base model, not introduced or fixed by SFT.

### 5. Style transfer without knowledge transfer, isolated cleanly
"What are the words of House Tyrell?" is the cleanest example in the set of the Week 2 theoretical concept *memorizing vs. learning a response style vs. acquiring a new capability*: the baseline hallucinates a whole unrelated biography; the fine-tuned model answers in the exact expected format (a short quoted motto) but with the wrong motto. The **style** of a terse, quoted-answer response was learned; the **fact** was not — because it was never encoded in the base model's weights to begin with.

### 6. Two cases of suspected verbatim memorization
Cricket rules and cardiac surgery summaries come back nearly word-for-word identical to the reference. Both are in the **test** split (excluded from training by the fixed seed=42 split), so this is unlikely to be train/test leakage. The more likely explanation: both passages are Wikipedia-style boilerplate that Qwen's base *pretraining* corpus almost certainly already contains verbatim — fine-tuning simply made the model more willing to reproduce known text directly as an answer, rather than teaching it that text for the first time.

## Conclusion
Week 2's corrections (lower LR, validation-driven early stopping) fixed the catastrophic overfitting from Week 1, and produced a model that is measurably better at following explicit formatting instructions. It did not fully eliminate generation-time degeneration (repetition loops), and shows a new, narrower regression on context-grounded extraction tasks. Both are natural candidates for the loss-masking investigation (`Week2_Checklist.md`, investigation avenue #2) if pursued in a later week.
