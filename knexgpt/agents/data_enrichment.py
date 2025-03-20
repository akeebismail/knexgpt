from .base import BaseAgent
from knexgpt.communication.message_queue import MessageQueueClient
import asyncio

class DataEnrichmentAgent(BaseAgent):
    """Agent responsible for data enrichment tasks."""
    
    def __init__(self):
        super().__init__(name="DataEnrichmentAgent")
        self.mq_client = MessageQueueClient(queue_name="data_enrichment")
    
    async def perform_task(self, data: dict, *args, **kwargs):
        """Enhance the knowledge graph with additional relationships.
        
        Args:
            data: Data to enrich
        """
        self.log("Enriching data")
        enriched_data = self.enrich_data(data)
        self.mq_client.send_message({"task": "validate", "data": enriched_data})
        return enriched_data
    
    def enrich_data(self, data: dict) -> dict:
        """Enrich data with additional relationships.
        
        Args:
            data: Data to enrich
            
        Returns:
            Enriched data
        """
        # Implement enrichment logic here
        return {"enriched_data": data}
    
    def start_listening(self):
        """Start listening for incoming messages."""
        self.mq_client.receive_messages(self.handle_message)

    def handle_message(self, message: dict):
        """Handle incoming messages."""
        self.log(f"Received message: {message}")
        if message.get("task") == "enrich":
            data = message.get("data")
            if data:
                asyncio.run(self.perform_task(data)) 