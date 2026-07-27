
## 🎥 6. Video Resources (FR / EN)

> **Pro Tip:** Watch at 1.25x-1.5x speed with English subtitles enabled to combine technical learning with your daily English listening practice!

### 🇫🇷 Cours & Explications en Français

- **Machine Learning & Deep Learning Fundamentals (Machine Learnia):**
  - [PyTorch pour le Deep Learning (Tensors, CUDA, Autograd)](https://www.youtube.com/playlist?list=PLO_fdPEVlfKqMDNmCFB2XIRyJ23A1yU1x)
  - *Pourquoi regarder:* La meilleure série francophone pour maîtriser le fonctionnement interne des Tensors PyTorch et la gestion GPU.

- **Comprendre les Transformers & le NLP (Yannic Kilcher - FR/EN ou vulgarisation FR):**
  - [Explication intuitive de l'Attention et des Transformers - Machine Learnia](https://www.youtube.com/watch?v=0PjHribuz2g)
  - *Pourquoi regarder:* Explication claire et illustrée du mécanisme *Self-Attention* et des blocs encodeurs/décodeurs.

- **Vulgarisation LLM, Fine-Tuning & Alignement (Science Étonnante):**
  - [Comment fonctionnent les IA comme ChatGPT ? (LLM, Fine-Tuning, RLHF)](https://www.youtube.com/watch?v=7Ell8JG_S44)
  - *Pourquoi regarder:* Vue d'ensemble visuelle parfaite pour ancrer la différence entre Pré-entraînement, SFT et Alignement par Récompense.

---

### 🇬🇧 English Deep Dives & Coding Tutorials

- **Core Transformers & Building GPT from Scratch (Andrej Karpathy):**
  - [Let's build GPT: from scratch, in code, spelled out.](https://www.youtube.com/watch?v=kCc8FmEb1nY)
  - *Pourquoi regarder:* Le tutoriel le plus important au monde pour comprendre *exactement* ce qui se passe sous le capot d'un Transformer décodeur (MHA, Logits, Softmax, Loss).

- **Visual Intuition & Mathematics (3Blue1Brown):**
  - [Visualizing Attention, Transformer Neural Networks (Chapter 5, Deep Learning Series)](https://www.youtube.com/watch?v=eMlx5fFNoYc)
  - *Pourquoi regarder:* Des animations 3D inégalées pour visualiser l'espace vectoriel des embeddings, les clés/requêtes/valeurs ($K, Q, V$), et l'attention.

- **Hugging Face Ecosystem & Practical SFT/LoRA (Hugging Face Official / Umar Jamil):**
  - [Umar Jamil: LoRA & QLoRA Explained & Implemented from Scratch](https://www.youtube.com/watch?v=PXER10Nzphc)
  - [Umar Jamil: LLaMA Architecture & Attention Mechanisms](https://www.youtube.com/watch?v=mnKuCxDkW4A)
  - *Pourquoi regarder:* Umar Jamil décortique les équations des papiers de recherche et les traduit ligne par ligne en PyTorch.

- **Fine-Tuning, DPO & Quantization Tutorials (Maxime Labonne / Benjamin Marie / Mark Saroufim):**
  - [Trelis Research / Fine-Tuning LLMs with HuggingFace TRL & PEFT](https://www.youtube.com/watch?v=iO82pIAtiYI)
  - *Pourquoi regarder:* Démonstrations pratiques de scripts d'entraînement `SFTTrainer`, gestion du VRAM et intégration LoRA/Quantization.

---

## 📺 Video Reference Checkpoints

| Topic | Recommended Video | Target Concept | Status |
| :--- | :--- | :--- | :---: |
| **PyTorch & CUDA** | Machine Learnia (PyTorch) | Tensors, Autograd, `to('cuda')` | ⬜ |
| **Transformer Math** | 3Blue1Brown (Chapter 5) | $Q, K, V$ Matrices, Softmax Scaling | ⬜ |
| **Transformer Code** | Andrej Karpathy (Let's build GPT) | Positional Encoding, Causal Mask | ⬜ |
| **LoRA / QLoRA** | Umar Jamil (LoRA Explained) | Low-Rank Decomposition ($A \times B$) | ⬜ |
| **SFT & Tokenization** | Hugging Face Official | Chat Templates, Padding, `SFTTrainer` | ⬜ |
