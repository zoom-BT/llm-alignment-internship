"""Sanity check that the local Python environment can import the core stack."""
import sys

import torch


def test_python_version_is_at_least_3_10():
    assert sys.version_info >= (3, 10)


def test_core_imports_succeed():
    import peft  # noqa: F401
    import transformers  # noqa: F401
    import trl  # noqa: F401


def test_cuda_availability_is_reported(capsys):
    if torch.cuda.is_available():
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")
    else:
        print("CUDA not available; this machine is CPU-only (expected for local dev).")
    captured = capsys.readouterr()
    assert "CUDA" in captured.out
