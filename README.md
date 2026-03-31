# 🚖 Taxi Trip Duration Predictor (MLOps & Kubernetes)

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.2-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5.svg?logo=kubernetes)](https://kubernetes.io/)

An end-to-end Machine Learning prediction API designed for cloud-native deployment. This service takes spatial and temporal features of a taxi ride and predicts the total trip duration. It is served via a high-performance **FastAPI** backend, fully containerized, and orchestrated using **Kubernetes** for auto-healing and scalability.

---

## 🏗️ Architecture & Design

* **The Model:** A pre-trained Machine Learning model (`model.joblib`) handles the core predictions, utilizing engineered features like Haversine distance and Manhattan dummy distances.
* **The API:** FastAPI wraps the model, providing automatic data validation via Pydantic and auto-generated Swagger UI documentation.
* **The Infrastructure:** The application is packaged into a multi-stage Docker image and deployed to a local Kubernetes cluster (Minikube). 
* **Traffic Flow:** User Request ➡️ Minikube Tunnel ➡️ Kubernetes ClusterIP Service ➡️ Load Balanced Pods ➡️ FastAPI Application.

---

## 📁 File Structure (Cookiecutter Standard)

This project strictly adheres to the industry-standard **Cookiecutter Data Science** logical structure to ensure reproducibility, clean code separation, and team scalability.

```text
.
├── models/                   # The serialized Machine Learning models (.joblib)
├── src/                      # Source code for feature engineering and data processing
├── app.py                    # Main FastAPI application and routing logic
├── Dockerfile                # Instructions for building the container image
├── deployment.yaml           # K8s manifests (Deployment & Service configurations)
├── requirements.txt          # Python library dependencies
├── .gitignore                # Git exclusion rules
└── README.md                 # Project documentation




⚙️ Prerequisites
Before you begin, ensure you have the following installed on your machine:

Git

Docker Desktop (Running)

Minikube

kubectl

🚀 Installation & Deployment Guide
Step 1: Clone the Repository
Download the project to your local machine:

Bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
(Note: Replace the URL above with your actual GitHub repository URL).

Step 2: Start the Kubernetes Cluster
Boot up your local Minikube environment:

Bash
minikube start
Step 3: Build the Container Image
To ensure Kubernetes has access to the image without needing a remote registry (like Docker Hub), we build the image directly inside Minikube's internal Docker daemon:

Bash
# 1. Point your terminal to Minikube's Docker environment
minikube docker-env | Invoke-Expression   # Use 'eval $(minikube docker-env)' on Mac/Linux

# 2. Build the image (tagged as v2)
docker build -t tripduration:v2 .
Step 4: Deploy the Application
Apply the Kubernetes manifests to create the Pods and the ClusterIP Service:

Bash
kubectl apply -f deployment.yaml
Verify that your pods are successfully running:

Bash
kubectl get pods -w
(Wait until the status shows 1/1 Running before proceeding).

💻 How to Use the API
Because the API is running safely isolated inside the Kubernetes cluster, we need to open a secure tunnel to access it from our local browser.

1. Open the Minikube Tunnel
Run this command to expose the service:

Bash
minikube service tripduration
This command will output a local URL (e.g., http://127.0.0.1:59957) and automatically open it in your default web browser.

2. Access the Interactive UI
In your browser, append /docs to the end of the URL provided by Minikube to access the interactive Swagger UI:
👉 http://127.0.0.1:<PORT>/docs

3. Make a Prediction
Click on the green POST /predict route.

Click the "Try it out" button.

Paste the following sample JSON into the Request Body:

JSON
{
  "vendor_id": 1.0,
  "passenger_count": 2.0,
  "pickup_longitude": -73.987,
  "pickup_latitude": 40.738,
  "dropoff_longitude": -73.967,
  "dropoff_latitude": 40.763,
  "store_and_fwd_flag": 0.0,
  "distance_haversine": 2.5,
  "distance_dummy_manhattan": 3.1,
  "direction": 45.0
}
Click "Execute".

Scroll down to see the Server Response, which will return the predicted trip duration in seconds!

🧹 Cleanup
When you are done testing, you can spin down the resources to save memory on your machine:

Bash
# Delete the Kubernetes resources
kubectl delete -f deployment.yaml

# Stop the Minikube cluster
minikube stop
