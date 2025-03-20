# Multi-Agent Knowledge Graph System

## Description
This project is a multi-agent knowledge graph system that integrates various graph databases and utilizes AI-driven agents to process semi-structured and unstructured data for intelligent querying and retrieval.

## Features
- Ontology creation and management using RDF/OWL.
- Multi-agent architecture for data extraction, enrichment, validation, and querying.
- Support for Neo4j, ArangoDB, and AWS Neptune.
- Natural language querying and retrieval-augmented generation (RAG).
- REST API for interfacing with the knowledge graph.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/akeebismail/knexgpt.git
   cd your-repo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the FastAPI application, run:
```bash
uvicorn knexgpt.api.app:app --host 0.0.0.0 --port 8000
```

You can then access the API at `http://localhost:8000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
