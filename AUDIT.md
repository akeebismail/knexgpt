# KnexGPT audit

Date: 21 October 2026. Scope: the git checkout at `/Users/akeebismail/works/kibb/knexgpt`, including uncommitted changes. Application code was not modified. This file is the evidence log for [`readme.md`](readme.md).

## Method

- Read every Python module, `pyproject.toml`, `Dockerfile`, `k8s-deployment.yaml`, `readme.md` as it stood before this rewrite, `.cursor/prd`, and `.cursor/s.txt`.
- Parsed and byte-compiled all 25 modules under `knexgpt/`. No syntax errors.
- Searched the tree for imports, callers, tests, lock files, license files, and CI config.
- Ran the standard-library and locally installed paths below. Did not install `torch`, `transformers`, `metagpt`, or `langchain`, and did not download model weights.
- Read third-party wheels or tarballs where a call site depends on a client API and the package was not installed.

Labels:

| Label | Meaning |
| --- | --- |
| Verified | Executed in the environment below, with the stated stubs or missing services. |
| Inspected | Read from this repository or from a downloaded third-party distribution. Not executed. |
| Not run | No execution and no third-party source check. |

## Environment

| Item | Value |
| --- | --- |
| Host Python | CPython 3.11.7 (`/usr/local/bin/python3`) |
| Audit virtualenv | `/tmp/knexgpt-audit-venv` (not part of the repository) |
| Repository at audit time | `4be0a49b187256ab70f2d25e842fc68de798f1a5` (`repo name`), parent `f74806407d4154e8a3a61e90bd63544f5e3a4ee3` (`knexgpt ontology agent`) |
| Integrated before push | `origin/main` had moved to `6a3736b` (merge of `bd2771e`, which imports `GraphQuery`). The documentation commit was rebased onto that history. |
| Remote | `git@github.com:akeebismail/knexgpt.git` |
| Working tree | `knexgpt/data_processing/chunkr_integration.py` modified, unstaged |
| Poetry | `poetry check` prints `All set!` |
| Lock file | Absent |

Packages installed only in the audit virtualenv, for the checks that needed them:

| Package | Version used | `pyproject.toml` constraint |
| --- | --- | --- |
| rdflib | 7.6.0 | `^7.0.0` (inside range) |
| owlready2 | 0.51 | `^0.45` means `>=0.45,<0.46` (0.51 is outside) |
| fastapi | 0.159.0 | `^0.109.0` (outside range; allows 0.109.x only) |
| pydantic | 2.14.1 | `^2.6.0` (inside range) |
| httpx | 0.28.1 | not declared; pulled in for `TestClient` |
| neo4j | 6.4.1 | `^5.14.0` (outside range; allows 5.x only) |
| pika | 1.4.4 | not declared |
| aioarangodb | 0.1.2 | not declared |
| pytest | 9.1.1 | dev `^8.0.0` (outside that range) |
| pytest-asyncio | 1.4.0 | dev `^0.23.0` (outside that range) |

The Neo4j checks that were executed never opened a driver session, so driver 6 versus 5 does not affect those two exceptions. The HTTP status codes were produced by FastAPI 0.159.0. The route body itself is the three statements in `query_knowledge_graph`. Owlready2 0.51 is also outside `^0.45`. The empty class list was observed on that version. The source calls `get_ontology(base_uri)` rather than `self.world.get_ontology`, and `manager.onto.world is manager.world` was false in that run.

The system interpreter already had `transformers` 4.57.1 and `huggingface_hub` 0.35.3. That interpreter was used only for Hub `model_info` calls. `~/.cache/huggingface/hub/` had no cached `gpt*` snapshot. Weights were not downloaded.

`poetry install` was not run.

## Inventory

25 Python files. No `tests/`, `requirements.txt`, `poetry.lock`, `LICENSE`, `.github/` workflow, example script, or `__main__.py`. Package initializers exist only at `knexgpt/__init__.py` and `knexgpt/agents/__init__.py`.

