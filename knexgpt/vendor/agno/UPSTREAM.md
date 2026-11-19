# Agno dependency source snapshot

Copied from [agno-agi/agno](https://github.com/agno-agi/agno) at commit `821be55d1ec3bb472abe8bd94c3b2a0d6c78392f` (18 November 2026), under Apache License 2.0.

Source tree mapping:
- `libs/agno/agno/db/` -> `knexgpt/vendor/agno/db/`
- `libs/agno/agno/vectordb/` -> `knexgpt/vendor/agno/vectordb/`
- `libs/agno/agno/utils/` -> `knexgpt/vendor/agno/utils/`
- `libs/agno/agno/filters.py` -> `knexgpt/vendor/agno/filters.py`
- `libs/agno/agno/exceptions.py` -> `knexgpt/vendor/agno/exceptions.py`

The related Knowledge snapshot is in `knexgpt/knowledge/`. The upstream `agno/__init__.py`, license, and provenance notice are also copied here.

**Status: unmodified source snapshot, not a self-contained library.** The Knowledge and dependency files retain their original `agno.*` absolute imports and depend on modules outside the copied set, such as `agno.models`, `agno.run`, `agno.session`, `agno.fs`, `agno.media`, `agno.metrics` and provider-specific external packages. For example, `agno.db.base` imports run/team/workflow types. These modules were intentionally not copied as part of this knowledge-focused import; completing their transitive closure would draw in unrelated agent execution code.

No application import rewrites, dependency installations, tests, or runtime integrations have been performed. Do not claim this snapshot can be imported independently. A later engineering task must map and isolate actual runtime dependencies, namespace vendored modules correctly, choose supported storage providers, and run import/integration tests.

Preserve original upstream notices and Apache 2.0 license/NOTICE obligations on redistribution. See `AGNO_LICENSE`.
