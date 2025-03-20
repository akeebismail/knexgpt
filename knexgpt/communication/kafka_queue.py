from confluent_kafka import Producer, Consumer, KafkaError
import json
from typing import Any, Dict
from .base_queue import BaseQueue

class KafkaQueue(BaseQueue):
    """Kafka client for message queue communication."""
    
    def __init__(self, topic: str, bootstrap_servers: str = 'localhost:9092'):
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([self.topic])
    
    def send_message(self, message: Dict[str, Any]) -> None:
        self.producer.produce(self.topic, json.dumps(message))
        self.producer.flush()
    
    def receive_messages(self, callback) -> None:
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    break
            message = json.loads(msg.value().decode('utf-8'))
            callback(message)
    
    def close(self) -> None:
        self.consumer.close() 