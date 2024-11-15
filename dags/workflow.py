import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

result_script_path = "/opt/airflow/dags/result.py"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'email_pipeline',
    default_args=default_args,
    description='A DAG to run result.py every 5 minutes',
    schedule_interval='*/5 * * * *',  
    start_date=datetime(2024, 11, 15),
    catchup=False,
) as dag:
    run_result_script = BashOperator(
        task_id='run_result_script',
        bash_command=f'python {result_script_path}',  
    )

    run_result_script
