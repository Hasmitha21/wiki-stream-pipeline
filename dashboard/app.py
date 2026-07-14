import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Wiki Stream Pipeline", layout="wide")
st.title("Wikipedia edits live pipeline")

engine = create_engine(
    "postgresql+psycopg2://pipeline:pipeline@localhost:5432/wiki"
)


@st.cache_data(ttl=60)
def q(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)


k = q("""
    select count(*) as edits,
           count(distinct wiki) as wikis,
           max(event_ts) as latest
    from analytics.stg_wiki_events
""")
c1, c2, c3 = st.columns(3)
c1.metric("Total edits", f"{k.edits[0]:,}")
c2.metric("Distinct wikis", int(k.wikis[0]))
c3.metric("Latest event (UTC)", str(k.latest[0])[:19])

st.subheader("Edits per minute")
epm = q("""
    select minute,
           sum(edit_count) as total,
           sum(bot_edits) as bots
    from analytics.fct_edits_per_minute
    group by minute
    order by minute
""")
st.line_chart(epm.set_index("minute"))

st.subheader("Top wikis — last hour")
top = q("""
    select wiki, sum(edit_count) as edits
    from analytics.fct_edits_per_minute
    where minute > now() - interval '1 hour'
    group by wiki
    order by edits desc
    limit 10
""")
st.bar_chart(top.set_index("wiki"))