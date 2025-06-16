# simple_producer.py
from kafka import KafkaProducer
import json

KAFKA_BOOTSTRAP_SERVERS = '127.0.0.1:9092'
KAFKA_TOPIC = 'twitter_stream'

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

test_message = {'text': 'Hello, Kafka!', 'created_at': '2023-01-01T00:00:00'}
producer.send(KAFKA_TOPIC, value=test_message)
producer.flush()
