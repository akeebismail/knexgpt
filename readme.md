# KnexGPT

**Open-source data ingestion, knowledge management, and data lifecycle infrastructure.**

KnexGPT is an early-stage Python project exploring how to collect information from different sources, organize it consistently, track where it came from, and make it available to software applications.

The goal is a small, reusable foundation for **data ingestion**, **knowledge management**, and the **context development lifecycle**: the work of keeping source information, its representations, and its metadata accurate as data changes. A developer should not have to rebuild the same source connectors, parsing logic, metadata records, and update handling for every application.

> **Status: early development, not a working product.** The repository contains original experiments and a copied snapshot of Agno's Knowledge code and supporting dependencies. These parts have not been integrated, dependency-resolved, or verified as a standalone KnexGPT package. This README distinguishes **existing source code** from **planned capabilities**.

## What problem is KnexGPT trying to solve?

Data arrives in different formats and from different systems. Loading a file or calling an API is only the beginning. Applications also need to know:

- **Where did the information come from?** Track source identity, origin, and metadata.
- **How was it processed?** Keep a traceable link from raw data to parsed and normalized records.
- **Is it still current?** Detect changes, refresh stale records, and handle deletions.
- **What changed?** Track versions of sources and their processed representations.
- **How can an application use it?** Provide consistent ways to inspect, search, query, or export the managed information.

KnexGPT aims to collect these responsibilities into a reusable library rather than make each application implement its own data-management pipeline.

## Project focus

The planned core has three areas.

### 1. Data ingestion

Connect to files and external sources, read their contents, parse supported formats, and turn them into consistent records. Sources should have their own identities and ingestion states rather than being treated as one-off file uploads.

### 2. Knowledge and metadata management

Keep source metadata, content representations, relationships, and provenance together. Support structured access to information without requiring an application to understand every upstream data format. Ontologies and richer semantic relationships are longer-term goals, **not implemented features**.

### 3. Context development lifecycle

Here, *context* means information that an application can use together with its source, meaning, and history; it does **not** mean a model or a prompt-serving runtime.

The lifecycle covers registering a source, ingesting and processing it, tracking changes, updating derived representations, handling failures, versioning, and eventually retiring outdated information. The aim is to keep managed information useful and trustworthy over time.

## Intended data flow

This diagram shows the **target design**, not an existing end-to-end pipeline.

~~~text
Files · Websites · APIs · Repositories · Cloud sources
                         |
                  Source registry
            Identity · Configuration · Status
                         |
                 Ingestion and parsing
                         |
                Normalized information
          Content · Documents · Metadata
                         |
            Storage and optional indexes
                         |
                  Query / export APIs
                         |
         Search · Internal tools · Data applications

Across the flow: provenance · change tracking · versioning · access rules
~~~

Storage and indexing should be implementation choices, not requirements imposed on every consumer. Optional retrieval indexes can help applications search the managed data.

## What is in the repository today?

| Area | Existing code | Status |
| --- | --- | --- |
| Knowledge abstractions | `knexgpt/knowledge/knowledge.py`, `content.py`, `protocol.py`, `document/` | Imported Agno Knowledge source; not verified as an independent KnexGPT package |
| Source readers and loaders | `knexgpt/knowledge/reader/`, `loaders/`, `remote_content/` | Source code for several kinds of content; imports and provider dependencies still need work |
| Content representations | `knexgpt/knowledge/chunking/`, `embedder/` | Chunking and embedding code exists as imported source; no verified integrated processing pipeline |
| Retrieval helpers | `knexgpt/knowledge/reranker/`, `query_transformer/` | Imported helper implementations; no validated end-to-end search or query service |
| Storage adapters | `knexgpt/vendor/agno/db/`, `vectordb/` | Vendored Agno source; not a supported KnexGPT storage deployment |
| Earlier experiments | `knexgpt/api/`, `agents/`, `db/`, `parser/`, `messaging/` | Legacy prototypes; they do not form a supported application |
| Source registry, metadata governance, and lifecycle | No integrated service | Planned work; not implemented |

