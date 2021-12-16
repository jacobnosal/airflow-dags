from datetime import timedelta, datetime
from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import V1Pod, V1PodSpec, V1Container, V1EnvVar, V1ObjectMeta

dag = DAG(
    dag_id="kubernetes_pod",
    default_args={
        'owner': 'jacob.nosal',
        'retries': 1,
        'retry_delay': timedelta(minutes=3)
    },
    description="Dag showing the KubernetesPodOperator capabilities.",
    schedule_interval="@hourly",
    start_date=datetime(2021, 12, 1),
    params={},
    tags=[],
    catchup=False
)

pod_task = KubernetesPodOperator(
    dag=dag,
    task_id='pod_task',
    namespace='airflow',
    get_logs=True,
    service_account_name='airflow-worker',
    is_delete_operator_pod=True,
    log_events_on_failure=True,
    pod_template_file="/opt/airflow/dags/templates/pod_template.yaml"
)