import redis
import json
from typing import Any, Dict
from .base_queue import BaseQueue

class RedisQueue(BaseQueue):
    """Redis client for message queue communication."""
    
    def __init__(self, queue_name: str, host: str = 'localhost', port: int = 6379):
        self.queue_name = queue_name
        self.client = redis.StrictRedis(host=host, port=port, decode_responses=True)
    
    def send_message(self, message: Dict[str, Any]) -> None:
        self.client.rpush(self.queue_name, json.dumps(message))
    
    def receive_messages(self, callback) -> None:
        while True:
            _, message = self.client.blpop(self.queue_name)
            callback(json.loads(message))
    
    def close(self) -> None:
        self.client.close() 