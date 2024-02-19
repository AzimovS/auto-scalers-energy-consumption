# Install Sockshop application with KEPLER

## Login to Azure service

You have to deploy Azure resources using Terraform.

> You will need to login to Azure using the `az login` command before you begin

## Terraform

This repo includes a sample terraform file to deploy Sockshop application and KEPLER with the following commands

```bash
# drop into proper directory
cd infrastructure/azure/

# initialize terraform plugins
terraform init

# deploy resources
terraform apply

# set variables to connect to aks cluster
export RESOURCE_GROUP=$(terraform output -raw green_name)
export LOCATION=$(terraform output -raw green_location)
export CLUSTER_NAME=$(terraform output -raw aks_name)


# get back to repository root 
cd ../../

```

> This deployment can take 5 minutes to provision.

<br/>

Retrieve the `.kube/config` file with the following code:

```bash
az aks get-credentials \
 --resource-group $RESOURCE_GROUP \
 --name $CLUSTER_NAME
```

Test your connectivity to the AKS cluster.

```bash
kubectl cluster-info
```

## Install Sockshop Application

```bash
kubectl apply -f Application-Deployment/complete-demo.yaml
```
It will take around 5-10 mins. You can monitor the pods state the following command:
```bash
kubectl get po -n sock-shop-g -w
```

To get an access to the website, get url with this command:
```bash
echo "http://$(kubectl get svc frontend-external -n sock-shop-g -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"
```

If it doesn't open, try to open the website again with a new tab.

## Install Kube-prometheus

```bash
kubectl apply --server-side -f infrastructure/kepler-prometheus/manifests/setup
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
kubectl apply -f infrastructure/kepler-prometheus/manifests/
```
It will take around 8-10 mins. You can monitor the pods state the following command:
```bash
kubectl get po -n monitoring -w
```


## Install KEPLER

We already generated the deployment file. If you want to generate yourself follow the instructions from [Here](https://sustainable-computing.io/installation/kepler/#build-manifests). The following command will deploy kepler.

```bash
kubectl apply -f kepler/generated-manifest/deployment.yaml
```

To get an access to prometheus, you can use port-forward:

```bash
kubectl port-forward service/prometheus-k8s -n monitoring 9090:9090
```

This will run the pods required for monitoring using Prometheus and Grafana. We can then use port-forwarding to access the Prometheus Web application and Grafana dashboard locally.
```bash
kubectl port-forward service/prometheus-k8s --namespace=monitoring 9090:9090
```

```bash
kubectl port-forward service/grafana --namespace=monitoring 3000:3000
```

You can access the Grafan on http://localhost:3000/. The username: admin and password: admin.
Also you need to import dashboard with the following [json file](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json).

## Clean up

When you are done testing, delete the resources using the following command.

```bash
az group delete --resource-group $RESOURCE_GROUP
```

If you deployed the Azure resources using Terraform, you can run this command instead.

```bash
cd infrastructure/azure/
terraform destroy
```