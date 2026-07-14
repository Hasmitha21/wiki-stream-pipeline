from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

DBT = "cd /opt/airflow/transform && dbt {} --profiles-dir ."

with DAG(
    dag_id="wiki_dbt_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="*/15 * * * *",
    catchup=False,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=2)},
) as dag:
    dbt_run = BashOperator(task_id="dbt_run", bash_command=DBT.format("run"))
    dbt_test = BashOperator(task_id="dbt_test", bash_command=DBT.format("test"))

    dbt_run >> dbt_test