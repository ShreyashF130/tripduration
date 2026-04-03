# 🚖 Taxi Trip Duration Predictor (Enterprise MLOps & Service Mesh)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Seldon Core](https://img.shields.io/badge/Seldon_Core-1.15-8A2BE2.svg)](https://www.seldon.io/)
[![Istio](https://img.shields.io/badge/Istio-Service_Mesh-466BB0.svg)](https://istio.io/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C.svg)](https://prometheus.io/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5.svg?logo=kubernetes)](https://kubernetes.io/)

An end-to-end, production-ready Machine Learning serving platform. Upgraded from a standalone REST API, this service now leverages **Seldon Core** for model orchestration and **Istio** for advanced service mesh networking. It supports complex deployment strategies like Canary/A-B-C testing, auto-scaling, and real-time observability via **Prometheus**.

---

## 🏗️ Architecture & Design

* **The Model Wrapper:** A Seldon-compatible Python class (`TripDurationModel.py`) handles model initialization and inference, stripping away boilerplate API code.
* **The Orchestrator:** **Seldon Core** automatically translates the Python wrapper into a high-performance REST/gRPC microservice.
* **The Service Mesh:** **Istio** manages all ingress and intra-cluster network traffic. An `Istio Gateway` exposes the front door, while a `VirtualService` handles advanced mathematical traffic splitting.
* **Observability:** An Envoy sidecar proxy is injected into every pod, automatically tracking request metrics and feeding them to **Prometheus** for real-time visualization.

---

## 📁 File Structure

This project adopts an industry-standard MLOps repository structure, separating ML code from Kubernetes infrastructure manifests.

```text
.
├── models/                   # Serialized Machine Learning models (.joblib)
├── src/                      # Source code for training and feature engineering
├── TripDurationModel.py      # Seldon Core Python wrapper class (replaces app.py)
├── Dockerfile                # Seldon-specific container build instructions
├── requirements.txt          # Python dependencies (seldon-core, scikit-learn, etc.)
├── k8s/                      # Kubernetes Infrastructure Manifests
│   ├── seldon-gateway.yaml   # Istio Ingress configuration (Unlocking port 80)
│   ├── routing.yaml          # Istio VirtualService (Traffic routing/splitting)
│   └── seldon_deployment.yaml# The Seldon ML blueprint
└── README.md                 # Project documentation



⚙️ Prerequisites
Ensure you have the following installed and configured on your machine:

Docker Desktop (Running)

Minikube & kubectl

istioctl (Istio CLI installed and added to PATH)

Note: This guide assumes your Minikube cluster is already running, the Seldon Operator is installed in the seldon-system namespace, and Istio is configured. Ensure your default namespace has Istio injection enabled:
kubectl label namespace default istio-injection=enabled

🚀 Deployment Guide
Step 1: Build the Container Image
To ensure Kubernetes has access to the image without needing a remote registry, build the image directly inside Minikube's internal Docker daemon:

Bash
# 1. Point your terminal to Minikube's Docker environment (Windows PowerShell)
& minikube -p minikube docker-env | Invoke-Expression

# 2. Build the Seldon image
docker build -t tripduration-seldon:v1 .
Step 2: Configure the Network (Istio)
Open the front door and map the routing rules for the API:

Bash
# 1. Apply the Gateway to allow traffic into the cluster
kubectl apply -f k8s/seldon-gateway.yaml

# 2. Apply the VirtualService to handle routing (and A/B traffic splits)
kubectl apply -f k8s/routing.yaml
Step 3: Deploy the Machine Learning Model
Apply the Seldon blueprint to spin up the ML pods and attach the Istio sidecars:

Bash
kubectl apply -f k8s/seldon_deployment.yaml
Verify the pods are running with 2/2 status (Model Container + Envoy Proxy):

Bash
kubectl get pods -w
💻 How to Use the API
Because we are utilizing a Service Mesh, traffic must enter through the Istio Ingress Gateway.

1. Open the Tunnel
Run this command to establish a tunnel from your localhost to the Istio Gateway, and leave this terminal window running:

Bash
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
2. Make a Prediction
Open a new terminal window. Seldon expects a specific JSON tensor format {"data": {"ndarray": [...]}}. Run the following command to test the endpoint:

Bash
Invoke-RestMethod -Uri "http://localhost:8080/seldon/default/tripduration/api/v1.0/predictions" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"data": {"ndarray": [[1.0, 2.0, -73.987, 40.738, -73.967, 40.763, 0.0, 2.5, 3.1, 45.0]]}}'
📊 Observability & Monitoring
This platform includes out-of-the-box metric scraping via Prometheus, tracking every request intercepted by the Istio Envoy proxies.

1. Generate Load (Optional):
Run a continuous loop to generate API traffic for the dashboard:

Bash
while($true) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8080/seldon/default/tripduration/api/v1.0/predictions" -Method Post -ContentType "application/json" -Body '{"data": {"ndarray": [[1.0, 2.0, -73.987, 40.738, -73.967, 40.763, 0.0, 2.5, 3.1, 45.0]]}}' | Out-Null
        Write-Host "." -NoNewline
    } catch { Write-Host "X" -NoNewline }
    Start-Sleep -Milliseconds 100
}
2. Open Prometheus:

Bash
istioctl dashboard prometheus
3. Analyze Traffic:
In the Prometheus web UI, use the following PromQL query to visualize request rates and traffic distribution in real-time:

Plaintext
sum(rate(istio_requests_total{destination_workload=~".*tripduration.*"}[1m])) by (destination_workload)
🧹 Cleanup
To safely teardown the local environment:

Bash
# Delete the network and model routing
kubectl delete -f k8s/routing.yaml
kubectl delete -f k8s/seldon-gateway.yaml

# Delete the ML deployment
kubectl delete -f k8s/seldon_deployment.yaml
