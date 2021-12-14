#!/usr/bin/env bash
set -x
spark_submit_bin="$1"

$spark_submit_bin --master k8s://https://promoted-lizard-k8s-b835d116.hcp.westus.azmk8s.io:443 \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=5 \
    --conf spark.kubernetes.container.image=jacobnosal/spark:3.2.0 \
    --conf spark.kubernetes.namespace=airflow \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    local:///opt/spark/examples/jars/spark-examples_2.12-3.2.0.jar \
    10000
