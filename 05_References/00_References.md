# 📚 Master References & Documentation Index

> **Purpose:** Centralized repository of papers, documentation, and technical guides required for the ML Research Internship.

---

## 📄 1. Fundamental Research Papers

### Architecture & Foundation
- **Transformer Architecture (Attention Is All You Need):**
  - [Paper (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762)
  - *Key concepts:* Multi-Head Attention (MHA), Feed-Forward Networks, Positional Encoding.

### Parameter-Efficient Fine-Tuning (PEFT)
- **LoRA: Low-Rank Adaptation of Large Language Models:**
  - [Paper (arXiv:2106.09685)](https://arxiv.org/abs/2106.09685)
  - *Key concepts:* Low-rank matrices ($r$, $\alpha$), parameter efficiency, zero latency overhead.
- **QLoRA: Efficient Finetuning of Quantized LLMs:**
  - [Paper (arXiv:2305.14314)](https://arxiv.org/abs/2305.14314)
  - *Key concepts:* 4-bit NormalFloat (NF4), Double Quantization, Paged Optimizers.

### Instruction Tuning & Supervised Fine-Tuning (SFT)
- **Training Language Models to Follow Instructions with Human Feedback (InstructGPT):**
  - [Paper (arXiv:2203.02155)](https://arxiv.org/abs/2203.02155)
  - *Key concepts:* Supervised fine-tuning on human demonstrations, reward modeling from preference comparisons, RLHF via PPO — Week 2's required reading.

### Alignment & Preference Optimization
- **DPO: Direct Preference Optimization:**
  - [Paper (arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  - *Key concepts:* Reference-free alignment, implicit reward modeling, preference loss.
- **ORPO: Monolithic Preference Optimization:**
  - [Paper (arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  - *Key concepts:* Odds Ratio Penalty, single-stage alignment without reference model.
- **GRPO: Group Relative Policy Optimization (DeepSeekMath):**
  - [Paper (arXiv:2402.03300)](https://arxiv.org/abs/2402.03300)
  - *Key concepts:* Relative group rewards, memory-efficient RL without explicit critic model.

---

## 🛠️ 2. Official Technical Documentation

### PyTorch & Hardware Mechanics
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [PyTorch CUDA & Memory Management](https://pytorch.org/docs/stable/notes/cuda.html)
- [Numerical Precision (FP32, FP16, BF16 Explained)](https://pytorch.org/docs/stable/amp.html)

### Hugging Face Ecosystem
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [Hugging Face Datasets Documentation](https://huggingface.co/docs/datasets/index)
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index)
- [Hugging Face TRL (Transformer Reinforcement Learning)](https://huggingface.co/docs/trl/index)
- [Hugging Face Accelerate (Distributed Training & Offloading)](https://huggingface.co/docs/accelerate/index)
- [Hugging Face Evaluate](https://huggingface.co/docs/evaluate/index)
- [LightEval Benchmark Suite](https://github.com/huggingface/lighteval)

---

## 📖 3. Concept Validation Guides & Articles

### Tokenization & Chat Templates
- [Hugging Face Guide: Chat Templates in Transformers](https://huggingface.co/docs/transformers/main/en/chat_templating)
- [Understanding Subword Tokenization (BPE, WordPiece, Unigram)](https://huggingface.co/docs/transformers/tokenizer_summary)

### SFT & Memory Optimization
- [TRL Guide: Supervised Fine-Tuning (SFTTrainer)](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face Guide: Efficient Training on Single GPU (Gradient Accumulation & Checkpointing)](https://huggingface.co/docs/transformers/perf_train_gpu_one)
- [BitsAndBytes 4-bit / 8-bit Quantization Integration](https://huggingface.co/docs/transformers/main_classes/quantization)

### Experiment Tracking & Logging
- [Weights & Biases (WandB) PyTorch / Transformers Integration](https://docs.wandb.ai/guides/integrations/huggingface)
- [TensorBoard with PyTorch](https://pytorch.org/tutorials/intermediate/tensorboard_tutorial.html)

---

## 💡 4. Open-Source Reference Models & Datasets

### Light Open-Source Models (Recommended for Week 1)
- [Qwen 2.5 (0.5B / 1.5B / 3B)](https://huggingface.co/Qwen)
- [SmolLM2 (135M / 360M / 1.7B)](https://huggingface.co/HuggingFaceTB)
- [Gemma 2 (2B)](https://huggingface.co/google/gemma-2-2b)
- [Llama 3.2 (1B / 3B)](https://huggingface.co/meta-llama)

### Benchmark Datasets
- [Hugging Face Datasets Hub](https://huggingface.co/datasets)
- [UltraFeedback Binarized (Preference Data)](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized)
- [OpenHermes 2.5 (Instruction Data)](https://huggingface.co/datasets/teknium/openhermes_2.5)

---

## 🎯 5. Prerequisites Verification Matrix

| Concept / Tool                   | Verification Link / Source                                                                        | Status |
| :------------------------------- | :------------------------------------------------------------------------------------------------ | :----: |
| **PyTorch Tensors & CUDA**       | [PyTorch CUDA Notes](https://pytorch.org/docs/stable/notes/cuda.html)                             |   ⬜    |
| **Transformers Architecture**    | [Attention Is All You Need Paper](https://arxiv.org/abs/1706.03762)                               |   ⬜    |
| **Tokenizers & Control Tokens**  | [HF Tokenizer Summary](https://huggingface.co/docs/transformers/tokenizer_summary)                |   ⬜    |
| **Chat Templates (Jinja2)**      | [HF Chat Templating Guide](https://huggingface.co/docs/transformers/main/en/chat_templating)      |   ⬜    |
| **SFT Training (`SFTTrainer`)**  | [TRL SFT Documentation](https://huggingface.co/docs/trl/sft_trainer)                              |   ⬜    |
| **VRAM & Precision (BF16/FP16)** | [HF Single GPU Performance](https://huggingface.co/docs/transformers/perf_train_gpu_one)          |   ⬜    |
| **LoRA / QLoRA Theory**          | [LoRA Paper](https://arxiv.org/abs/2106.09685) \| [QLoRA Paper](https://arxiv.org/abs/2305.14314) |   ⬜    |
| **DPO / Alignment Theory**       | [DPO Paper](https://arxiv.org/abs/2305.18290)                                                     |   ⬜    |