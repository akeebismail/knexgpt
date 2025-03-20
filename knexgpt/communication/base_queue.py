from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseQueue(ABC):
    """Abstract base class for message queue communication."""
    
    @abstractmethod
    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message to the queue."""
        pass
    
    @abstractmethod
    def receive_messages(self, callback) -> None:
        """Receive messages from the queue."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the connection."""
        pass 