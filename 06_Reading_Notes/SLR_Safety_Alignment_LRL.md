# LLM Safety Alignment in Low-Resource Languages: A Systematic Literature Review

- **Link:** arXiv:2608.14626v1 [cs.CL], 20 Jul 2026. PDF read in full: `afrique-safety-dpo/notebooks/2608.14626v1.pdf`
- **Read on:** 2026-08-26
- **Authors:** Lemofouet, Uzor, Anyanwu, Kapsa, Imam, Sahil, Oppong, **Abdullahi**, Siro, Abdulmumin, Yimam, Muhammad — AIMS Cameroon, Bayero University Kano, Brown, CWI, Pretoria, Hamburg, Imperial College London
- **Venue:** accepted at the LM4UC workshop, IJCAI 2026
- **Why it matters here:** it defines the gap our recentred H2 occupies (see `03_Experiments/Week5_Deviations_From_Proposal.md`, D6), and Tassallah Abdullahi — UbuntuGuard's corresponding author, whose dataset we train on — is a co-author.

## Problem

Safety alignment is built for English and does not survive translation into low-resource languages. The review formalises this with PRISMA 2020: ~1,500 papers from Semantic Scholar, arXiv and OpenAlex, deduplicated to 1,300, filtered to 242, screened to 70, then two rounds of manual revision down to **50 studies**. Organised around four research questions: alignment methods (RQ1), risks and cultural harms (RQ2), datasets and benchmarks (RQ3), cross-lingual transfer factors (RQ4).

## Method — the taxonomy (Figure 2)

Three families, by *where* the alignment happens:

1. **Culturally grounded data adaptation** — fix the data.
2. **Cross-lingual transfer and objective optimisation** — fix the training objective.
3. **Mechanistic and parameter-level alignment** — edit the model internals directly.

## Configurations that worked elsewhere

This is the section to mine. Grouped by what it tells us for our own runs.

### Systems that succeeded at *our* data scale

| System | Data scale | Recipe | Reported result |
| :---- | :---- | :---- | :---- |
| **ConsistentGuard** (Chen et al. 2025, MRL workshop) | **1,000 samples** | SFT → GRPO → CAO (Constrained Alignment Optimization) | Outperforms *larger* classifiers; interpretable reasoning chains |
| **Aligning** (Paul et al. 2025, BHASHA workshop, Hindi) | 40k filtered | Translate preference data with Llama-3.1-405B, filter with FAITH quality metrics, then **SFT → DPO** | **40k filtered matches or exceeds 200k unfiltered** |
| **MrGuard** (Yang et al. 2025, EMNLP) | synthetic | **SFT with QLoRA** → GRPO-based RL, reasoning chains not binary labels | **+15% average F1** across 8 languages, robust to code-switching |
| **LionGuard 2** (Tan et al. 2025, EMNLP demo) | — | Lightweight localised moderation, Singapore-specific harm categories | Beats commercial APIs on 17 benchmarks; **naively translated training data reduces performance** |
| **CultureGuard** (Joshi et al. 2025, IJCNLP-AACL) | 386k, 9 langs | generate → filter → validate with native speakers → **LoRA** guard model | Beats models trained on translated English; zero-shot transfer to unseen languages |
| **SEALGuard** (Shan et al. 2025, AIware) | 266k prompts, 9 langs | **LoRA** fine-tune on SEALSBench | **+48% Defence Success Rate** over LlamaGuard |

**The line that matters most for us:** ConsistentGuard reached publishable results on **1,000 samples**. Our pool is 869 pairs. Small data is not, by itself, a reason this cannot be a workshop paper — and ConsistentGuard was itself a workshop paper.

### Objectives other than DPO, worth knowing before Week 6

- **MPO — Multilingual reward gaP Optimization** (Zhao et al. 2025, ACL main). Minimises the reward gap between safe and unsafe outputs *directly across languages*, so it does **not** require `(chosen, rejected)` pairs in every target language. Reported to consistently outperform RLHF and DPO baselines on cross-lingual safety benchmarks **under noisy conditions**. Relevant to us because D5 established our PASS/FAIL labels were never human-validated — "noisy" describes our labels precisely.
- **KTO and KTO-S** (Lim et al. 2025, LM4UC workshop, Singlish). Compares SFT, DPO and KTO where preference pairs are hard to collect. **SFT+KTO reduced toxicity by 99%**; KTO-S is an improved regularisation strategy that **stabilises fine-tuning under data scarcity**. KTO needs only a binary good/bad signal, not pairs — which is what UbuntuGuard's PASS/FAIL labels natively are, before we pair them up.
- **MLC loss** (Bu et al. 2026, ICLR). Multi-Lingual Consistency: enforces directional consistency between multilingual representation vectors in a single training update, aligning several languages at once without response-level supervision in each target language.

### Training-free / mechanistic alternatives (no GPU training at all)

- **Sparse Weight Editing** (Liang et al. 2026): safety capability is concentrated in a sparse weight subset; a closed-form linear transformation projects low-resource representations into the safety subspace, **no gradient computation**. Validated on 8 languages across Llama-3 and Qwen-2.5.
- **Layer-wise Safety Feature Transplant** (Shin & Hwang 2026, EACL): activation analysis finds safety-critical layers in a high-resource aligned model and transplants them into a low-resource expert. **Training-free**; gains on MultiJail while preserving MMLU, BELEBELE, MGSM.
- **Soteria** (Banerjee et al. 2025, EMNLP Findings): gradient-based attribution identifies language-specific attention heads responsible for harmful outputs and steers only those. Small parameter fraction, preserves language quality.

## Warnings that change our protocol

Four findings here are direct threats to our design, not background reading.

