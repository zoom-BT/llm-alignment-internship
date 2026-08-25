# RESEARCH PROPOSAL

| RESEARCH PROPOSAL |  | PREPARED BY          Balbino Tchoutzine	 |
| :---- | :---- | ----: |
| 23/08/2026 |  | **Fabrique Ngousso** Yaoundé, Cameroon |

# **Translated Safety Alignment vs. Native:** Direct Preference Optimization on African Multi-Lingual Foundation Models

# 1\. Research Context

Large language models (LLMs) exhibit a critical degradation of their safety guardrails when prompted in low-resource languages (*Yong et al., 2023; Abdullahi et al., 2026*). The majority of current work relies on safety datasets automatically translated from English, which miss culturally grounded risks and underestimate vulnerability to cross-lingual attacks.
The recent emergence of foundation models benefiting from large-scale continued pre-training (CPT) on African corpora, such as AfriqueQwen3.5-4B-50Langs (35.5 billion tokens across 50 languages), offers a solid linguistic base. It constitutes an ideal case study for measuring the direct impact of targeted DPO alignment without interference from prior English-centric alignment (*Rafailov et al., 2023*).

# 2\. Related Work

The recent scientific literature on the safety alignment of large language models is structured around three axes fundamental to this project:

1. Multilingual safety degradation and the flaws of translated benchmarks
   Work on multilingual safety demonstrates that LLM safety guardrails collapse when queries are formulated in low-resource languages (*Yong et al., 2023*). A recent systematic review of the literature highlights that the majority of evaluations rely on datasets automatically translated from English, an approach that masks culturally grounded risks and underestimates injection or code-switching attacks. To address this limitation, recent initiatives have introduced native benchmarks centered on local safety policies, such as UbuntuGuard (*Abdullahi et al., 2026*), which proposes multi-turn dialogue scenarios authored by African domain experts.

2. Continued pre-training and African foundation models
   To overcome tokenization biases and the poor geometric representation of low-resource languages in models' latent space, the research community has developed continued pre-training (CPT) strategies. The AfriqueLLM suite (*Yu et al., 2026*), and in particular the AfriqueQwen3.5-4B-50Langs model, represents the current state of the art, extending the Qwen3.5-4B base model over more than 35.5 billion tokens covering 50 African languages. This "Raw" model has not undergone any instruction or safety alignment (*Yu et al., 2026*).

# 3\. Research Question

To what extent does a DPO (*Direct Preference Optimization*) safety alignment based on native African-language data improve the refusal rate for malicious queries on the AfriqueQwen3.5-4B-50Langs model (*Yu et al., 2026*), compared to an alignment on translated data, while preserving the model's accuracy and utility on benign queries?

# 4\. Hypotheses

**H1) Superiority of native vs. translated alignment:**
A DPO alignment performed with a native safety dataset (e.g. *UbuntuGuard*) produces a refusal rate *(Refusal Rate)* for malicious queries in African languages significantly higher than one obtained via alignment on data automatically translated from English.

**H2) Role of the CPT-pretrained backbone:**
Due to its richer vector and linguistic representation across 50 African languages, the AfriqueQwen3.5-4B-50Langs model (*Yu et al., 2026*) retains safety rules better after DPO alignment than a standard, non-adapted base model (*Qwen3.5-4B-Base*).

**H3) Preservation of utility and control of over-refusal:**
DPO alignment targeted on native data reverses safety degradation on toxic queries without causing a disproportionate increase in the over-refusal rate *(Over-Refusal Rate)* on benign health- and local-culture-related questions.

5\. Expected Contribution
**C1) Targeted safety alignment on an African CPT backbone (~~first~~):**
An ~~first~~ empirical evaluation and implementation of DPO safety alignment on the AfriqueQwen3.5-4B-50Langs foundation model (*Yu et al., 2026*), testing the hypothesis that multilingual continued pre-training improves the retention of safety instructions.
**C2) Experimental evidence, Native vs. Translated:**
A quantified comparative analysis demonstrating the limitations of translated safety data and the effectiveness of alignment datasets natively grounded in the African socio-cultural context (*Abdullahi et al., 2026*).
**C3) Frugal, reproducible alignment pipeline:**
An open-source codebase enabling the evaluation and alignment of multilingual LLMs under light compute constraints (runnable on an NVIDIA T4 GPU in under 2 hours via QLoRA+DPO).

