CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.wiki_events (
    id              BIGSERIAL PRIMARY KEY,
    event           JSONB NOT NULL,
    kafka_partition INT NOT NULL,
    kafka_offset    BIGINT NOT NULL,
    ingested_at     TIMESTAMPTZ DEFAULT now(),
    UNIQUE (kafka_partition, kafka_offset)
);