Git history is two commits by Akeeb Ismail on 20 March 2025: the prototype (`f748064`, 32 files) and a one-line README edit (`4be0a49`). `pyproject.toml` still lists the author as `Your Name <your.email@example.com>`.

`.cursor/prd` is a design note for an ontology-backed multi-agent graph system (RDF/OWL/SHACL, Neo4j, ArangoDB, Neptune, MetaGPT, Chunkr, Firecrawl, RAG, REST or GraphQL, RBAC, GDPR logging, dashboards). `.cursor/s.txt` is the generation prompt that points at that note. Neither file is read at runtime.

## Import matrix

Command: audit virtualenv, repository root on `sys.path`, no stubs. Result is `OK` or the exception from `importlib.import_module`.

| Module | Result |
| --- | --- |
| `knexgpt` | OK |
| `knexgpt.agents` | OK |
| `knexgpt.agents.base` | OK |
| `knexgpt.agents.data_enrichment` | OK (`pika` was installed in this env) |
| `knexgpt.agents.data_extraction` | `ModuleNotFoundError: No module named 'knexgpt.db.neo4j_adapter'` |
| `knexgpt.agents.query_processing` | OK |
| `knexgpt.agents.validation` | OK |
| `knexgpt.api.app` | `ModuleNotFoundError: No module named 'transformers'` |
| `knexgpt.communication.base_queue` | OK |
| `knexgpt.communication.kafka_queue` | `ModuleNotFoundError: No module named 'confluent_kafka'` |
| `knexgpt.communication.message_queue` | OK |
| `knexgpt.communication.message_queue_client` | `ModuleNotFoundError: No module named 'confluent_kafka'` |
| `knexgpt.communication.rabbitmq_queue` | OK |
| `knexgpt.communication.redis_queue` | `ModuleNotFoundError: No module named 'redis'` |
| `knexgpt.data_processing.chunkr_integration` | `ModuleNotFoundError: No module named 'chunkr_ai'` |
| `knexgpt.data_processing.firecrawl_integration` | `ModuleNotFoundError: No module named 'firecrawl'` |
| `knexgpt.data_processing.preprocessing_pipeline` | OK |
| `knexgpt.db.adapter` | OK (`neo4j` was installed) |
| `knexgpt.db.adapter_factory` | `ModuleNotFoundError: No module named 'knexgpt.db.neo4j_adapter'` |
| `knexgpt.db.arangodb_adapter` | OK (`aioarangodb` was installed). Construction is a separate failure, below. |
| `knexgpt.db.neptune_adapter` | `ModuleNotFoundError: No module named 'gremlin_python'` |
| `knexgpt.db.query_translator` | OK |
| `knexgpt.ontology.base` | OK |
| `knexgpt.querying.nl_to_cypher` | `ModuleNotFoundError: No module named 'transformers'` |
| `knexgpt.querying.rag` | `ModuleNotFoundError: No module named 'transformers'` |

On the system interpreter, where `transformers` is installed, `knexgpt.querying.nl_to_cypher` and `knexgpt.querying.rag` import. Importing `knexgpt.api.app` still constructs `RAG()`, which calls the pipeline. An earlier import in that interpreter raised:

```text
OSError: gpt-2 is not a local folder and is not a valid model identifier listed on 'https://huggingface.co/models'
```

A later `huggingface_hub.model_info` call explains that message:

| Model id | `model_info` result |
| --- | --- |
| `gpt-2` (the id in `rag.py`) | `RepositoryNotFoundError`. Response text: `401 Client Error` and `Repository Not Found for url: https://huggingface.co/api/models/gpt-2`. |
| `gpt2` | Resolves to `openai-community/gpt2`, pipeline tag `text-generation`. |
| `Helsinki-NLP/opus-mt-en-cy` | Resolves. Pipeline tag `translation`. Tags include `en` and `cy`. |

The model card at `https://huggingface.co/Helsinki-NLP/opus-mt-en-cy` lists source language `en` and target language `cy`. The OPUS-MT `en-cy` training readme uses the same codes and the Tatoeba `en.cy` set. ISO 639-1 assigns `cy` to Welsh. The card does not describe a Cypher generator. No translation or generation was executed.