6\. Selected Models
The study will rely on two 4-billion-parameter models to isolate the impact of multilingual continued pre-training (*Continued Pre-Training — CPT*) on the retention of safety instructions:
**M1) Target African CPT Model:** *AfriqueQwen3.5-4B-50Langs, June 2026*
Foundation model developed by the McGill-NLP team (Yu et al., 2026), extended from the Qwen3.5 architecture via continued pre-training on 35.5 billion tokens covering 50 African languages. Used to verify whether a latent space rich in local languages improves the efficiency of safety guardrails.
**M2) Reference Model (baseline architecture):** *Qwen3.5-4B-Base, March 2026*
Standard, unadapted base model (no African-language CPT). Used to measure the safety-performance gap between a standard general-purpose English/multilingual backbone and a backbone specifically adapted to African languages (validation of **H2**).

7\. Datasets

The datasets are structured according to their role in the experimental pipeline (DPO training vs. evaluation):
**D1) Alignment Data (DPO Training)**

- Native DPO Dataset

 Extracted directly from the **training split of UbuntuGuard** (Abdullahi et al., 2026 — CC BY 4.0 license), which already provides complete preference pairs in the local language, with no manual writing required (1,171 to 13,532 examples depending on the language, across 10 African languages including Hausa, Yoruba, Swahili). Each instance comprises:
**Prompt**: A toxic or sensitive query, derived from the 8,091 original English queries and translated by the benchmark's authors into the target language.
**Chosen (PASS)**: A response compliant with the context-specific safety policy (5-8 rules generated by GPT-5), generated by Llama-3.1-405B or Qwen3-235B.
**Rejected (FAIL)**: A response violating one or more rules of the same policy, generated by the same models.
*Limitation to note (see section 13):* since PASS/FAIL come from third-party models rather than AfriqueQwen-Raw itself, these pairs are off-policy for the target model — a standard limitation of public preference datasets (e.g. UltraFeedback).

- Translated DPO Dataset

To isolate the "translation quality/nativeness" variable rather than content, this dataset reuses the **same English source content from UbuntuGuard** (the same PASS/FAIL pairs) but machine-translated (NLLB/Google Translate) into the target languages, instead of the benchmark authors' translations. H1 thus compares two versions of the same safety content — native/expert translation vs. machine translation — at equal volume and content.

**D2) Safety & Refusal Evaluation Datasets**

- **UbuntuGuard** (Abdullahi et al., 2026): Native policy-based safety benchmark covering 10 African languages across sensitive multi-turn scenarios (health, finance, education, government). Used to measure the Refusal Rate.
- **AfriHate:** Corpus annotated by native speakers covering 15 African languages, used to test hate speech and abusive language detection.

**D3) Over-Refusal & Utility Evaluation Datasets**

- HealthBench-Africa Extension: Benign health-advice scenarios and queries formulated in local languages.
- Uhura-TruthfulQA / IrokoBench subsets: Questions on local culture, history, and knowledge. Used to measure the Over-Refusal Rate and verify that DPO alignment does not improperly block legitimate queries (validation of **H3**).

8\. Baselines
The experiment will compare four model configurations to precisely isolate the factors driving alignment effectiveness:
**B1) AfriqueQwen-Raw**
The unaligned AfriqueQwen3.5-4B-50Langs model, establishing the CPT backbone's baseline level of spontaneous refusal and safety.
**B2) AfriqueQwen + Translated-DPO**
The AfriqueQwen3.5-4B-50Langs model aligned via DPO with the safety dataset automatically translated from English (Translated-DPO).
**B3) Qwen-Base + Native-DPO**
The standard general-purpose Qwen3.5-4B-Base model aligned with the native dataset (Native-DPO), used to validate the impact of the backbone's linguistic representation (**H2**).
**B4) AfriqueQwen + Native-DPO**
The target model, combining African continued pre-training with DPO alignment on native data.

9\. Evaluation Metrics & Procedure
Evaluation relies on three main quantitative metrics:

- Refusal Rate (RR%)
  Proportion of malicious or toxic queries (from UbuntuGuard) for which the model produces an explicit refusal compliant with the safety policy.

- Over-Refusal Rate (Over-RR %)
  Proportion of legitimate, benign queries (health, culture) wrongly blocked by the model (measures preservation of utility, **H3**).
- Moderation F1-Score / Precision:
  Macro F1 score evaluated on the AfriHate corpus, measuring the model's ability to classify hate speech and abusive content.


Evaluation procedure: generated responses are automatically classified using linguistic refusal-detection patterns and a lightweight moderation classifier, with manual cross-validation on a 10% sample of responses.

