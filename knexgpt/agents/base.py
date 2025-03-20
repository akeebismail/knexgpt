"""
Base class for agents in the multi-agent system.
"""
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str):
        """Initialize the agent with a name.
        
        Args:
            name: Name of the agent
        """
        self.name = name
        logger.info(f"Initialized agent: {self.name}")
    
    @abstractmethod
    async def perform_task(self, *args, **kwargs):
        """Perform the agent's designated task."""
        pass

    def log(self, message: str) -> None:
        """Log a message with the agent's name.
        
        Args:
            message: Message to log
        """
        logger.info(f"[{self.name}] {message}") 