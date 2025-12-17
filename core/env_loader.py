import importlib
import os
import pytest

def load_env():
    try:
        env = pytest.config.getoption("--env")
    except Exception:
        env = os.getenv("ENV", "dev")

    return importlib.import_module(f"config.{env}")