10\. Experimental Protocol
**E1) Baseline Evaluation**
Inference of the Raw AfriqueQwen3.5-4B-50Langs model on the evaluation datasets (UbuntuGuard, AfriHate, HealthBench-Africa) to extract starting metrics.

**E2) DPO Dataset Structuring**
Formatting of UbuntuGuard's training-split PASS/FAIL pairs into ChatML for Native-DPO (no generation required); automatic translation (NLLB) of the same English-source pairs into the target languages for Translated-DPO.

**E3) DPO Training via QLoRA**
Model fine-tuning using the DPO algorithm (Rafailov et al., 2023) under 4-bit QLoRA (rank=16, alpha=32, learning rate=5\*10^-6) on Kaggle (2\* T4 GPUs).

**E4) Comparative Inference & Post-Evaluation**
Re-evaluation of the aligned models on the same prompts to measure the performance delta (**delta RR and delta ORR**).

11\. Planned Ablation Studies

**A1) Alignment data volume**
Evaluation of the aligned model's performance with 250, 500, and 1000 DPO examples to determine the minimal threshold of preference data required.

**A2) Impact of linguistic diversity**
Comparison between monolingual DPO alignment (e.g. Hausa only) and balanced multilingual DPO alignment (Hausa, Yoruba, Swahili, Pidgin) to observe cross-lingual safety transfer.

12\. Estimated Computing Requirements (\<12h)

- **Baseline Inference (Colab T4)**

  Inference on 1000 prompts takes ~15 minutes with vLLM/Hugging Face pipeline optimization in 4-bit.

- **DPO Training (Kaggle 2\* Tesla T4)**
  A QLoRA DPO training run on 1000 preference pairs (3 epochs) takes approximately 45 to 60 minutes and requires < 6GB of VRAM per GPU.
- **Feasibility criterion validation**
  A complete initial experiment (Inference + Training + Re-Inference) runs in under 2 hours, satisfying the budget constraint (< 12 hours per experiment and > 30 hours/week available).


13\. Main Risks and Limitations

- **Risk of Catastrophic Forgetting**

  DPO alignment can reduce the model's general linguistic fluency. Mitigation: integrating general conversational pairs into the alignment dataset.

- **Restricted Linguistic Scope**

  The experimental evaluation will focus on 4 to 5 major languages (Hausa, Yoruba, Swahili, Nigerian Pidgin) out of the 50 covered by the model.

- **Absence of Real-Time Human Annotators**

  Validation relies on expert-pre-annotated benchmarks and automated metrics.

- **Off-Policy DPO Pairs**

  UbuntuGuard's PASS/FAIL responses are generated by third-party models (Llama-3.1-405B, Qwen3-235B), not by AfriqueQwen-Raw itself — a standard limitation of public preference datasets (e.g. UltraFeedback), but one that may reduce the DPO signal's effectiveness compared to on-policy pairs.


14\. Schedule for Weeks 5 to 8

| Week  | Main Objectives & Technical Deliverables |
| :---- | :---- |
| W1 | Validate the inference script, extract Baseline 1, and prepare the DPO datasets. |
| W2 | Run DPO training on Kaggle (Native model vs. Translated model) and obtain Baselines 2 and 3. |
| W3 | Run ablation studies (data volume, language mix) and evaluate over-refusal (ORR). |
| W4 | Synthesize results, generate comparative figures, and write the final report. |


15\. Expected Figures and Tables
**F1) Pipeline Architecture**
Diagram illustrating the flow from the AfriqueQwen CPT model through DPO alignment (Native vs. Translated) to the dual evaluation (Safety vs. Over-Refusal).
**F2) Refusal Efficiency Chart**
Bar chart comparing the Refusal Rate (RR) per language across the raw model, translated alignment, and native alignment.
**T1) Main Results Table**
Comparative summary of metrics (RR, ORR, F1-AfriHate) across all baselines.
**T2) Ablation Results**
Evolution of scores by DPO dataset size (250, 500, 1000 examples) and degree of linguistic diversity.

# All\_Refs

Full bibliography and list of open-source resources (models and datasets) for the *Balbino* *Research Proposal*.

### **1\. Foundational Scientific Publications (Reference Articles)**

* **AfriqueLLM & AfriqueQwen3.5 (African CPT Model):**

* **Reference:** Yu, H., Xu, T., Hedderich, M. A., Hamidouche, W., Zamir, S. W., & Adelani, D. I. (2026). *AfriqueLLM: How Data Mixing and Model Architecture Impact Continued Pre-training for African Languages*. arXiv preprint arXiv:2601.06395.

