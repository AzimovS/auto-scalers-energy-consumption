# Tea Store microservice application
We use the tea store microservice application from [Descartes Research](https://github.com/DescartesResearch/TeaStore/tree/master). The TeaStore is a distributed micro-service reference and test application featuring five distinct services plus a registry.
![Tea Store Application](resources/teastore.png)

## Steps to run the application on AKS
1.	Login to your Azure account using the command:<br/>
    ```
    az login
    ```
    ![Azure CLI Login](resources/azure_cli_login.png)
    
    It requires to add device code as well which can be done by using: <br/>
    ```
    az login –use-device-code
    ```

    ![Azure CLI Login](resources/azure_cli_login_device_code.png)

2.	Create resource group: <br/>
    ```
    az group create --name {resource_group_name} --location eastus
    ```

3.	Create cluster in resource group: <br/>
    ```
    az aks create --resource-group {resource_group_name} --name {cluster_name} --enable-managed-identity --node-count 3 --generate-ssh-keys --load-balancer-sku standard
    ```

4.	Connect to the cluster: <br/>
    ```
    az aks get-credentials --resource-group {resource_group_name} –name {cluster_name}
    ```
    ![Connect to cluster](resources/az_connect_to_cluster.png)

5. Deploy the teastore application to AKS using the instructions provided in the repo from DescartesResearch. <br/>
    ```
    kubectl create -f https://raw.githubusercontent.com/DescartesResearch/TeaStore/master/examples/kubernetes/teastore-clusterip.yaml
    ```

6. Check the status of the deployed application using: <br/>
    ```
    kubectl get all -A
    ```
    ![Check status](resources/kubectl_check_status2.png)

    Wait until all of the pods are in running status.

    ![Check status](resources/kubectl_check_status.png)

7. Use port-forwarding to access the application locally.
    After all of the pods are running, we can port-forward the web-ui to access the UI locally using the command: <br/>
    ```
    kubectl port-forward service/teastore-webui --namespace=teastore 8080:8080
    ```

8. Load testing using Locust: <br/>
    The repo for teastore application also comes with a python script to run load testing using Locust.

    ```
    cd teastore_microservice_app
    cd locust
    locust
    ```

9. Carbon intensity emission tracker using Kepler:
    We use [Kepler](https://github.com/sustainable-computing-io/kepler/tree/main) to get the carbon intensity values for the different pods running the different microservices in the tea store application.

    We deployed Kepler in AKS using deployment using manifest. We first tried deploying it using Helm which was easier but with the Helm deployment, we got empty query results from Prometheus. We then switched to deployment using manifests. Before deploying Kepler, it is important to deploy the monitoring stack using the following steps:

    ```
    git clone --depth 1 https://github.com/prometheus-operator/kube-prometheus
    cd kube-prometheus
    kubectl apply --server-side -f manifests/setup
    kubectl wait \
	--for condition=Established \
	--all CustomResourceDefinition \
	--namespace=monitoring
    kubectl apply -f manifests/
    ```

    This will run the pods required for monitoring using Prometheus and Grafana. We can then use port-forwarding to access the Prometheus Web application and Grafana dashboard locally.

    ```
    kubectl port-forward service/prometheus-k8s --namespace=monitoring 9090:9090
    ```

    ```
    kubectl port-forward service/grafana 3000:3000 --namespace=monitoring
    ```

    The Grafana dashboard login credentials values are: <br/>
    username: admin<br/>
    password: admin

    The Kepler deployment also requires the following:<br>
    *  kubectl v1.21+
    * make
    * go
    
    n we can use the following commands to deploy Kepler: 
    ```
    cd ./kepler
    make build-manifest OPTS="PROMETHEUS_DEPLOY"
    kubectl apply -f _output/generated-manifest/deployment.yaml
    ```

    We had issues with the makefile when running the above commands with the latest version of Kepler. However, we were able to run it using version: release-0.5.4.