## Executed behaviour

### Pytest

`pytest` from the repository root: exit code 5, `no tests ran in 0.01s`.

### `QueryTranslator`

From the repository root, with no extra `PYTHONPATH`:

```text
QueryTranslator().translate("ASK { ?s ?p ?o }", "cypher") == "MATCH (n) RETURN n"
```

Full matrix:

| Target | Input | Output |
| --- | --- | --- |
| `cypher` | `SELECT ?s WHERE { ?s ?p ?o }` | `MATCH  ?s ?p ?o  RETURN ?s` |
| `cypher` | `select ?s where { ?s ?p ?o }` | `MATCH (n) RETURN n` |
| `cypher` | `ASK { ?s ?p ?o }` | `MATCH (n) RETURN n` |
| `cypher` | empty string | `MATCH (n) RETURN n` |
| `gremlin` | `SELECT ?s WHERE { ?s ?p ?o }` | `g.V().has(' ?s ?p ?o ').values('?s')` |
| `gremlin` | lower-case `select`/`where`, `ASK`, or empty | `g.V()` |
| `aql`, `sparql` | any of the inputs above | `None` |

None of these strings were sent to a database.

### `PreprocessingPipeline`

`preprocess({"text": "Hello", "n": 1})` returns the same object.

### `OntologyManager`

Storage directory `/tmp/knexgpt-onto`, base URI `http://example.org/knex/`, RDFLib 7.6.0, Owlready2 0.51.

- The storage directory is created on construction.
- `manager.onto.world is manager.world` is false.
- `list(manager.onto.classes())` is empty before and after `add_class` / `add_property`.
- `add_class("Person", parent_class="Agent")` and an object property `knows` produce triples. `Agent` is only the object of `rdfs:subClassOf`. It is not asserted as `owl:Class`.
- `add_property("age", domain="Person", range_="integer", prop_type="DatatypeProperty")` raises `AssertionError: Object integer must be an rdflib term` after the `owl:DatatypeProperty` and `rdfs:domain` triples are already in the graph.
- `validate()` returns `[]`.
- `save("turtle")` writes `ontology.turtle` (351 bytes, 7 triples). A new manager `load`s that file from 0 triples back to 7.

### Neo4j adapter, no server

`127.0.0.1:7687` refused TCP. `Neo4jAdapter("neo4j://127.0.0.1:7687", "neo4j", "secret")` leaves `_driver is None`.

- `execute_query(GraphQuery(query="RETURN 1"))` raises `RuntimeError: Not connected to database`.
- `batch_execute([GraphQuery(query="RETURN 1")])` raises `AttributeError: 'NoneType' object has no attribute 'session'`.
- URL factory: `neo4j://` and `neo4j+s://` return `Neo4jAdapter`. `bolt://127.0.0.1:7687` raises `ValueError: Unsupported database type: bolt`. `http://127.0.0.1:8529` raises `ValueError: Unsupported database type: http`.

`connect()`, `session.run`, and `result.data()` were not executed.

### ArangoDB adapter

Library: `aioarangodb` 0.1.2. No server on `127.0.0.1:8529`.

- Constructing `ArangoDBAdapter` with no running event loop raises `RuntimeError: no running event loop` inside `aiohttp.ClientSession()`.
- Inside a running loop, `self.db` is a coroutine (`inspect.iscoroutine` true). `self.db.aql` raises `AttributeError: 'coroutine' object has no attribute 'aql'`.
- `client.close()` returns a coroutine. `ArangoDBAdapter.disconnect` does not await it.
- Awaiting `client.db()` manually returns `StandardDatabase`. `execute_query` then raises `ClientConnectorError` for `127.0.0.1:8529`.

Inspected library facts that match those results: `ArangoClient.db` and `ArangoClient.close` are `async def`. `AQL.execute` returns `self._execute(...)`, and `APIWrapper._execute` is `async def`. The cursor implements `__aiter__` / `__anext__`, so the `async for` in `execute_query` matches the library once `self.db` is a database object. The project's `__init__` never awaits `db()`, so that loop is not reached.