* **Link:** [https://arxiv.org/abs/2601.06395](https://arxiv.org/abs/2601.06395)

  \[cite: 1\]

* **UbuntuGuard (Native Safety Policy Benchmark):**

* **Reference:** Abdullahi, T., Mgonzo, M., Owodunni, A. T., Singh, R., & Eickhoff, C. (2026). *UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages*. OpenReview / arXiv preprint arXiv:2601.12696.

* **Link:** [https://openreview.net/pdf?id=uPSzx3SBdf](https://openreview.net/pdf?id=uPSzx3SBdf)

  \[cite: 2\]

* **AfriHate (Hate Speech Corpus in 15 African Languages):**

  - **Reference:** Muhammad, S. H., et al. (2025). *AfriHate: A Multilingual Collection of Hate Speech and Abusive Language Datasets for African Languages*. arXiv preprint arXiv:2501.08284.

  - **Link:** [https://arxiv.org/abs/2501.08284](https://arxiv.org/abs/2501.08284)

    \[cite: 3\]

* **Multilingual Safety Vulnerability (*Jailbreaking* via Low-Resource Languages):**

  - **Reference:** Yong, J. U., Menghini, C., & Bach, S. H. (2023). *Low-Resource Languages Jailbreak GPT-4*. arXiv preprint arXiv:2310.02446.

  - **Link:** [https://arxiv.org/abs/2310.02446](https://arxiv.org/abs/2310.02446)

* **Direct Preference Optimization (DPO):**

  - **Reference:** Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. Advances in Neural Information Processing Systems (NeurIPS 2023).

  - **Link:** [https://arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290)

* **QLoRA (4-bit Quantization and LoRA Adapters):**

  - **Reference:** Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. Advances in Neural Information Processing Systems (NeurIPS 2023).

  - **Link:** [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)

* **AfriStereo (Bias and Stereotype Evaluation):**

  - **Reference:** YUX Cultural AI Lab (2025). *AfriStereo: A Culturally Grounded Dataset for Evaluating Stereotypical Bias in Large Language Models*. arXiv preprint arXiv:2511.22016.

  - **Link:** [https://arxiv.org/abs/2511.22016](https://arxiv.org/abs/2511.22016)

    \[cite: \]

### **2\. Studied Models (Hugging Face)**

| Model Name | Experimental Role | Direct Hugging Face Link |
| :---- | :---- | :---- |
| **AfriqueQwen3.5-4B-50Langs** | Target CPT model (McGill-NLP)  | [HuggingFace / McGill-NLP](https://huggingface.co/McGill-NLP)  \[cite: 1\]  |
| **Qwen3.5-4B-Base** | Control model (Qwen Team) | [HuggingFace / Qwen/Qwen3.5-4B-Base](https://huggingface.co/Qwen) |

### **3\. Datasets and Evaluation Benchmarks (Hugging Face & Repositories)**

| Dataset Name | Use in Proposal | Link / Source Repository |
| :---- | :---- | :---- |
| **UbuntuGuard** | Safety & refusal policy dataset  | [OpenReview Paper & Dataset](https://openreview.net/pdf?id=uPSzx3SBdf)  \[cite: 2\]  |
| **AfriHate** | Hate speech detection (15 languages)  | [HuggingFace: afrihate/afrihate](https://huggingface.co/datasets/afrihate/afrihate)  \[cite: 3\]  |
| **AfriStereo** | Stereotype/anti-stereotype pairs  | [GitHub: Afri-Stereo Repository](https://github.com/YUX-Cultural-AI-Lab/Afri-Stereo)  \[cite: \]  |
| **CyberNaija** | Cyberbullying in Pidgin and code-switching  | [HuggingFace: cike-dev/CyberNaija](https://huggingface.co/datasets/cike-dev/CyberNaija)  \[cite: \]  |
| **IrokoBench** | Multi-task and safety comprehension  | [HuggingFace Collection: masakhane/irokobench](https://huggingface.co/collections/masakhane/irokobench)  \[cite: \]  |
| **Uhura-TruthfulQA** | Factuality and cultural grounding  | [HuggingFace: masakhane/uhura-truthfulqa](https://huggingface.co/datasets/masakhane/uhura-truthfulqa)  \[cite: \]  |
| **HealthBench-Africa** | Over-refusal and medical advice evaluation  | [HuggingFace: tonative/healthbench-africa-extension](https://huggingface.co/datasets/tonative/healthbench-africa-extension)  \[cite: \] |
