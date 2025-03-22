# E-commerce Multichannel Messages Streaming Pipeline

## Overview
Build a microservices-based Kubernetes infrastructure to support a Kafka streaming pipeline that performs extract, transform, and load (ETL) operations into PostgreSQL using PySpark.  

## Architecture
![Message_Streaning_Pipeline](images/Architecture_Message_Streaming_Pipeline.png)

The project architecture revolves around seamless data processing pipelines, orchestrated by Kubernetes containers. Events originating from messages offline file are captured in a streaming data producer job, forwarded to a Kafka topic named `messages_data`, processed through a micro-batch PySpark pipeline for transformation, and stored into PostgreSQL. All of the intrastructure are built using Terraform for continuous and stable deployment.

## Data Flow Features
1. **Data Producer**: Scrapes data and continuously publishes it to the Kafka topic `message_data`.
2. **Kafka Message Queue**: Decouples the pipeline using Kafka as a message queue, ensuring flexibility and stability for downstream consumers.
3. **Data Consumer with PySpark**: Cleans and processes streaming message data using PySpark to enable near-realtime ETL.
4. **PostgreSQL Sink**: Writes the cleaned data into PostgreSQL as part of an E-commerce multichannel messaging data mart.


## Setup
1. Install `terraform` and `gcloud` for the following deployment.

2. Run the terraform script if you need to re-deploy your cluster.
    ```bash
    gcloud auth application-default login
    cd terraform/
    terraform init
    terraform apply
    ```
    Make sure your ip is included in the list of authorized network.

3. Connect to cluster to interact with Kubernetes.
    ```bash
    gcloud container clusters get-credentials cluster-1 --zone [zone] --project [project_id]
    ```

4. (Only first time) Annotate default Kubernetes service account (KSA)
    ```bash
    gcloud storage buckets add-iam-policy-binding gs://[bucket_name] \
    --role=roles/storage.objectViewer \
    --member=principal://iam.googleapis.com/projects/[project_number]/locations/global/workloadIdentityPools/[project_id].svc.id.goog/subject/ns/default/sa/default \
    --condition=None
    ```

5. Deploy your pods/jobs with Kubernetes yaml files:
    ```bash
    cd ../kubernetes/
    kubectl apply -f [folder_name]
    ```


## Usage
1. Check the status of `Kubernetes` pods and services.
    ```bash
    kubectl get pods -owide
    kubectl get services 
    ```

2. Monitor `Kafka` producer, consumer, and topic metrics to gain insights into message flow and system performance.
    ```bash
    kubectl exec -it [kafka-pod-name] -- /bin/bash
    cd /bin
    kafka-console-consumer --bootstrap-server kafka-service:9092 --topic message_data --from-beginning
    ```

3. Access the Spark Web UI to monitor Spark job execution:
    ```bash
    kubectl port-forward svc/spark-master-service 8080:8080
    ```
    Then, open "http://localhost:8080" in your browser.

4. Connect to `PostgreSQL` to begin data processing and analytics workloads.
    ```bash
    kubectl exec -it [postgres-pod-name] -- psql -U root -d messaging
    ```
    Access data using SQL statements:
    ```sql
    -- Show all table
    \dt 

    -- Show top 10 records of message data
    select * from messages limit 10;
    ```





