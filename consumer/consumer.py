import time

import psycopg2
from confluent_kafka import Consumer

TOPIC = "raw_events"
BATCH_SIZE = 500
BATCH_TIMEOUT_S = 5

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "postgres-writer",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="wiki",
    user="pipeline", password="pipeline",
)

INSERT_SQL = """
    INSERT INTO raw.wiki_events (event, kafka_partition, kafka_offset)
    VALUES (%s, %s, %s)
    ON CONFLICT (kafka_partition, kafka_offset) DO NOTHING
"""


def flush(batch):
    with conn.cursor() as cur:
        cur.executemany(INSERT_SQL, batch)
    conn.commit()
    consumer.commit()
    print(f"Wrote {len(batch)} events")


def main():
    consumer.subscribe([TOPIC])
    batch, last_flush = [], time.time()
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            batch.append((msg.value().decode(), msg.partition(), msg.offset()))
        if batch and (len(batch) >= BATCH_SIZE or time.time() - last_flush > BATCH_TIMEOUT_S):
            flush(batch)
            batch, last_flush = [], time.time()


if __name__ == "__main__":
    main()