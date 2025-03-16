# Messages Streaming Pipeline

## Overview
Build a microservices-based Kubernetes infrastructure to support a Kafka streaming pipeline that performs extract, transform, and load (ETL) operations into PostgreSQL using PySpark.  

## Architecture

## Features
1. **Data Producer**: Scrapes data and continuously publishes it to the Kafka topic message_data.
2. **Kafka Message Queue**: Decouples the pipeline using Kafka as a message queue, ensuring flexibility for downstream consumers.
3. **Data Consumer with PySpark**: Cleans and processes streaming message data using PySpark to enable real-time ETL.
4. **PostgreSQL Sink**: Writes the cleaned data into PostgreSQL as part of an E-commerce multichannel messaging data mart.

## How It Works

## Setup
1. Run the terraform script if you need to re-deploy your cluster.
```shell
gcloud auth application-default login
cd terraform/
terraform init
terraform apply
```
Make sure your ip is included in the list of authorized network.

2. Connect to cluster to interact with Kubernetes.
```shell
gcloud container clusters get-credentials cluster-1 --zone [zone] --project [project_id]
```

3. Annotate default service account
```
kubectl annotate serviceaccount --namespace default default iam.gke.io/gcp-service-account=365750068155-compute@developer.gserviceaccount.com
```


## Usage
1. Deploy your pods/jobs with Kubernetes yaml files:
```shell
kubectl apply -f [folder_name]
```

2. Check the status
```shell
kutectl get pods -owide
kutectl get services 
```

3. Configmap
```
kubectl create configmap data-consumer-config --from-file=../streaming_consumer/data_consumer.py
kubectl exec -it [spark-master-xxx] -- bash

spark-submit \
--master spark://spark-master-service:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5 \
/app/data_consumer.py
```

4. Spark UI
```
kubectl port-forward svc/spark-master-service 8080:8080
```
Check the external ip if you need to access the service through internet.




