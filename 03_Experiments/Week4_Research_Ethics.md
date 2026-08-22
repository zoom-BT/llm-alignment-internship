# Week 4 — Research Ethics: Honest & Harmless Design

Applying the last two of InstructGPT's HHH principles (Helpful, **Honest**, **Harmless**) to the research design itself, not just to the models being evaluated — required explicitly by the internship agreement's Article 12 ("Research concerning African communities, languages, societies, or cultures shall avoid unsupported generalizations", and mandates documenting limitations of data/annotator representativeness, geographic and cultural coverage).

## Honest

**Ground truth is sourced, not asserted from memory.** Every fact in `pilot_questions.json` was verified via web search against a citable source (`source_url` field) before being included — deliberately, because using an LLM (me) to author "ground truth" about an underrepresented topic from memory alone would risk baking the very failure mode under study (hallucination on underrepresented regions) directly into the measurement instrument.

**The comparison design avoids manufacturing a predetermined conclusion.** Every African fact is paired with a non-African control on the *same question type* (first post-independence leader, regional-org founding year, anti-colonial battle, etc.), matched as closely as feasible on general popularity — not comparing "Africa" against arbitrarily well-known Western facts, which would trivially "prove" a gap that's really just about obscurity, not region.

**Limitations to be stated explicitly in the full proposal, not glossed over:**
- Small sample (44 questions) — results are a preliminary signal, not a statistically definitive claim
- Single verifier (the intern) — no inter-annotator agreement measured; mitigated by choosing unambiguous, single-answer factual questions (dates, names) rather than interpretive ones
- Wikipedia's own documented coverage gap for African topics means even this "neutral" data source carries an upstream bias — a limitation of the measurement method, disclosed rather than hidden
- Popularity-matching is approximate (based on question-type analogy, not a formal metric like Wikipedia pageviews at question-construction time) — a methodological refinement to flag for the full proposal if time permits

## Harmless

**Category balance was audited, not assumed.** Of the 22 African-region questions, only 3 involve conflict/violence (Rwandan genocide, the Biafra war, the Berlin Conference's colonial partition) — the remaining 19 cover institutions, culture, and political history (universities, regional development banks, continental parliaments, literature, independence, first female heads of state). A pilot set dominated by conflict topics would itself risk reinforcing a reductive narrative about the region under study, independent of what the models actually say.

**Terminology was reviewed for delegitimizing framing.** The Mau Mau/Dedan Kimathi question was originally categorized as `"insurgency_leader"` — corrected to `"independence_movement_leader"`, since "insurgency" carries a connotation of illegitimate rebellion, when the historical context is an anti-colonial independence struggle (the same correction applies symmetrically to its matched control, the Malayan Emergency's Chin Peng, for consistency).

**Findings will be attributed to the training data and the AI system, not to the region or its people.** Any observed hallucination gap reflects underrepresentation of African topics in these models' pretraining corpora — a property of the models and the data pipelines that produced them. The write-up must not imply, even by omission, that this reflects anything about the intrinsic knowability, importance, or documentation of African history and institutions — the Wikipedia coverage-gap literature already establishes that the gap is a data-availability artifact, not a reflection of the underlying facts' significance.

**No private or sensitive data involved.** All entities are public figures, public institutions, or historical events already extensively documented in public, citable sources — no personal data, no vulnerable individuals, nothing requiring the ethics/IRB-style review the contract flags for human-subjects work (Article 12's human-evaluation approval clause does not apply here, since ground-truth verification is done by the intern against public sources, not via external human annotation).

## What this means for the full Week 4 proposal
These considerations belong in the proposal's "main risks and limitations" section, not as an afterthought — and the category-balance audit and terminology review should be treated as part of the experimental protocol (repeated if the question set is expanded for the full study), not a one-time check on this pilot alone.
