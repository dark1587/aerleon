"""Harness that runs the example files under docs/examples/.

CLI examples: docs/examples/cli/<name>/{def,policies,expected}
API examples: docs/examples/api/<name>.py with a sibling <name>.stdout.ref

Regenerate the checked-in expected output with:
    UPDATE_DOC_EXAMPLES=1 pytest tests/docs
"""

import contextlib
import importlib.util
import io
import multiprocessing
import os
import shutil
import sys
from pathlib import Path

import pytest

from aerleon import aclgen
from aerleon.utils import config

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_EXAMPLES_DIR = REPO_ROOT / "docs/examples/cli"
API_EXAMPLES_DIR = REPO_ROOT / "docs/examples/api"
UPDATE_ENV = "UPDATE_DOC_EXAMPLES"


def updating() -> bool:
    return os.environ.get(UPDATE_ENV) == "1"


def normalize_output(relpath: str, data: bytes) -> bytes:
    """The single normalisation seam for generator output (identity for now)."""
    return data


def render_cli_example(example_dir: Path, output_dir: Path) -> dict[str, bytes]:
    """Run aclgen in-process on example_dir and return {relative path: bytes}."""
    def_dir = example_dir / "def"
    policies_dir = example_dir / "policies"
    assert def_dir.is_dir(), f"{example_dir}: missing def directory"
    assert policies_dir.is_dir(), f"{example_dir}: missing policies directory"
    output_dir.mkdir(parents=True, exist_ok=True)
    aclgen.Run(
        str(policies_dir),
        str(def_dir),
        None,
        str(output_dir),
        config.defaults["exp_info"],
        1,
        config.defaults["ignore_directories"],
        False,
        False,
        multiprocessing.get_context(),
    )
    return {
        path.relative_to(output_dir).as_posix(): normalize_output(
            path.relative_to(output_dir).as_posix(), path.read_bytes()
        )
        for path in sorted(output_dir.rglob("*"))
        if path.is_file()
    }


def run_api_example(module_path: Path) -> str:
    """Import module_path with its directory as cwd, run main(), return stdout."""
    saved_cwd = os.getcwd()
    module_name = f"docs_example_{module_path.stem}"
    os.chdir(module_path.parent)
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            module.main()
        return buffer.getvalue()
    finally:
        os.chdir(saved_cwd)
        sys.modules.pop(module_name, None)


def check_files(actual: dict[str, bytes], expected_dir: Path, *, update: bool) -> None:
    if update:
        shutil.rmtree(expected_dir, ignore_errors=True)
        for relpath, data in actual.items():
            target = expected_dir / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return
    assert expected_dir.is_dir(), (
        f"{expected_dir} does not exist; create it with {UPDATE_ENV}=1 pytest tests/docs"
    )
    expected = {
        p.relative_to(expected_dir).as_posix(): p.read_bytes()
        for p in expected_dir.rglob("*")
        if p.is_file()
    }
    extra = sorted(set(actual) - set(expected))
    missing = sorted(set(expected) - set(actual))
    assert not extra, f"unexpected output files: {', '.join(extra)}"
    assert not missing, f"missing output files: {', '.join(missing)}"
    changed = sorted(name for name in actual if actual[name] != expected[name])
    assert not changed, (
        f"output differs from expected: {', '.join(changed)} "
        f"(review the change, then regenerate with {UPDATE_ENV}=1)"
    )


def check_text(actual: str, ref_path: Path, *, update: bool) -> None:
    if update:
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text(actual, encoding="utf-8")
        return
    assert ref_path.is_file(), (
        f"{ref_path} does not exist; create it with {UPDATE_ENV}=1 pytest tests/docs"
    )
    assert actual == ref_path.read_text(encoding="utf-8"), (
        f"stdout differs from {ref_path.name} (regenerate with {UPDATE_ENV}=1)"
    )


def cli_example_names() -> list[str]:
    if not CLI_EXAMPLES_DIR.is_dir():
        return []
    return sorted(p.name for p in CLI_EXAMPLES_DIR.iterdir() if p.is_dir())


def api_example_names() -> list[str]:
    if not API_EXAMPLES_DIR.is_dir():
        return []
    return sorted(
        p.stem for p in API_EXAMPLES_DIR.glob("*.py") if not p.name.startswith("_")
    )


@pytest.mark.parametrize("name", cli_example_names())
def test_cli_example(name, tmp_path):
    actual = render_cli_example(CLI_EXAMPLES_DIR / name, tmp_path / "out")
    assert actual, f"{name}: aclgen produced no output files"
    check_files(actual, CLI_EXAMPLES_DIR / name / "expected", update=updating())


@pytest.mark.parametrize("name", api_example_names())
def test_api_example(name):
    check_text(
        run_api_example(API_EXAMPLES_DIR / f"{name}.py"),
        API_EXAMPLES_DIR / f"{name}.stdout.ref",
        update=updating(),
    )
