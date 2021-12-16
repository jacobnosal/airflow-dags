from datetime import timedelta, datetime
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from kubernetes.client import V1Pod, V1PodSpec, V1Container, V1EnvVar, V1ObjectMeta

dag = DAG(
    dag_id="data_science_owned_dag",
    default_args={
        'owner': 'jacob.nosal',
        'retries': 1,
        'retry_delay': timedelta(minutes=3)
    },
    description="Dag demonstrating templating and RBAC capabilities.",
    schedule_interval="@hourly",
    start_date=datetime(2021, 12, 1),
    params={
        'start_date': '12-01-2021'
    },
    tags=['data_sci'],
    catchup=False,
    access_control={
        "data_science": {"can_read", "can_edit"},
        "data_mgmt": {"can_read"}
    }
)

spark_job = BashOperator(
    dag=dag,
    task_id="some_bash",
    bash_command="""
        echo "This dag has a start date of {{ params.start_date }} but that is user generated."
        echo "This dag run executes at the end of the time interval that it represents."
        echo "That means that {{ data_interval_start }} is the 'Time' that the dag run represents"
        echo "but, the dag executes at {{ data_interval_end }}. This really only matters when the"
        echo "schedule is set to a long window, like quarterly. Ask me how I know this."
        echo "Access a connection string {{ conn.spark_k8s }} is easy. Same goes for vars."
        echo "This is jinja templating so we can also create our own macros. This is how most"
        echo "problems are solved in airflow."
    """
)