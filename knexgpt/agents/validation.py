from .base import BaseAgent
from knexgpt.communication.message_queue import MessageQueueClient
import asyncio

class ValidationAgent(BaseAgent):
    """Agent responsible for validation tasks."""
    
    def __init__(self):
        super().__init__(name="ValidationAgent")
        self.mq_client = MessageQueueClient(queue_name="validation")
    
    async def perform_task(self, data: dict, *args, **kwargs):
        """Validate the data for consistency.
        
        Args:
            data: Data to validate
        """
        self.log("Validating data")
        validation_results = self.validate_data(data)
        self.mq_client.send_message({"task": "process_query", "data": validation_results})
        return validation_results
    
    def validate_data(self, data: dict) -> dict:
        """Validate data for consistency.
        
        Args:
            data: Data to validate
            
        Returns:
            Validation results
        """
        # Implement validation logic here
        return {"validation_results": "Data is consistent"}
    
    def start_listening(self):
        """Start listening for incoming messages."""
        self.mq_client.receive_messages(self.handle_message)

    def handle_message(self, message: dict):
        """Handle incoming messages."""
        self.log(f"Received message: {message}")
        if message.get("task") == "validate":
            data = message.get("data")
            if data:
                asyncio.run(self.perform_task(data)) 