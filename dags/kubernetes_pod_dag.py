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

# https://github.com/apache/airflow/blob/af0fb4f1a632ccc11fe22ea906d9a0fb1187cf91/airflow/kubernetes/pod_generator.py#L224
# https://github.com/apache/airflow/blob/af0fb4f1a632ccc11fe22ea906d9a0fb1187cf91/airflow/providers/cncf/kubernetes/operators/kubernetes_pod.py#L436
pod_task = KubernetesPodOperator(
    dag=dag,
    task_id='pod_task',
    namespace='airflow',
    get_logs=True,
    name="curler",
    service_account_name='airflow-worker',
    is_delete_operator_pod=True,
    log_events_on_failure=True,
    pod_template_file="/opt/airflow/dags/repo/dags/templates/pod_template.yaml"
)