from .neo4j_adapter import Neo4jAdapter
from .arangodb_adapter import ArangoDBAdapter
from .neptune_adapter import NeptuneAdapter
from .adapter import GraphDBAdapter


def create_adapter(db_type: str, **kwargs) -> GraphDBAdapter:
    """Factory function to create a graph database adapter.
    
    Args:
        db_type: The type of the database ('neo4j', 'arangodb', 'neptune').
        **kwargs: Additional arguments for the adapter.
    
    Returns:
        An instance of GraphDBAdapter.
    """
    if db_type == 'neo4j':
        return Neo4jAdapter(**kwargs)
    elif db_type == 'arangodb':
        return ArangoDBAdapter(**kwargs)
    elif db_type == 'neptune':
        return NeptuneAdapter(**kwargs)
    else:
        raise ValueError(f"Unsupported database type: {db_type}") 