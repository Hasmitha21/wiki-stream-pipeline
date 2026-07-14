
  create view "wiki"."analytics"."stg_wiki_events__dbt_tmp"
    
    
  as (
    with ranked as (
    select
        *,
        row_number() over (
            partition by event->'meta'->>'id'
            order by ingested_at
        ) as rn
    from "wiki"."raw"."wiki_events"
    where event->>'type' in ('edit', 'new')
)
select
    id,
    event->'meta'->>'id'                        as event_id,
    event->>'title'                              as title,
    event->>'wiki'                               as wiki,
    event->>'type'                               as event_type,
    event->>'user'                               as editor,
    (event->>'bot')::boolean                     as is_bot,
    to_timestamp((event->>'timestamp')::bigint)  as event_ts,
    (event->'length'->>'new')::int
      - coalesce((event->'length'->>'old')::int, 0) as bytes_changed,
    ingested_at
from ranked
where rn = 1
  );