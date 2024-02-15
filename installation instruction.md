# Install with Azure Kubernetes Service

## Prerequisites

* An Azure Subscription (e.g. [Free](https://aka.ms/azure-free-account) or [Student](https://aka.ms/azure-student-account) account)
* [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) with [Azure Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/install#azure-cli) installed
* [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [`kubectl` CLI](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* [Helm CLI](https://helm.sh/docs/intro/install/)
* Bash shell (e.g. macOS, Linux, [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/windows/wsl/about), [Multipass](https://multipass.run/), [Azure Cloud Shell](https://docs.microsoft.com/azure/cloud-shell/quickstart), [GitHub Codespaces](https://github.com/features/codespaces), etc)
* OPTIONAL: [Terraform CLI](https://www.terraform.io/downloads)

> If you do not have all the tools listed above, you can launch the [GitHub Codespaces](https://github.com/features/codespaces) environment which has all the tools pre-installed.

## Clone repo

Use Git CLI to clone this repo and drop into the directory
<!-- 
# To fix
```bash
git clone https://github.com/HabsB/Green-Autoscaling/tree/main/greenScalingversion
cd Green-Autoscaling
``` -->

## Deploy Azure Infrastructure

You have to deploy Azure resources using Terraform.

> Regardless of the option you choose, you will need to login to Azure using the `az login` command before you begin

## Terraform

This repo includes a sample terraform file to deploy Azure Cache for Redis and Azure Kubernetes Service with the following commands

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
## Install KEPLER

Detailed energy consumption measurement at a granular level (energy consumption per pod) using Kepler to assess the autoscaler’s impact on individual pods. the deployment detail of Kepler is provided in the following link[https://sustainable-computing.io/installation/kepler/]


## Install KEDA

As the name suggest, KEDA is a requirement for this operator. A sample manifest is available in this repo to install KEDA v2.10.0.

```bash
kubectl apply -f keda-2.10.0.yaml

# wait for external metrics
kubectl wait --for=condition=Available --timeout=600s apiservice v1beta1.external.metrics.k8s.io
```

## Deploy the SockShop Microservices Web Application

```bash
kubectl apply -f Application-Deployment/complete-demo.yaml
```

Finally, scale the `different sock-shop microservices` app using KEDA's CPU trigger.

```bash
kubectl apply -f Scalers/autoscaling-complete.yaml
```

## Install Carbon Intensity Exporter Operator

To test with real data from the Carbon Aware SDK, head over to this [repo](https://github.com/Azure/kubernetes-carbon-intensity-exporter/) and follow the instructions in the [README.md](https://github.com/Azure/kubernetes-carbon-intensity-exporter/blob/main/README.md) to install the operator into the AKS cluster.

> IMPORTANT: You must have WattTime API credentials to use this operator

If you do not have WattTime API credentials you can skip this step and still test this operator using mock carbon intensity data

```bash
git clone https://github.com/Azure/kubernetes-carbon-intensity-exporter.git
cd kubernetes-carbon-intensity-exporter
```
# wait a few seconds and note the number of replicas that are ready now
kubectl get hpa -w -n sock-shop-g
Using Helm, install the Carbon Intensity Exporter Operator into the AKS cluster.

```bash
export WATTTIME_USERNAME="DanB" 
export WATTTIME_PASSWORD="aj)NwBf~IbF+"
export REGION=westus

helm install carbon-intensity-exporter oci://ghcr.io/azure/kubernetes-carbon-intensity-exporter/charts/carbon-intensity-exporter \
  --version v0.3.0 \
  --set carbonDataExporter.region=$REGION \
  --set wattTime.username=$WATTTIME_USERNAME \
  --set wattTime.password=$WATTTIME_PASSWORD

# go back to repo directory
cd ../
```

Verify carbon intensity data is in place.

```bash
# ensure the status of the carbon intensity exporter operator pod is running
kubectl get po -n kube-system -l app.kubernetes.io/name=carbon-intensity-exporter

# get configmap data SHOULD BE FIXED
kubectl get cm -n kube-system carbon-intensity -o jsonpath='{.data}' | jq
```

You can view the carbon intensity values with the following command.

```bash
# get carbon intensity binary data SHOULD BE FIXED
kubectl get cm -n kube-system carbon-intensity -o jsonpath='{.binaryData.data}' | base64 --decode | jq
```

## Install Carbon Aware KEDA Operator


Currently KEDA is scaling your workload as needed and will scale up to a maximum of 10 replicas (KEDA's default) if needed. We will now add carbon awareness to it, so that it's maximum replicas is capped based on carbon intensity.

Install the latest version of the operator. At the writing moment it was v0.2.0.

> Latest release versions can be found here 👉 https://github.com/Azure/carbon-aware-keda-operator/releases/

```bash
export version="v0.2.0"
kubectl apply -f "https://github.com/Azure/carbon-aware-keda-operator/releases/download/${version}/carbonawarekedascaler-${version}.yaml"
```

With the operator installed, we can now deploy a custom resource called `CarbonAwareKedaScaler` to set the max replicas KEDA can scale up to based on carbon intensity.

> IMPORTANT: If the Carbon Intensity Exporter Operator was NOT installed from the step above, make sure `mockCarbonForecast` is set to `true` to use mock data in the below mentioned file.

```bash
kubectl apply -f Scalers/carbonawarescaler.yaml
```

Check the status of the custom resource.

```bash
kubectl describe carbonawarekedascalers.carbonaware.kubernetes.azure.com carbon-aware-orders-scaler
```

Inspect operator logs.

```bash
kubectl logs -n carbon-aware-keda-operator-system -l control-plane=controller-manager
```

### Visualize Carbon Aware KEDA Operator

Inspecting operator logs and status/events of the custom resource is great. What's better? Visualizing the data in Grafana!

Each time the operator reconciles, it writes custom metrics (e.g., Carbon Intensity, Max Replicas, and Max Replicas) to the `/metrics` endpoint so that Prometheus can scape the data and visualized using Grafana.

This repo include manifests to deploy `kube-prometheus` into the cluster which is configured to scrape from the operator's namespace: `carbon-aware-keda-operator-system`.

Install the Prometheus operator.
fix with
https://github.com/prometheus-operator/kube-prometheus?tab=readme-ov-file

```bash
kubectl apply --server-side -f infrastructure/prometheus/manifests/setup
kubectl wait --for condition=Established --all CustomResourceDefinition --namespace=monitoring
```

Deploy `ServiceMonitor` into the cluster.

```bash
kubectl apply -f - <<EOF 
apiVersion: monitoring.coreos.com/v1  
kind: ServiceMonitor  
metadata:  
  labels:  
    app.kubernetes.io/component: metrics  
    app.kubernetes.io/created-by: carbon-aware-keda-operator  
    app.kubernetes.io/instance: controller-manager-metrics-monitor  
    app.kubernetes.io/managed-by: kustomize  
    app.kubernetes.io/name: servicemonitor  
    app.kubernetes.io/part-of: carbon-aware-keda-operator  
    control-plane: controller-manager  
  name: carbon-aware-keda-operator-controller-manager-metrics-monitor  
  namespace: carbon-aware-keda-operator-system  
spec:  
  endpoints:  
  - bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token  
    path: /metrics  
    port: https  
    scheme: https  
    tlsConfig:  
      insecureSkipVerify: true  
  selector:  
    matchLabels:  
      control-plane: controller-manager 
EOF
```

Deploy the Prometheus + Grafana stack.

```bash
kubectl apply -f infrastructure/prometheus/manifests/

# wait for all the monitoring pods to be running
kubectl get po -n monitoring -w
```

> This deployment can take 10-15 minutes to provision.


Assign the `carbon-aware-keda-operator-metrics-reader` cluster role to the Prometheus operator. This allows the Prometheus operator to scrape from the Carbon Aware KEDA Operator's namespace.

```bash
kubectl create clusterrolebinding carbon-aware-keda-operator-prometheus-rolebinding \
  --clusterrole=carbon-aware-keda-operator-metrics-reader \
  --serviceaccount=default:prometheus-operator
```

Grafana has been deployed as a service in the cluster; however, it is only accessible via `ClusterIP`. You can `port-forward` the service to access it from your local machine or you can update the service type to `LoadBalancer` so that you can reach it from outside the cluster.

```bash
kubectl patch svc grafana -n monitoring -p '{"spec": {"type": "LoadBalancer"}}'
```

After a few minutes, Azure Load Balancer will provisioned and assigned a public IP. Browse to the website when it is fully provisioned.

```bash
echo "http://$(kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'):3000/"
```

In your web browser, navigate to the Grafana URL which was obtained in the command above and log in using the default username `admin` with default password `admin`. You will be prompted to create a new password.

Download the sample dashboard [here](https://github.com/Azure/carbon-aware-keda-operator/blob/main/hack/grafana/Carbon%20Aware%20KEDA-Dashboard.json).

Expand the **Dashboards** menu item and click the **+ Import** button.

![grafana dashboard import](../assets/images/grafana-import.png)

Upload the **Carbon Aware KEDA-Dashboard.json** file and select **prometheus** as the data source then click Import.

![grafana dashboard datasource](../assets/images/grafana-dashboard.png)

You will be able to view the default max replicas, and the max replicas ceiling being raised and lowered over time based on the carbon intensity rating.

![carbon aware dashboard](../assets/images/carbon-aware-dashboard.png)

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
