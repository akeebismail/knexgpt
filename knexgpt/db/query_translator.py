from typing import Optional

class QueryTranslator:
    """Translates SPARQL queries to Cypher/Gremlin."""
    
    def translate(self, sparql_query: str, target_language: str) -> Optional[str]:
        """Translate a SPARQL query to the target language.
        
        Args:
            sparql_query: The SPARQL query to translate.
            target_language: The target query language ('cypher' or 'gremlin').
        
        Returns:
            The translated query or None if translation is not possible.
        """
        if target_language == 'cypher':
            return self.translate_to_cypher(sparql_query)
        elif target_language == 'gremlin':
            return self.translate_to_gremlin(sparql_query)
        return None
    
    def translate_to_cypher(self, sparql_query: str) -> str:
        """Translate SPARQL to Cypher."""
        # Basic translation logic for SELECT and WHERE
        if "SELECT" in sparql_query and "WHERE" in sparql_query:
            # Extract the variable and pattern
            variable = sparql_query.split("SELECT")[1].split("WHERE")[0].strip()
            pattern = sparql_query.split("WHERE")[1].strip().strip("{}")
            # Translate to Cypher
            return f"MATCH {pattern} RETURN {variable}"
        return "MATCH (n) RETURN n"
    
    def translate_to_gremlin(self, sparql_query: str) -> str:
        """Translate SPARQL to Gremlin."""
        # Basic translation logic for SELECT and WHERE
        if "SELECT" in sparql_query and "WHERE" in sparql_query:
            # Extract the variable and pattern
            variable = sparql_query.split("SELECT")[1].split("WHERE")[0].strip()
            pattern = sparql_query.split("WHERE")[1].strip().strip("{}")
            # Translate to Gremlin
            return f"g.V().has('{pattern}').values('{variable}')"
        return "g.V()" 