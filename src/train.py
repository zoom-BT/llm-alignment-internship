"""SFT / PEFT / DPO training entry points built on TRL and Accelerate.

Meant to run on remote GPUs (Kaggle/Colab); see README.md for the
git-clone-based sync pattern used to pull this module into a notebook.
"""


def run_sft(config: dict):
    """Run supervised fine-tuning using trl.SFTTrainer per `config['training']`."""
    raise NotImplementedError("Wire up once the first base model is chosen.")


def run_dpo(config: dict):
    """Run DPO/ORPO alignment using trl per `config['training']`."""
    raise NotImplementedError("Wire up once a reference SFT checkpoint exists.")
