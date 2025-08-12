import os
import time
import json
import uuid
import random
import signal
from datetime import datetime
from confluent_kafka import Producer

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC = os.getenv("TOPIC_NAME", "test-topic")
try:
    MESSAGE_RATE = float(os.getenv("MESSAGE_RATE", "2"))
    if MESSAGE_RATE <= 0:
        raise ValueError()
except Exception:
    MESSAGE_RATE = 2.0

INTERVAL = 1.0 / MESSAGE_RATE

producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})
running = True

def acked(err, msg):
    if err:
        print(f"[producer] Delivery failed: {err}")
    else:
        print(f"[producer] Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

def make_message():
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "value": random.random(),
        "category": random.choice(["alpha", "beta", "gamma", "delta"]),
        "meta": {
            "seq": random.randint(0, 10000)
        }
    }

def shutdown(signum, frame):
    global running
    print(f"[producer] Received signal {signum}, shutting down...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

print(f"[producer] Starting. Producing to {TOPIC} at {MESSAGE_RATE} msg/s (interval={INTERVAL:.3f}s).")
try:
    for seq in range(5):  # Only send 5 messages
    payload = make_message()
    key = str(seq).encode("utf-8")
    value = json.dumps(payload).encode("utf-8")
    producer.produce(TOPIC, key=key, value=value, callback=acked)
    producer.poll(0)
    time.sleep(INTERVAL)
except Exception as e:
    print(f"[producer] Error: {e}")
finally:
    print("[producer] Flushing pending messages...")
    producer.flush(timeout=10)
    print("[producer] Exited.")
