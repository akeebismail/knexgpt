from typing import Any, Dict, List
from aioarangodb import ArangoClient
from .adapter import GraphDBAdapter, GraphQuery, GraphResult

class ArangoDBAdapter(GraphDBAdapter):
    """ArangoDB database adapter implementation."""
    
    def __init__(self, url: str, username: str, password: str, database: str):
        self.client = ArangoClient(hosts=url)
        self.db = self.client.db(database, username=username, password=password)
    
    async def connect(self) -> None:
        """Establish connection to ArangoDB database."""
        # Connection is established in the constructor
        pass
    
    async def disconnect(self) -> None:
        """Close ArangoDB connection."""
        self.client.close()
    
    async def execute_query(self, query: GraphQuery) -> GraphResult:
        """Execute an AQL query."""
        cursor = await self.db.aql.execute(query.query, bind_vars=query.parameters or {})
        records = [record async for record in cursor]
        return GraphResult(data=records, metadata={"query": query.query})
    
    async def batch_execute(self, queries: List[GraphQuery]) -> List[GraphResult]:
        """Execute multiple AQL queries in batch."""
        results = []
        for query in queries:
            result = await self.execute_query(query)
            results.append(result)
        return results 