### Neptune adapter

`gremlinpython` was not installed. `gremlinpython` 3.8.2 was downloaded and read.

- `Client.__init__` fills a connection pool. `Connection.connect` runs from `Connection.write` when the connection is not yet initialised, not from `Client.__init__`.
- `Client.submitAsync` warns that it is deprecated and returns `submit_async()`, which returns `Connection.write()`, which returns `concurrent.futures.Future`.
- `ResultSet.all()` returns another `concurrent.futures.Future`.

`NeptuneAdapter.execute_query` awaits `submitAsync(...)` and then awaits `.all()`. With a stand-in whose `submitAsync` returns `concurrent.futures.Future()`, the call raises `TypeError: object Future can't be used in 'await' expression`. The second await was not reached. No WebSocket was opened. The `database` parameter is unused. `connect` is `pass`.

`Client.__init__` in that release imports `gremlin_python.driver.aiohttp.transport` and raises `Exception: Please install AIOHTTP...` if that import fails. That import was not executed through `NeptuneAdapter`.

### RabbitMQ client

`127.0.0.1:5672` refused TCP. `MessageQueueClient("data_extraction", host="127.0.0.1")` from `knexgpt.communication.message_queue` raises `pika.exceptions.AMQPConnectionError` (empty message string) on Pika 1.4.4.

### Agents, with stubs

Pika was replaced in `sys.modules` by a connection that records `basic_publish`. `knexgpt.db.neo4j_adapter.Neo4jAdapter` was inserted as an empty stub so `adapter_factory` could finish importing. `gremlin_python` was stubbed for the same reason. Published bodies:

| Caller | Routing key | Body |
| --- | --- | --- |
| `DataEnrichmentAgent.perform_task({"a": 1})` | `data_enrichment` | `{"task": "validate", "data": {"enriched_data": {"a": 1}}}` |
| `ValidationAgent.perform_task({"anything": "broken"})` | `validation` | `{"task": "process_query", "data": {"validation_results": "Data is consistent"}}` |
| `QueryProcessingAgent.perform_task("who knows whom")` | none | return value `{"query_results": "Results for query: who knows whom"}` |

Queue names on the constructed objects: `data_extraction`, `data_enrichment`, `validation`, `query_processing`.

`DataExtractionAgent.perform_task({"a": 1})` raised `NameError: name 'GraphQuery' is not defined` on the file audited before `bd2771e`. The publish list stayed empty. That commit, now on `main`, adds `from knexgpt.db.adapter import GraphQuery`. The `NameError` was not re-run against the updated file. Importing `knexgpt.agents.data_extraction` still fails first, on the missing `knexgpt.db.neo4j_adapter` module.

`extract_data` results: a dict is returned as itself; a `.json` file loads as a dict; a `.csv` file returns a `list` (`[{'name': 'Ada', 'age': '36'}]`); a `.txt` file returns `{"text": "hello text"}`; a missing path returns `{}`.

`process_json_output` on a success object returns `extracted_text`, `title`, `author`, `pages`, and `keywords`. A non-success status returns `{}`.

`DataEnrichmentAgent.handle_message({"task": "other"})` publishes nothing. `handle_message({"task": "enrich", "data": {"x": 1}})` publishes to `data_enrichment`. `ValidationAgent.handle_message` for task `validate` publishes to `validation`. `QueryProcessingAgent.handle_message` for task `process_query` does not publish.

`adapter_factory.create_adapter("postgres")` raises `ValueError: Unsupported database type: postgres` once the missing `neo4j_adapter` module is stubbed. Without that stub the factory module cannot be imported at all, so the `postgres` branch is unreachable in an unmodified tree.

`start_listening` has no callers in the repository. Search covered the Python tree.

### HTTP route, transformers stubbed

`transformers.pipeline` was replaced before importing `knexgpt.api.app`. Recorded constructor calls, in order:

