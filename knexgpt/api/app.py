from fastapi import FastAPI
from pydantic import BaseModel
from knexgpt.querying.rag import RAG
from knexgpt.querying.nl_to_cypher import NLToCypher

app = FastAPI()
rag = RAG()
nl_to_cypher = NLToCypher()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_knowledge_graph(request: QueryRequest):
    # Translate natural language to Cypher
    cypher_query = nl_to_cypher.translate(request.query)
    # Retrieve context from the knowledge graph (mocked for now)
    context = "Sample context from the knowledge graph."
    # Generate a response using RAG
    response = rag.generate_response(context, request.query)
    return {"response": response} 