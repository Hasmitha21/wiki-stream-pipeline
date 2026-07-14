select
    id,
    event->>'title'                              as title,
    event->>'wiki'                               as wiki,
    event->>'type'                               as event_type,
    event->>'user'                               as editor,
    (event->>'bot')::boolean                     as is_bot,
    to_timestamp((event->>'timestamp')::bigint)  as event_ts,
    (event->'length'->>'new')::int
      - coalesce((event->'length'->>'old')::int, 0) as bytes_changed,
    ingested_at
from {{ source('raw', 'wiki_events') }}
where event->>'type' in ('edit', 'new')