1. `pipeline("text-generation", model="gpt-2")` from `RAG()`.
2. `pipeline("translation", model="Helsinki-NLP/opus-mt-en-cy")` from `NLToCypher()`.

`fastapi.testclient.TestClient` against that app:

| Request | Status | Body |
| --- | --- | --- |
| `POST /query` `{"query": "who knows whom"}` | 200 | `{"response": "Context: Sample context from the knowledge graph.\nQuery: who knows whom\nResponse: ||GENERATED||"}` |
| `POST /query` `{}` | 422 | Pydantic missing-field error at `body.query` |
| `GET /query` | 405 | |
| `GET /` | 404 | |

The string `NOT-CYPHER`, returned by the stub translator, is not in the 200 body. The fixed context string is. Route paths: `/query`, `/docs`, `/docs/oauth2-redirect`, `/redoc`, `/openapi.json`.

This does not show what `gpt-2` or the Marian model would emit. The process never loaded those weights.

### Local ports

TCP connect with a 0.4 second timeout: `5672`, `7687`, and `8529` refused. An HTTP `GET` to `127.0.0.1:8000` returned no bytes within 3 seconds and was not treated as this application. Redis and Kafka clients were not constructed, including where those default ports happened to accept TCP.

## Call graph

| Symbol | Defined in | Imported by |
| --- | --- | --- |
| `app`, `query_knowledge_graph` | `knexgpt/api/app.py` | uvicorn target named by the Dockerfile. No in-repo caller. |
| `NLToCypher`, `RAG` | `knexgpt/querying/` | `knexgpt/api/app.py` only. |
| `OntologyManager` | `knexgpt/ontology/base.py` | no other module. |
| `PreprocessingPipeline`, `WebScraper`, `TextChunker` | `knexgpt/data_processing/` | no other module. |
| `QueryTranslator` | `knexgpt/db/query_translator.py` | `knexgpt/agents/data_extraction.py` only. |
| `create_adapter` (factory) | `knexgpt/db/adapter_factory.py` | `data_extraction.py` only. |
| `create_adapter` (URL) | `knexgpt/db/adapter.py` | no other module. |
| `Neo4jAdapter` | `knexgpt/db/adapter.py` | the URL factory in the same file. The factory module looks for it under `neo4j_adapter`. |
| `MessageQueueClient` (Pika) | `knexgpt/communication/message_queue.py` | all four agents. |
| `MessageQueueClient` (switch) | `knexgpt/communication/message_queue_client.py` | no other module. |
| `KafkaQueue`, `RedisQueue`, `RabbitMQQueue` | `knexgpt/communication/` | the unused switch only. `RabbitMQQueue` duplicates `message_queue.py`. |
| Agent classes | `knexgpt/agents/` | no other module. `agents/__init__.py` does not re-export them. |

## Third-party API mismatches

### Chunkr, working tree

`chunkr-ai` 0.3.7 wheel, not imported:

- `Chunkr.__init__(url=None, api_key=None, raise_on_failure=False)` accepts the keyword used by `TextChunker`.
- `upload` and `close` on the concrete class are `async def`. `TextChunker.upload_pdf` and `TextChunker.close` are synchronous and do not await them. The upload docstring says the return value is a `TaskResponse`. The project annotation is `str`.
- No `chunk` method exists on `Chunkr` or `ChunkrBase`. `chunk_text` calls `self.chunkr.chunk(text)`.

### Chunkr, git HEAD

HEAD content of `knexgpt/data_processing/chunkr_integration.py` is `from chunkr import Chunkr`, `Chunkr(chunk_size=1000)`, and `self.chunkr.chunk(text)`. PyPI `chunkr` 0.3.1 exports `create_chunks_dir`, `create_csv_chunk_iter`, `create_csv_chunk_dir`, `create_parquet_chunk_iter`, and `create_parquet_chunk_dir`. It does not define `Chunkr`. That import was not executed.

The uncommitted diff replaces the HEAD body with the `chunkr_ai` body (API key, `upload_pdf`, `close`).

