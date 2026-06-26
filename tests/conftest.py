# -*- coding: utf-8 -*-
"""Shared pytest fixtures and helpers for the DataQ test suite."""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _all_catalogs():
    paths = sorted(REPO_ROOT.glob("example*.ttl"))
    paths += sorted((REPO_ROOT / "Official catalogs").glob("*.ttl"))
    return [p for p in paths if p.is_file()]


CATALOGS = _all_catalogs()
CATALOG_IDS = [p.name for p in CATALOGS]


@pytest.fixture(params=CATALOGS, ids=CATALOG_IDS)
def catalog_path(request):
    """Path to each bundled catalog (parametrized)."""
    return str(request.param)


@pytest.fixture
def catalog_text(catalog_path):
    with open(catalog_path, "r", encoding="utf-8") as handle:
        return handle.read()


def load_original(module_name):
    """Import one of the original root-level check_*.py scripts by name."""
    path = REPO_ROOT / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
