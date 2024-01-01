import pandas as pd 
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator
import os 

INSURANCE = os.getenv("INSURANCE")

default_args = {
    'owner': 'siobhan.doherty'
}

def read_csv_file():
    df = pd.read_csv(INSURANCE)
    print(df)
    return df.to_json()

def remove_null_values(ti):
    json_data = ti.xcom_pull(task_ids='read_csv_file')
    df = pd.read_json(json_data)
    df = df.dropna()
    print(df)
    return df.to_json()

def groupby_smoker(ti):
    json_data = ti.xcom_pull(task_ids='remove_null_values')
    df = pd.read_json(json_data)

    smoker_df = df.groupby('smoker').agg({
        'age': 'mean',
        'bmi': 'mean',
        'charges': 'mean'
    }).reset_index()

    smoker_df.to_csv(GROUPED_BY_SMOKER, index=False)

def groupby_region(ti):
    json_data = ti.xcom_pull(task_ids='remove_null_values')
    df = pd.read_json(json_data)

    region_df = df.groupby('region').agg({
        'age': 'mean',
        'bmi': 'mean',
        'charges': 'mean'
    }).reset_index()

    region_df.to_csv(GROUPED_BY_REGION, index=False)

with DAG(
    dag_id = 'python_pipeline_II',
    description = 'Running a Python pipeline', 
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['python', 'transform', 'pipeline']
) as dag:
    read_csv_file = PythonOperator(
        task_id = 'read_csv_file',
        python_callable = read_csv_file
    )

    remove_null_values = PythonOperator(
        task_id = 'remove_null_values',
        python_callable = remove_null_values
    )

    groupby_smoker = PythonOperator(
        task_id = 'groupby_smoker',
        python_callable = groupby_smoker
    )

    groupby_region = PythonOperator(
        task_id = 'groupby_region',
        python_callable = groupby_region
    )

read_csv_file >> remove_null_values >> [groupby_smoker, groupby_region]

