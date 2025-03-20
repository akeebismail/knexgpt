from typing import Any, Dict
from .base_queue import BaseQueue
from .kafka_queue import KafkaQueue
from .rabbitmq_queue import RabbitMQQueue
from .redis_queue import RedisQueue

class MessageQueueClient:
    """Client for message queue communication."""
    
    def __init__(self, queue_type: str, **kwargs):
        if queue_type == 'kafka':
            self.queue: BaseQueue = KafkaQueue(**kwargs)
        elif queue_type == 'rabbitmq':
            self.queue: BaseQueue = RabbitMQQueue(**kwargs)
        elif queue_type == 'redis':
            self.queue: BaseQueue = RedisQueue(**kwargs)
        else:
            raise ValueError(f"Unsupported queue type: {queue_type}")
    
    def send_message(self, message: Dict[str, Any]) -> None:
        self.queue.send_message(message)
    
    def receive_messages(self, callback) -> None:
        self.queue.receive_messages(callback)
    
    def close(self) -> None:
        self.queue.close() 