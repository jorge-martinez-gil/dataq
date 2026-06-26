# -*- coding: utf-8 -*-
"""Smoke tests for the `dataq` command-line interface."""
import json

from dataq.cli import main
from conftest import REPO_ROOT

EXAMPLE = str(REPO_ROOT / "example001.ttl")
EXAMPLE2 = str(REPO_ROOT / "example002.ttl")


def test_cli_assess_text(capsys):
    rc = main(["assess", EXAMPLE])
    assert rc == 0
    assert "DataQ quality report" in capsys.readouterr().out


def test_cli_assess_json(capsys):
    rc = main(["assess", EXAMPLE, "--format", "json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["source"] == EXAMPLE


def test_cli_assess_output_file(tmp_path, capsys):
    out = tmp_path / "report.json"
    rc = main(["assess", EXAMPLE, "--format", "json", "-o", str(out)])
    assert rc == 0
    data = json.loads(out.read_text())
    assert data["n_triples"] > 0


def test_cli_compatibility(capsys):
    rc = main(["compatibility", EXAMPLE, EXAMPLE])
    assert rc == 0
    assert "100.00%" in capsys.readouterr().out


def test_cli_similarity_offline(capsys):
    rc = main(["similarity", EXAMPLE, EXAMPLE2, "--offline"])
    assert rc == 0
    assert "similarity" in capsys.readouterr().out.lower()


def test_cli_show(capsys):
    rc = main(["show", EXAMPLE])
    assert rc == 0
    assert "http://example.org/catalog1" in capsys.readouterr().out


def test_cli_missing_file_errors(capsys):
    rc = main(["assess", "does_not_exist.ttl"])
    assert rc == 1
