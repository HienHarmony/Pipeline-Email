import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Đường dẫn đến script Python
result_script_path = "/opt/airflow/dags/result.py"

# Các tham số mặc định của DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Định nghĩa DAG
with DAG(
    dag_id='email_pipeline',  # Tên DAG
    default_args=default_args,
    description='A DAG to run result.py every 5 minutes',
    schedule='*/5 * * * *',  # Lịch chạy (mỗi 5 phút)
    start_date=datetime(2024, 11, 15),
    catchup=False,  # Không chạy lại các DAG chưa chạy trong quá khứ
) as dag:

    # Task BashOperator để chạy file result.py
    run_result_script = BashOperator(
        task_id='run_result_script',
        bash_command=f'python {result_script_path}',  # Lệnh chạy Python script
    )

    # Thiết lập DAG
    run_result_script
