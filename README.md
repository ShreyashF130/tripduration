# 🚖 ML Trip Duration Predictor (K8s & FastAPI)

An end-to-end Machine Learning API that predicts taxi trip durations based on spatial and temporal features. The application serves predictions via a high-performance **FastAPI** backend, is fully containerized using **Docker**, and is orchestrated locally via **Kubernetes (Minikube)** for enterprise-grade scaling and auto-healing.

## 🚀 Tech Stack

* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **API Framework:** FastAPI, Uvicorn, Pydantic
* **Containerization:** Docker
* **Orchestration:** Kubernetes (Minikube, kubectl)
* **Language:** Python 3.13

## 📁 Project Structure

```text
.
├── models/
│   └── model.joblib          # Trained ML model
├── src/                      # ML pipeline and feature engineering scripts
├── app.py                    # FastAPI application and routing
├── Dockerfile                # Multi-stage Docker image build instructions
├── deployment.yaml           # Kubernetes Deployment and Service configuration
├── requirements.txt          # Python dependencies
└── README.md
