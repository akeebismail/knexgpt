from transformers import pipeline

class NLToCypher:
    """Class for translating natural language to Cypher."""
    
    def __init__(self):
        self.translator = pipeline('translation', model='Helsinki-NLP/opus-mt-en-cy')
    
    def translate(self, nl_query: str) -> str:
        """Translate a natural language query to Cypher.
        
        Args:
            nl_query: The natural language query.
        
        Returns:
            A Cypher query.
        """
        translation = self.translator(nl_query, max_length=100)
        return translation[0]['translation_text'] 