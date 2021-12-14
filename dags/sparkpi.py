from datetime import timedelta, datetime
from airflow.models.dag import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from kubernetes.client import V1Pod, V1PodSpec, V1Container, V1EnvVar, V1ObjectMeta

dag = DAG(
    dag_id="sparkpi",
    default_args={
        'owner': 'jacob.nosal',
        'retries': 1,
        'retry_delay': timedelta(minutes=3)
    },
    description="Dag showing the SparkSubmitOperator's capabilities.",
    schedule_interval="@hourly",
    start_date=datetime(2021, 12, 1),
    params={},
    tags=[],
    catchup=False
)

executor_config = {
    "pod_override": V1Pod(
        metadata=V1ObjectMeta(
            labels={
                "tier": "poc"
            }
        ),
        spec=V1PodSpec(
            containers=[
                V1Container(
                    name="base",
                    image="jacobnosal/airflow:2.2.2",
                    env=[
                        V1EnvVar(name="AIRFLOW__LOGGING__LOGGING_LEVEL", value="DEBUG")
                    ]
                )
            ]
        )
    )
}

spark_job = SparkSubmitOperator(
    task_id='spark_job',
    conn_id='spark-k8s',
    application='local:///opt/spark/examples/jars/spark-examples_2.12-3.2.0.jar', 
    java_class="org.apache.spark.examples.SparkPi",
    application_args=[
        '10000'
    ],
    name="sparkpi",
    spark_binary="/home/airflow/.local/bin/spark-submit",
    conf={
        'spark.executor.instances': '5',
        'spark.kubernetes.container.image':'jacobnosal/spark:3.2.0',
        'spark.kubernetes.namespace': 'airflow', 
        'spark.kubernetes.authenticate.driver.serviceAccountName': 'spark'
    },
    verbose=False,
    dag=dag,
    executor_config=executor_config
)