1. **Benign fine-tuning alone degrades safety.** Upadhayay & Behzadan (2025), *Tongue-tied: Breaking LLMs safety through new language learning*: fine-tuning aligned models on new or synthetic languages degrades safety **even with benign data**. "Introducing new linguistic domains without safety recalibration may reduce robustness." → This is a *confound* for H2: AfriqueQwen's 35.5B-token African CPT may itself have eroded stock Qwen's safety, so B1's baseline refusal rate is not a neutral starting point. It is also, read the other way, precisely the mechanism H2 proposes to repair. Must be discussed either way.
2. **Format compliance is not refusal.** Pattnayak & Chowdhuri (2026a, IndicJR, EACL industry track): contract-bound prompts in JSON format **inflate refusal counts without actually preventing jailbreaks**. → Our RR% detector must not score a well-formed, policy-shaped response as a refusal. This is a concrete requirement for Thursday's metric implementation.
3. **Ambiguous boundary refusals actively hurt.** Zhang et al. (2026a): unfiltered distillation *raised* jailbreak success by up to **16.6 points**, because ambiguous "boundary" refusals confuse the student; filtering mitigates it. → Analogous risk in our data: unvalidated PASS labels (D5) that sit near the boundary may teach the wrong thing. Argues for inspecting a sample of PASS/FAIL pairs before training, not after.
4. **The evaluation itself is suspect, not just the models.** Vajjala (2025): annotation discrepancies and culturally biased benchmarks contribute to inadequate evaluation measures. Consistent with what we found independently across six dataset cards.

## Key Results

- Yong et al. (2023): translating harmful prompts into low-resource languages achieves a **79% jailbreak success rate on GPT-4**, against **<15%** for high-resource languages. Figure 3(A) puts low-resource failure at 79%, mid-resource ~30%, high-resource 11% — a **seven-fold** gap.
- Deng et al. (2024): low-resource languages carry ~**3x** the likelihood of harmful content.
- Song et al. (2025): code-switching bypasses reach **67.23%** on GPT-3.5 and **40.34%** on GPT-4 — and the review notes code-switching is a normal communicative practice in African contexts, not an adversarial construct.
- Figure 4: English appears in ~55 studies. Swahili and Hausa sit around 5, Zulu and Yoruba around 3, Igbo and Nigerian Pidgin at 1-2. The under-representation is quantified, and citable as motivation.

## Cross-lingual transfer factors (RQ4) — the mechanism behind H2

Verbatim, section 7:

> "Morphologically rich languages and underrepresented scripts often suffer from **fragmented tokenization** and weaker semantic representations, reducing the reliability of safety reasoning and refusal behavior."

This names tokenisation fragmentation as a *mechanism* for safety failure. Our incidental measurement — AfriqueQwen's 248,044-token vocabulary encoding this corpus at ~4.1 characters/token — is a direct probe of exactly that mechanism, and links our H2 to a named causal story rather than a bare correlation.

Related, and cheap to run as supporting analysis:
- **Verma & Bharadwaj (2025):** safety-relevant features cluster around high-resource regions of the latent space.
- **Wang et al. (2026), *Refusal direction is universal across safety-aligned languages*:** a shared directional structure in refusal behaviour across languages.
- **Zhang et al. (2026b), *Who transfers safety?*:** identifies cross-lingual shared safety neurons that can be selectively targeted.

## Limitations

The review's own: restricted to English-language studies from major databases; grouping languages into broad regional categories may obscure real linguistic differences; may under-represent locally published or very recent work.

## Takeaway

**The single most useful sentence in the paper, from the Discussion:**

> "Techniques like parameter-efficient fine-tuning, data synthesis, and cross-lingual transfer might be helpful, yet they are **poorly validated in the context of the African languages**. As long as the pre-trained models lack coverage of these languages, the gains brought by such techniques are rather marginal. Partly because, at the pre-training stage, these models already under-represent the languages, which makes recovery of any kind of multilingual representation impossible."

The review states the blocker as a *premise*: PEFT alignment gains stay marginal **because** pre-training under-represents these languages. Our setup is the instrument that tests that premise directly — AfriqueQwen3.5-4B-50Langs does **not** lack the coverage, having had 35.5B tokens of African continued pre-training. H2 asks whether removing the stated blocker makes PEFT safety alignment work.

That is a sharper framing than "we compare two backbones": we are testing the causal claim the field's own systematic review rests on, using the model that did not exist when that claim was made. Combined with the review's explicit note that **continued pre-training is not covered as a method**, and its future-work call to validate PEFT and cross-lingual transfer specifically in African languages, this is as clean a gap statement as a workshop paper needs.

## New leads to follow up

- **LSR** (Faruna 2026, arXiv:2603.19273), *Linguistic safety robustness benchmark for low-resourced West African languages* — measures **cross-lingual refusal degradation** in Yoruba, Hausa, Igbo and Igala. This is our RR% metric, already operationalised for African languages, and it was not among the six datasets surveyed so far. Add to `Week5_Dataset_Description_Sheet.md` once verified against its own source.
- **Uhura** (Bayes et al. 2024, arXiv:2412.00948) — already in the dataset sheet, but the review frames it as covering safety constraints, not only truthfulness. Worth re-reading the paper on that point.
- **ML-Bench & Guard** (Zhao et al. 2026, arXiv:2605.00689) — policy-grounded multilingual safety benchmark over 14 languages, built on regional regulations. Same policy-grounded design as UbuntuGuard.
- **PolyGuard** (Kumar et al. 2025, COLM) — multilingual safety moderation tool for 17 languages; a possible off-the-shelf component for the moderation-F1 metric rather than building our own.

## Links

[[DPO]] · [[QLoRA]] · [[LoRA]] · `03_Experiments/Week5_Deviations_From_Proposal.md` · `03_Experiments/Week5_Dataset_Description_Sheet.md`
