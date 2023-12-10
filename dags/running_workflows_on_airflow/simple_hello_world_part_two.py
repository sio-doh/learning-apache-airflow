from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'siobhan.doherty',
}

dag = DAG(
    dag_id = 'hello_world_two',
    description = 'Our second "Hello World" DAG!',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['beginner', 'bash', 'hello world']
)

task = BashOperator(
    task_id = 'hello_world_task_two',
    bash_command = 'echo Hello world once again!',
    dag = dag
)

task
