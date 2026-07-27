# LLM Alignment Internship

Research journal and modular codebase for a research internship on LLM
fine-tuning and alignment (SFT, PEFT/LoRA/QLoRA, DPO, ORPO, GRPO, reward
modeling), running 2026-07-27 to 2026-09-21, supervised by Pascal Junior
Tikeng Notsawo (PhD Candidate, Université de Montréal / Mila).

## Repository layout

| Path | Purpose |
|---|---|
| `00_Admin_&_Roadmap/` | Contract milestones, weekly checklists |
| `01_Daily_Logs/` | One markdown file per working day: hours, tasks, concepts learned |
| `02_Technical_Concepts/` | Reference notes on the underlying ML concepts (precision/VRAM, optimizers, tokenization, etc.) |
| `03_Experiments/` | Narrative log of each experiment: hypothesis, setup, outcome |
| `04_Weekly_Reports/` | End-of-week summaries |
| `05_References/` | Links, cheat sheets, paper index |
| `06_Reading_Notes/` | One fiche per paper read (problem, method, loss, compute, limitations) |
| `notebooks/` | Local copies of the Kaggle/Colab notebooks used for remote training |
| `ollama/` | Modelfile template used to load a fine-tuned checkpoint into Ollama for local testing |
| `src/` | Modular training/eval/export code, imported by the remote notebooks |
| `tests/` | Local sanity tests (imports, environment) |
| `results/` | Tracked evaluation metrics (JSON); checkpoints/weights are git-ignored |
| `config.yaml` | Global default paths and hyperparameters |

## Execution model

This machine has no GPU. The split is:

- **Local**: writing/reviewing code in `src/`, keeping notes, running
  `pytest tests/` and `ruff check` to catch broken imports/config before
  spending remote GPU time, and testing already fine-tuned small models
  via Ollama.
- **Remote (Kaggle T4/P100, Colab, or a cluster)**: the actual SFT/PEFT/DPO
  training in `src/train.py`.

### Running training remotely

At the top of a Kaggle/Colab notebook:

```bash
git clone https://github.com/zoom-BT/llm-alignment-internship.git
pip install -r llm-alignment-internship/requirements.txt
```

This pulls the current `src/` code so the notebook always trains against
the latest committed version.

### Testing a fine-tuned model locally via Ollama

1. Pull the LoRA checkpoint down from the remote run.
2. `python -m src.export` merges the adapter into the base model and
   converts it to GGUF (see `src/export.py`).
3. Fill in `ollama/Modelfile.template` with the resulting `.gguf` path and
   run `ollama create <name> -f ollama/Modelfile.template`.
4. `ollama run <name>` to interact with it on CPU.

## Local setup

```bash
pip install -r requirements.txt
pytest tests/
```
