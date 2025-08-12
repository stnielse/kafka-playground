import os
import time
from confluent_kafka import Consumer

bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
topic = os.getenv("TOPIC_NAME", "test-topic")

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
}

time.sleep(12)

consumer = Consumer(conf)
consumer.subscribe([topic])

print(f"Consumer started. Listening to '{topic}'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(f"Consumed: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