### Firecrawl

Not installed and not called. Current Firecrawl Python docs show `from firecrawl import Firecrawl` and `firecrawl.scrape(...)`. The project calls `scrape(url)` with one positional argument and annotates the result as `str`. The documented example treats the result as a document object. No pin selects a `firecrawl-py` version.

### PyPI `asyncio` 3.4.3

Wheel inspected, not installed. It contains a top-level `asyncio` package (Tulip, PEP 3156 reference implementation; metadata summary `reference implementation of PEP 3156`). Poetry constraint `asyncio = "^3.4.3"` accepts 3.4.3 and excludes 4.x. Installing it can shadow the standard library module that `data_extraction.py`, `data_enrichment.py`, `validation.py`, and `query_processing.py` import.

## Outstanding issues

### Broken on the paths that were executed

1. **API model id.** `rag.py` requests `gpt-2`. Hub `model_info` returns repository not found. Importing the app constructs `RAG()` immediately, so the server does not start. Generation was not run, including against the id `gpt2` that does resolve.
2. **Translation model is English to Welsh.** `nl_to_cypher.py` loads `Helsinki-NLP/opus-mt-en-cy`. The API discards the result anyway (`cypher_query` is unused). The name of the class and of the local variable describe a different task.
3. **Fixed retrieval context.** `app.py` sets `context = "Sample context from the knowledge graph."` and the comment says this is mocked. `RAG` does not query a graph.
4. **Extraction agent cannot be imported.** `adapter_factory.py` line 1 imports `knexgpt.db.neo4j_adapter`. There is no such file. `Neo4jAdapter` lives in `knexgpt/db/adapter.py`.
5. **`GraphQuery` was unbound during the audit.** With the factory stubbed, `perform_task` raised `NameError` before `execute_query` and before `send_message`. Commit `bd2771e` (`Fix missing GraphQuery import in DataExtractionAgent`), merged as `6a3736b`, adds the import. The updated `perform_task` was not executed. Issue 4 still prevents importing the module.
6. **Agent queues do not meet.** Publishers and consumers use the routing keys in the table above. A message published by one agent is not on the queue the next agent consumes. `start_listening` is never called.
7. **RabbitMQ at construction.** `MessageQueueClient.__init__` opens Pika immediately. With no broker, agent construction raises `AMQPConnectionError`.
8. **ArangoDB client misuse.** Construction requires a running loop, `db()` is not awaited, and `close()` is not awaited. Against a closed port, a manually corrected `db()` then fails with `ClientConnectorError`.
9. **Neptune client misuse.** `await submitAsync(...)` does not accept the `concurrent.futures.Future` that `gremlinpython` 3.8.2 returns. `await result_set.all()` has the same shape and was not reached.
10. **`batch_execute` without a driver.** `Neo4jAdapter.batch_execute` dereferences `_driver` when `execute_query` would raise `RuntimeError`.
11. **Datatype range.** A string `range_` on a datatype property raises `AssertionError` from RDFLib after partial triples are inserted.
12. **Docker install.** `Dockerfile` runs `pip install -r requirements.txt`. That file is not in the tree. Image build was not executed; the `RUN` step has no file to install.
13. **Pytest collects nothing.** Exit code 5. Dev dependencies do not change that.

### Incomplete implementations

