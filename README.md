# GKE for microservice data pipeline

## Setup
0. (Optional) Run the terraform script if you need to re-deploy your cluster.
```shell
gcloud auth application-default login
cd terraform/
terraform init
terraform apply
```
Make sure your ip is included in the list of authorized network.

1. Connect to cluster to interact with Kubernetes.
```shell
gcloud container clusters get-credentials cluster-1 --zone asia-east1-a --project tw-rd-de-finn
```

2. Resize your node if neceesary (terraform default: 1), and re-apply your pods.
```
cluster > cluster-1 > node > default-pool > RESIZE
```
```shell
kubectl apply -f pod.yaml 
kutectl get pods -owide
```

3. Service won't be changed (including external IP), but you also need to start up as re-deploying your cluster. 
```shell
kubectl apply -f service.yaml 
kutectl get services 
```
Check the external ip if you need to access the service through internet.




terraform import google_container_cluster.my_cluster projects/tw-rd-de-finn/locations/asia-east1-a/clusters/cluster-1
terraform import google_container_node_pool.my_node_pool projects/tw-rd-de-finn/locations/asia-east1-a/clusters/cluster-1/nodePools/default-pool