**About the AI-related code:** The repository includes imported embedding, vector database, and reranking implementations, as well as legacy agent experiments. These are part of the repository's history and current source tree; they are **not** a verified KnexGPT model-serving or context-delivery service. Embeddings, where used, are numerical representations for indexing and similarity search. That is different from an API sending embeddings to an LLM. No end-to-end delivery path is currently validated.

## Source layout

~~~text
knexgpt/
├── knowledge/          Imported knowledge abstractions, readers,
│                       representations, and retrieval helpers
├── vendor/agno/        Supporting Agno source and provenance notes
├── api/                Legacy FastAPI prototype
├── agents/             Legacy agent experiments
├── db/                 Legacy storage and graph experiments
├── parser/             Earlier parsing and ingestion code
└── messaging/          Earlier messaging experiments

pyproject.toml          Existing Poetry configuration; incomplete for the import
Dockerfile              Legacy Docker image; not a validated deployment
k8s-deployment.yaml     Legacy deployment sketch
LICENSE                 Apache License 2.0
readme.md               This project overview
~~~

## Development roadmap

The near-term plan is to build and test **general-purpose data-management components**. These are proposed engineering stages, not claims about what already works.

1. **Standalone package foundation.** Identify required imports, isolate vendored dependencies, define supported packages and adapters, and add reproducible unit tests.
2. **Source management.** Introduce stable source IDs, metadata, configuration, status, and basic lifecycle operations.
3. **Ingestion.** Build a tested flow from supported sources to stored records, with clear error reporting and retry behavior.
4. **Parsing and representation.** Normalize documents and extracted content, preserve source references, and validate output.
5. **Metadata and lifecycle.** Track revisions, refreshes, updates, deletions, provenance, and the state of derived records.
6. **Data access.** Expose consistent APIs for inspecting, searching, filtering, and exporting managed information.
7. **Reliability and documentation.** Add integration tests, fixtures, development commands, and examples that work from a clean checkout.

The design should be useful to ordinary data-driven applications without requiring an AI model, agent framework, or inference service. Existing experimental AI-related modules remain explicitly identified above; this roadmap does not imply they have been removed.

## Current limitations

KnexGPT is **not yet a runnable, end-to-end data-management service**.

- The imported Knowledge snapshot still contains `agno.*` imports and dependencies on modules outside the copied source. The included modules are not yet independently importable and tested.
- The legacy `POST /query` endpoint uses mocked context and is not a supported data-query interface.
- A working source registry, governed lifecycle, reliable refresh/version handling, and a consistent public data-access API have not been implemented.
- `pyproject.toml` does not yet cover all dependencies required by the imported Knowledge code.
- The Dockerfile references a missing `requirements.txt`; the Docker and Kubernetes files should not be treated as working deployments.
- There is no verified install-and-run guide or supported release at this stage.

These are known development gaps, not hidden setup steps.

## Getting started

Clone the repository to inspect or contribute to the source:

~~~bash
git clone https://github.com/akeebismail/knexgpt.git
cd knexgpt
~~~

Start with `knexgpt/knowledge/` for the imported Knowledge implementation and [`knexgpt/vendor/agno/UPSTREAM.md`](knexgpt/vendor/agno/UPSTREAM.md) for its source revision, dependencies, and attribution.

**A supported installation and test workflow is still planned.** Do not assume `poetry install` or the existing Dockerfile provides a runnable application.

## Relationship to Cherragon

KnexGPT is a smaller open-source project exploring ideas about ingestion, knowledge organization, and managing data over time. Related ideas also inform **Cherragon**, a broader project. KnexGPT is not a distribution of the full Cherragon platform.

## Upstream code and license

KnexGPT is distributed under the **Apache License 2.0**; see [LICENSE](LICENSE).

The Knowledge source and supporting vendored modules include code copied from [Agno](https://github.com/agno-agi/agno), which is also licensed under Apache License 2.0. The upstream revision, copied paths, known missing dependencies, and provenance are described in [`knexgpt/vendor/agno/UPSTREAM.md`](knexgpt/vendor/agno/UPSTREAM.md). Preserve applicable copyright, license, and notice requirements when modifying or redistributing this code.

## Contributing

Contributions are welcome, particularly around dependency isolation, source-management contracts, reproducible ingestion, lifecycle handling, tests, and documentation.

Please distinguish working code from planned design, keep changes focused, and include tests for behavior that is ready to support.
