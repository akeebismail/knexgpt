from transformers import pipeline

class RAG:
    """Class for Retrieval-Augmented Generation."""
    
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt-2')
    
    def generate_response(self, context: str, query: str) -> str:
        """Generate a response using RAG.
        
        Args:
            context: The context retrieved from the knowledge graph.
            query: The user's query.
        
        Returns:
            A generated response.
        """
        input_text = f"Context: {context}\nQuery: {query}\nResponse:"
        response = self.generator(input_text, max_length=100, num_return_sequences=1)
        return response[0]['generated_text'] 