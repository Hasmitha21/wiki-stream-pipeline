select
    date_trunc('minute', event_ts)        as minute,
    wiki,
    count(*)                              as edit_count,
    count(*) filter (where is_bot)        as bot_edits,
    sum(bytes_changed)                    as net_bytes_changed
from {{ ref('stg_wiki_events') }}
group by 1, 2