# Agno Knowledge source attribution

This directory vendors the source files from Agno's Knowledge package, preserving their original relative paths and file contents.

- Upstream repository: https://github.com/agno-agi/agno
- Upstream revision: `821be55d1ec3bb472abe8bd94c3b2a0d6c78392f` (2026-11-18)
- Original path: `libs/agno/agno/knowledge/`
- Copied path: `knexgpt/knowledge/`
- Upstream license: Apache License, Version 2.0 (see `AGNO_LICENSE`)

The vendored code retains imports of `agno.*` modules outside this directory, including database adapters, vector databases, and utilities. This commit is a source copy, **not** a functional standalone port. It does not change existing KnexGPT runtime wiring or replace the Agno package dependencies.

The existing files are unchanged from the pinned upstream revision. Please preserve applicable copyright/license notices when modifying or redistributing them.
