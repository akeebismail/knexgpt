# KnexGPT

**Open-source knowledge and context infrastructure for AI systems.**

AI applications need more than a vector database or a retrieval call. They need a dependable way to connect to knowledge sources, interpret and organize content, maintain its meaning and metadata, and deliver relevant context to downstream systems.

**KnexGPT explores that infrastructure layer.** It is a smaller, open-source project focused on the foundations of knowledge management and context delivery. It is not intended to be another agent framework, an LLM wrapper, or a collection of RAG demos.

> **Project status: early development.** This repository contains original prototype code and a recently imported Agno Knowledge source snapshot. These pieces are not yet integrated into a complete or production-ready service. The sections below distinguish code present in the repository from the direction of the project.

## Why KnexGPT?

RAG and agent frameworks often focus on what an AI application does *after* it receives context. KnexGPT focuses on the infrastructure needed *before* that point:

- **Knowledge sources:** identify where knowledge comes from and manage its lifecycle and metadata.
- **Ingestion and representation:** load documents and remote content, parse them, and produce useful representations.
- **Knowledge organization:** model relationships, semantics, and ontologies rather than treating every source as an anonymous chunk of text.
- **Retrieval and context delivery:** make relevant knowledge available to LLMs, agents, search, and other consuming applications.
- **Governance:** establish the foundations for provenance, ownership, access rules, and trustworthy updates.

The goal is reusable context infrastructure that can serve different AI systems without requiring each application to rebuild its own knowledge pipeline.

## Intended architecture

```text
Knowledge sources
  Files · Websites · APIs · Cloud storage · Repositories
                       |
              Source management
          Identity · Metadata · Lifecycle
                       |
             Ingestion and parsing
                       |
            Knowledge representation
        Documents · Chunks · Semantics
                       |
              Storage and indexes
         Content · Vector · Graph (goal)
                       |
             Retrieval and assembly
                       |
               Context consumers
           Search · LLMs · Agents · Apps

Cross-cutting goals: provenance · governance · access control · freshness
```

This is a **target architecture**, not a claim that every stage is currently wired together.

## What is in the repository?

| Area | Code present | Current status |
| --- | --- | --- |
| Knowledge abstractions | `knexgpt/knowledge/knowledge.py`, content, document, and protocol modules | Imported Agno Knowledge source; not integrated or validated as a standalone KnexGPT runtime |
| Readers and loading | `knexgpt/knowledge/reader/`, `loaders/`, `remote_content/` | Source implementations for documents, websites, repositories, and cloud storage; provider dependencies and imports need integration |
| Representation | `knexgpt/knowledge/chunking/`, `embedder/` | Chunking and embedding implementations present as source |
| Retrieval support | `knexgpt/knowledge/reranker/`, `query_transformer/` | Source implementations present; no verified end-to-end retrieval service |
| Storage integrations | `knexgpt/vendor/agno/db/`, `vectordb/` | Vendored Agno dependencies and adapters; not a supported KnexGPT storage deployment |
| Legacy prototype | `knexgpt/api/`, `agents/`, `db/`, `parser/`, `messaging/` | Earlier experimental modules; incomplete and not a functioning pipeline |
| Source governance and ontology lifecycle | No integrated KnexGPT service yet | Project direction, **not implemented** |

The imported Agno source still uses `agno.*` imports and relies on modules and third-party packages outside the copied snapshot. It cannot currently be treated as an independently installable or tested KnexGPT Knowledge package.

### Source layout

```text
knexgpt/
├── knowledge/          Knowledge abstractions, readers, loaders,
│                       chunking, embedding, reranking, and page utilities
├── vendor/agno/        Supporting Agno database, vector, and utility source
├── api/                Legacy FastAPI prototype
├── agents/             Legacy agent experiments
├── db/                 Legacy graph adapters and query translation
├── parser/             Early preprocessing and ingestion wrappers
└── messaging/          Queue integration experiments

pyproject.toml          Original Poetry configuration; needs reconciliation
Dockerfile              Legacy image; not a validated deployment path
k8s-deployment.yaml     Legacy Kubernetes deployment sketch
LICENSE                 Apache License 2.0
readme.md               Project overview
```

## Current limitations

KnexGPT is **not yet a working end-to-end knowledge platform**.

- The imported Knowledge code and vendored dependencies have not been namespace-adapted, dependency-resolved, or integration-tested.
- The legacy `POST /query` endpoint is a prototype with mocked context; it is not a knowledge retrieval API. Its referenced querying modules are not present in the current tree.
- There is no integrated knowledge-source registry, ontology lifecycle, policy enforcement, or governed query interface.
- The Poetry dependencies do not yet represent the complete dependency set for the imported Knowledge implementation.
- The Dockerfile references a `requirements.txt` file that is not present. Do not assume the current Docker or Kubernetes configuration can deploy the project.
- No verified installation, test, or production deployment procedure is published for the current repository state.

These are active engineering gaps, not supported features.

## Development direction

Work is intended to proceed from small, testable foundations toward a complete context pipeline:

1. **Make the Knowledge foundation usable.** Resolve imports and actual transitive dependencies, choose supported adapters, and establish tests.
2. **Define knowledge sources as first-class objects.** Give each source stable identity, metadata, configuration, and a lifecycle independent of a particular reader or vector store.
3. **Connect ingestion to representations.** Build a tested path from source to parsed content, chunks, and stored knowledge, including refresh and failure handling.
4. **Build reliable retrieval.** Query indexed knowledge and return usable context with source references.
5. **Add governance and semantics.** Introduce ontology management, provenance, ownership, access controls, and freshness guarantees incrementally.

This is a direction of travel, not a published release schedule or promise that these capabilities already exist.

## Getting started

You can inspect and contribute to the source today:

```bash
git clone https://github.com/akeebismail/knexgpt.git
cd knexgpt
```

Start with `knexgpt/knowledge/` for the knowledge foundation and `knexgpt/vendor/agno/UPSTREAM.md` for the imported source and its known integration gaps.

**There is not yet a supported install-and-run quickstart.** In particular, `poetry install` or building the Dockerfile should not be treated as evidence that the Knowledge service is ready. A reproducible developer setup and integration tests are among the first tasks.

## Relationship to Cherragon

KnexGPT is a compact, open-source exploration of knowledge and context infrastructure ideas that also inform **Cherragon**. It has its own repository and development scope; it is not a distribution of the full Cherragon platform.

## Upstream code and licensing

KnexGPT is distributed under the **Apache License 2.0**; see [LICENSE](LICENSE).

The Knowledge package and supporting vendored modules include source copied from [Agno](https://github.com/agno-agi/agno), also licensed under Apache 2.0. The exact source revision, paths, known missing dependencies, and attribution information are documented in [`knexgpt/vendor/agno/UPSTREAM.md`](knexgpt/vendor/agno/UPSTREAM.md). Retain the relevant upstream license and attribution notices when modifying or redistributing this code.

## Contributing

Contributions are welcome, especially around dependency isolation, reproducible setup, tests, and turning the knowledge-source model into a coherent integration.

Please keep proposed changes focused, include tests for working code, and distinguish implemented behavior from architectural proposals.
