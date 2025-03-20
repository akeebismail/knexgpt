from .base import BaseAgent
from knexgpt.communication.message_queue import MessageQueueClient
import asyncio

class QueryProcessingAgent(BaseAgent):
    """Agent responsible for query processing tasks."""
    
    def __init__(self):
        super().__init__(name="QueryProcessingAgent")
        self.mq_client = MessageQueueClient(queue_name="query_processing")
    
    async def perform_task(self, query: str, *args, **kwargs):
        """Process the user query.
        
        Args:
            query: User query to process
        """
        self.log(f"Processing query: {query}")
        query_results = self.process_query(query)
        return query_results
    
    def process_query(self, query: str) -> dict:
        """Process the user query.
        
        Args:
            query: User query to process
            
        Returns:
            Query results
        """
        # Implement query processing logic here
        return {"query_results": f"Results for query: {query}"}
    
    def start_listening(self):
        """Start listening for incoming messages."""
        self.mq_client.receive_messages(self.handle_message)

    def handle_message(self, message: dict):
        """Handle incoming messages."""
        self.log(f"Received message: {message}")
        if message.get("task") == "process_query":
            query = message.get("data")
            if query:
                asyncio.run(self.perform_task(query)) 