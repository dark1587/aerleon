"""Self-tests for the docs example harness, run on tiny fixtures in tmp_path."""

import os
import shutil
import sys

import pytest

import tests.docs.docs_examples_test as h
from tests.docs.docs_examples_test import (
    check_files,
    check_text,
    render_cli_example,
    run_api_example,
)

DEFINITIONS = """\
networks:
  MGMT:
    values:
      - address: 10.0.0.0/24
      - address: 192.168.10.0/24
services:
  SSH:
    - port: 22
      protocol: tcp
"""

POLICY = """\
filters:
  - header:
      targets:
        cisco: edge-inbound extended
    terms:
      - name: allow-ssh
        comment: "Allow SSH from the management network."
        source-address: MGMT
        protocol: tcp
        destination-port: SSH
        action: accept
      - name: default-deny
        action: deny
"""


@pytest.fixture
def tiny_example(tmp_path):
    root = tmp_path / "example"
    (root / "def").mkdir(parents=True)
    (root / "policies" / "pol").mkdir(parents=True)
    (root / "def" / "definitions.yaml").write_text(DEFINITIONS)
    (root / "policies" / "pol" / "edge-inbound.yaml").write_text(POLICY)
    return root


def test_render_cli_example_returns_output_files(tiny_example, tmp_path):
    out = render_cli_example(tiny_example, tmp_path / "out")
    assert list(out) == ["edge-inbound.acl"]
    assert b" permit tcp 10.0.0.0 0.0.0.255 any eq 22\n" in out["edge-inbound.acl"]


def test_render_cli_example_mirrors_subdirectories(tiny_example, tmp_path):
    pols = tiny_example / "policies"
    (pols / "site-a").mkdir()
    shutil.move(str(pols / "pol"), str(pols / "site-a" / "pol"))
    out = render_cli_example(tiny_example, tmp_path / "out")
    assert list(out) == ["site-a/edge-inbound.acl"]


def test_render_cli_example_raises_on_aclgen_error(tiny_example, tmp_path):
    pol = tiny_example / "policies" / "pol" / "edge-inbound.yaml"
    pol.write_text(POLICY.replace("source-address: MGMT", "source-address: NOPE"))
    with pytest.raises(SystemExit):
        render_cli_example(tiny_example, tmp_path / "out")


def test_render_cli_example_requires_def(tmp_path):
    (tmp_path / "policies").mkdir()
    with pytest.raises(AssertionError, match="missing def directory"):
        render_cli_example(tmp_path, tmp_path / "out")


def test_render_cli_example_requires_policies(tmp_path):
    (tmp_path / "def").mkdir()
    with pytest.raises(AssertionError, match="missing policies directory"):
        render_cli_example(tmp_path, tmp_path / "out")


def test_check_files_missing_expected_names_update_env(tmp_path):
    with pytest.raises(AssertionError, match="UPDATE_DOC_EXAMPLES=1"):
        check_files({"a.acl": b"x"}, tmp_path / "expected", update=False)


def _expected(tmp_path):
    expected = tmp_path / "expected"
    expected.mkdir()
    (expected / "a.acl").write_bytes(b"x")
    (expected / "b.acl").write_bytes(b"y")
    return expected


def test_check_files_detects_extra_file(tmp_path):
    with pytest.raises(AssertionError, match="unexpected output files: c.acl"):
        check_files(
            {"a.acl": b"x", "b.acl": b"y", "c.acl": b"w"}, _expected(tmp_path), update=False
        )


def test_check_files_detects_missing_file(tmp_path):
    with pytest.raises(AssertionError, match="missing output files: b.acl"):
        check_files({"a.acl": b"x"}, _expected(tmp_path), update=False)


def test_check_files_detects_changed_file(tmp_path):
    with pytest.raises(AssertionError, match="output differs from expected: b.acl"):
        check_files({"a.acl": b"x", "b.acl": b"z"}, _expected(tmp_path), update=False)


def test_check_files_passes_when_equal(tmp_path):
    check_files({"a.acl": b"x", "b.acl": b"y"}, _expected(tmp_path), update=False)


def test_check_files_update_removes_stale(tmp_path):
    expected = tmp_path / "expected"
    expected.mkdir()
    (expected / "stale.acl").write_bytes(b"old")
    check_files({"a.acl": b"x"}, expected, update=True)
    assert sorted(p.name for p in expected.iterdir()) == ["a.acl"]
    assert (expected / "a.acl").read_bytes() == b"x"


def test_run_api_example_captures_stdout_and_restores_cwd(tmp_path):
    (tmp_path / "data.txt").write_text("hello\n")
    (tmp_path / "ex.py").write_text(
        "def main():\n    print(open('data.txt').read(), end='')\n"
    )
    cwd = os.getcwd()
    assert run_api_example(tmp_path / "ex.py") == "hello\n"
    assert os.getcwd() == cwd
    assert "docs_example_ex" not in sys.modules


def test_run_api_example_registers_module_while_running(tmp_path):
    (tmp_path / "reg.py").write_text(
        "import sys\n"
        "def main():\n"
        "    print('docs_example_reg' in sys.modules)\n"
    )
    assert run_api_example(tmp_path / "reg.py") == "True\n"
    assert "docs_example_reg" not in sys.modules


def test_run_api_example_cleans_up_when_main_raises(tmp_path):
    (tmp_path / "boom.py").write_text("def main():\n    raise RuntimeError('boom')\n")
    cwd = os.getcwd()
    with pytest.raises(RuntimeError, match="boom"):
        run_api_example(tmp_path / "boom.py")
    assert os.getcwd() == cwd
    assert "docs_example_boom" not in sys.modules


def test_check_text_round_trip(tmp_path):
    check_text("out\n", tmp_path / "x.stdout.ref", update=True)
    check_text("out\n", tmp_path / "x.stdout.ref", update=False)
    with pytest.raises(AssertionError):
        check_text("other\n", tmp_path / "x.stdout.ref", update=False)


def test_check_text_missing_ref_names_update_env(tmp_path):
    with pytest.raises(AssertionError, match="UPDATE_DOC_EXAMPLES=1"):
        check_text("out\n", tmp_path / "x.stdout.ref", update=False)


def test_api_example_names_skips_private(monkeypatch, tmp_path):
    for name in ("a.py", "_helper.py", "a.stdout.ref"):
        (tmp_path / name).write_text("")
    monkeypatch.setattr(h, "API_EXAMPLES_DIR", tmp_path)
    assert h.api_example_names() == ["a"]


def test_cli_example_names_sorted_dirs_only(monkeypatch, tmp_path):
    (tmp_path / "b").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "file.txt").write_text("")
    monkeypatch.setattr(h, "CLI_EXAMPLES_DIR", tmp_path)
    assert h.cli_example_names() == ["a", "b"]
    monkeypatch.setattr(h, "CLI_EXAMPLES_DIR", tmp_path / "missing")
    assert h.cli_example_names() == []


def test_updating_reads_env(monkeypatch):
    monkeypatch.setenv(h.UPDATE_ENV, "1")
    assert h.updating() is True
    monkeypatch.setenv(h.UPDATE_ENV, "0")
    assert h.updating() is False
    monkeypatch.delenv(h.UPDATE_ENV)
    assert h.updating() is False
