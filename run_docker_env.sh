#!/usr/bin/env bash

set -x

docker run -it \
    --rm \
    -v /Users/jacobnosal/.kube:/opt/kube \
    -v /Users/jacobnosal/Documents/projects/airflow-dags/scripts:/opt/scripts \
    -e KUBECONFIG=/opt/kube/config \
    jacobnosal/spark:3.2.0 \
    /bin/bash