14. **Enrichment, validation, and query agents** return a wrapper, the constant `"Data is consistent"`, or `Results for query: ...`. Source comments say the logic is still to be implemented.
15. **`PreprocessingPipeline.preprocess`** returns the input object.
16. **`OntologyManager.validate`** returns `[]` under a TODO comment. SHACL is not referenced.
17. **Owlready2 is unused for edits.** Classes are added only to the RDFLib graph. `self.world` is not the ontology's world.
18. **`QueryTranslator`** is a case-sensitive split on `SELECT` and `WHERE`. It has no AQL target, which is the language `ArangoDBAdapter.execute_query` sends to `db.aql.execute`.
19. **URL factory** accepts `neo4j`, `neo4j+s`, and `neo4j+ssc` only. The comment says other databases are still TODO. `bolt` is rejected.
20. **`process_json_output`** has no caller. It expects a Chunkr-like JSON shape that `TextChunker` does not produce.
21. **CSV annotation.** `extract_data` is annotated `-> dict` and returns a `list` for `.csv` files.
22. **Query task payload.** Validation publishes a dict. `QueryProcessingAgent.perform_task` is annotated as taking `str`. The f-string would stringify a dict if the message arrived. That arrival was not executed.
23. **`message_queue_client.py` imports every backend** at import time, so one missing package blocks the other two.
24. **`adapter_factory.py` imports every adapter** at import time, so the missing Neo4j module blocks ArangoDB and Neptune as well. After that import was stubbed, constructing an ArangoDB adapter still hit the event-loop error.
25. **Neptune `connect`** does not connect. The driver connects on write. The unused `database` argument is not sent as a traversal alias or as request options.
26. **No settings.** Model ids, the mocked context, the SPARQL sample, and the Kafka group id `mygroup` are literals. No `.env` loader is called by project code.
27. **No process supervisor for agents.** There is no module that constructs the four agents and calls `start_listening`.
28. **Logging.** Agents use `logging.getLogger(__name__)`. The package never calls `logging.basicConfig`. Queue sends in `message_queue.py` use `print`. The stub run printed `Sent message: ...` to stdout.

### Declared and unused, or undeclared and required

29. **Unused declarations:** `metagpt`, `langchain`, `torch` (no direct import), `python-dotenv`, `uvicorn` (launcher only), `aiohttp` (no direct import).
30. **Undeclared imports:** `pika`, `aioarangodb`, `gremlinpython`, `confluent_kafka`, `redis`, `firecrawl` / `firecrawl-py`, `chunkr_ai` (working tree), `chunkr` (HEAD).
31. **Harmful declaration:** PyPI `asyncio` 3.4.3, as above.
32. **No lock file.** `poetry check` does not pin transitive versions.
33. **Placeholder author.** `pyproject.toml` authors field was not updated to the git author.

### Deployment and license

34. **Kubernetes manifest** is a Deployment of image `knexgpt:latest` with three replicas and `containerPort: 8000`. No Service, environment, command, probes, or resources. The app has no health route.
35. **License is not established.** The previous README said MIT and linked to `LICENSE`. There is no `LICENSE` file and no license field in `pyproject.toml`.
36. **Previous README overstated the tree.** It listed RDF/OWL management, multi-agent extraction, enrichment, validation, and querying, support for three databases, natural-language RAG, and a REST API as features, and it documented `pip install -r requirements.txt` plus `cd your-repo`. Those install steps cannot be followed as written.

### Design notes with no code

From `.cursor/prd`, with no corresponding implementation found in the Python tree: SHACL, MetaGPT roles, Gremlin as a supported query path that actually runs, GraphQL, visualization or dashboards, RBAC, GDPR controls, and audit logging of data transactions. Cypher execution exists only as uncalled methods on `Neo4jAdapter`.

## Not run

- `poetry install` and any resolution of `torch`, `transformers`, `metagpt`, or `langchain`.
- Pipeline inference for either model, including a corrected `gpt2` id.
- `Neo4jAdapter.connect` and `session.run`.
- A live ArangoDB or Neptune endpoint.
- `gremlinpython` imported through `NeptuneAdapter` (the Future failure used a stand-in with the same return type as 3.8.2).
- Firecrawl `scrape`, Chunkr `upload` / `chunk` / `close`, Kafka, and Redis.
- Docker build and any Kubernetes apply.
- Installing the PyPI `asyncio` wheel on top of CPython 3.11.
- Browser walkthrough. No application code changed, and the uvicorn process cannot get past import in the environments above.

## File status after this audit

Documentation written:

- `readme.md` replaced with a description of the current tree.
- `AUDIT.md` added.

`knexgpt/data_processing/chunkr_integration.py` remains the pre-existing uncommitted edit. No other application file was changed.
