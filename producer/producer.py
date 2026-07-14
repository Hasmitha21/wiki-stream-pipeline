import json

import requests
from confluent_kafka import Producer

STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
TOPIC = "raw_events"

producer = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")


def main():
    resp = requests.get(
        STREAM_URL,
        stream=True,
        headers={"User-Agent": "wiki-stream-pipeline/0.1"},
        timeout=30,
    )
    count = 0
    for line in resp.iter_lines():
        if line and line.startswith(b"data: "):
            event = json.loads(line[len(b"data: "):])
            producer.produce(
                TOPIC,
                key=str(event.get("wiki", "")),
                value=json.dumps(event),
                callback=delivery_report,
            )
            producer.poll(0)
            count += 1
            if count % 100 == 0:
                print(f"Produced {count} events")


if __name__ == "__main__":
    main()