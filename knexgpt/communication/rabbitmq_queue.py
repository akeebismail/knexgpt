import pika
import json
from typing import Any, Dict
from .base_queue import BaseQueue

class RabbitMQQueue(BaseQueue):
    """RabbitMQ client for message queue communication."""
    
    def __init__(self, queue_name: str, host: str = 'localhost'):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
    
    def send_message(self, message: Dict[str, Any]) -> None:
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message)
        )
    
    def receive_messages(self, callback) -> None:
        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
        
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=on_message,
            auto_ack=True
        )
        self.channel.start_consuming()
    
    def close(self) -> None:
        self.connection.close() 