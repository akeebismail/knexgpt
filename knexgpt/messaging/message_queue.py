import pika
import json
from typing import Any, Dict

class MessageQueueClient:
    """Client for message queue communication using RabbitMQ."""
    
    def __init__(self, queue_name: str, host: str = 'localhost'):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
    
    def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message to the queue.
        
        Args:
            message: Message to send
        """
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message)
        )
        print(f"Sent message: {message}")
    
    def receive_messages(self, callback) -> None:
        """Receive messages from the queue.
        
        Args:
            callback: Function to call with each received message
        """
        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
        
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=on_message,
            auto_ack=True
        )
        print(f"Waiting for messages in {self.queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()
    
    def close(self) -> None:
        """Close the connection."""
        self.connection.close() 