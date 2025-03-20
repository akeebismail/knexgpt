"""
Universal adapter for graph database interactions.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import logging
from urllib.parse import urlparse

from neo4j import AsyncGraphDatabase, AsyncDriver
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class GraphQuery(BaseModel):
    """Base model for graph queries."""
    query: str
    parameters: Optional[Dict[str, Any]] = None

class GraphResult(BaseModel):
    """Base model for graph query results."""
    data: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

class GraphDBAdapter(ABC):
    """Abstract base class for graph database adapters."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the database."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    async def execute_query(self, query: GraphQuery) -> GraphResult:
        """Execute a query on the database.
        
        Args:
            query: Query to execute
            
        Returns:
            Query results
        """
        pass
    
    @abstractmethod
    async def batch_execute(self, queries: List[GraphQuery]) -> List[GraphResult]:
        """Execute multiple queries in batch.
        
        Args:
            queries: List of queries to execute
            
        Returns:
            List of query results
        """
        pass

class Neo4jAdapter(GraphDBAdapter):
    """Neo4j database adapter implementation."""
    
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        database: str = "neo4j"
    ):
        """Initialize Neo4j adapter.
        
        Args:
            uri: Neo4j connection URI
            username: Database username
            password: Database password
            database: Database name
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self._driver: Optional[AsyncDriver] = None
        
    async def connect(self) -> None:
        """Establish connection to Neo4j database."""
        try:
            self._driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            await self._driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close Neo4j connection."""
        if self._driver:
            await self._driver.close()
            logger.info("Disconnected from Neo4j")
    
    async def execute_query(self, query: GraphQuery) -> GraphResult:
        """Execute a Cypher query.
        
        Args:
            query: Cypher query with parameters
            
        Returns:
            Query results
        """
        if not self._driver:
            raise RuntimeError("Not connected to database")
            
        async with self._driver.session(database=self.database) as session:
            result = await session.run(
                query.query,
                parameters=query.parameters or {}
            )
            records = await result.data()
            
            return GraphResult(
                data=records,
                metadata={"query": query.query}
            )
    
    async def batch_execute(self, queries: List[GraphQuery]) -> List[GraphResult]:
        """Execute multiple Cypher queries in batch.
        
        Args:
            queries: List of Cypher queries
            
        Returns:
            List of query results
        """
        results = []
        async with self._driver.session(database=self.database) as session:
            for query in queries:
                result = await session.run(
                    query.query,
                    parameters=query.parameters or {}
                )
                records = await result.data()
                results.append(
                    GraphResult(
                        data=records,
                        metadata={"query": query.query}
                    )
                )
        return results

def create_adapter(
    db_url: str,
    username: str,
    password: str,
    **kwargs
) -> GraphDBAdapter:
    """Factory function to create appropriate database adapter.
    
    Args:
        db_url: Database connection URL
        username: Database username
        password: Database password
        **kwargs: Additional database-specific arguments
        
    Returns:
        Database adapter instance
    """
    parsed_url = urlparse(db_url)
    scheme = parsed_url.scheme.lower()
    
    if scheme in ["neo4j", "neo4j+s", "neo4j+ssc"]:
        return Neo4jAdapter(db_url, username, password, **kwargs)
    # TODO: Add support for other graph databases
    else:
        raise ValueError(f"Unsupported database type: {scheme}") 