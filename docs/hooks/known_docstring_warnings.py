"""Temporary mkdocs hook: drop known griffe docstring warnings.

``mkdocs build --strict`` aborts on griffe docstring warnings that come from
docstrings in ``aerleon/``. Docs PRs change no Python under ``aerleon/``, so
the exact known messages are filtered here. The cleanup PR fixes the
docstrings and deletes this file and the ``hooks:`` line in ``mkdocs.yml``.
"""

import logging

KNOWN: tuple[str, ...] = (
    "aerleon/lib/naming.py:480: Failed to get 'exception: description' pair from 'service tokens.'",
)


class _KnownWarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(message.endswith(known) for known in KNOWN)


def on_startup(**kwargs) -> None:
    logging.getLogger("mkdocs.plugins.griffe").addFilter(_KnownWarningFilter())
