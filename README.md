# Early Care Gateway

![MIT License](https://img.shields.io/badge/License-MIT-3DA639?logo=opensourceinitiative&logoColor=white)
![LaTeX](https://img.shields.io/badge/Documentation-LaTeX-008080?logo=latex&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

A Microservice Architecture for Clinical Decision Support with Explainable AI.

EarlyCare Gateway is a web system designed to optimize triage and preliminary diagnosis workflows. Built on a microservices architecture, the system analyzes multimodal data (text, images, signals, and structured records) providing predictions supported by Explainable AI (XAI) insights.

*Note: This system is designed exclusively for professional use by authorized medical personnel to prevent risks associated with self-diagnosis.*

---

## Table of Contents
- [System Overview](#systemoverview)
- [Getting Started](#gettingstarted)

---
## System Overview

<div align="center">
  <img width="650" alt="architecture" src="https://github.com/user-attachments/assets/090e92bb-fedb-4a7a-9c0d-a5096e4681ce" />
</div>

### Key Features
- **Microservices Architecture:** A modular and scalable system comprising independent services for Authentication, Data Processing, AI, Audit, and Gateway, all orchestrated via Docker Compose.
- **Multimodal AI Analysis:**
    - **Text:** Clinical note classification using ClinicalBERT (fine-tuned) and clinical reasoning via LLM (Gemini 2.5 Flash).
    - **Imaging:** Chest X-Ray analysis with CheXNet (DenseNet) and skin lesion diagnosis with EfficientNet.
    - **Structured Data:** Cardiovascular risk assessment using XGBoost.
    - **Signals (ECG):** Anomaly detection via LLM analysis.
- **Explainable AI (XAI):** The system explains every diagnosis using SHAP (feature importance), Grad-CAM (visual heatmaps), and Chain of Thought (natural language reasoning).
- **Security & Privacy:** Implements JWT authentication, password hashing, and patient data anonymization (hashing identifiers before processing).
- **Audit Trail:** Asynchronous and immutable logging of all operations to ensure full clinical traceability.

### Performance Highlights
The system has been validated on public datasets (*MIMIC-III, ChestX-ray, HAM10000, UCI Heart Disease*) with promising results:
- **Chest X-Ray:** Mean AUC 0.837.
- **Skin Lesions:** Accuracy 88% (Melanoma Recall 73%).
- **Textual Analysis:** Accuracy 88%.
- **Cardiac Risk:** Accuracy 82.1%.

### Tech Stack
- **Backend:** Python, FastAPI.
- **AI & Data Science:** PyTorch, Hugging Face Transformers, Scikit-Learn, XGBoost, Pandas, Google Gemini API.
- **Database:** PostgreSQL (with Repository Pattern).
- **Containerization & Deployment:** Docker, Docker Compose.
- **Testing:** Pytest

## Getting Started

### Prerequisites

Prior to running the project, ensure that your system meets the following software and hardware requirements:

- **Python 3:** Generate the JWT secret key
- **Pip:** Install testing dependencies
- **Docker (and WSL for Windows):** Build containers
- **Docker Compose V2:** Deploy the multi-container system
- **Git:** Clone the repository
- **At least 2 GB of Disk Space:** Host AI models and system components
- **Recommended at least 8 GB RAM:** Ensure stable execution

Check versions:

```bash
git -- version
python -- version
pip -- version
wsl -- version # Windows only
docker -- version
docker compose version
```

### Quickstart

**1. Clone the repository**

    git clone https://github.com/carrieroroberto/early_care_gateway
    cd early_care_gateway

**2. Configure environment variables**

The file *.env.example* serves as a template for the environment configuration required by the system. Rename it to *.env*, or create a new *.env* file and fill it with the correct values for your setup (e.g. database user and password).

**Generate keys**

If Python is installed on your machine, you can generate a secure SHA256 secret key using:

    python secret_key_generator.py

Copy the generated key and paste it into your *.env* file under *SECRET KEY*. If you already have a Gemini API key, place it under *GOOGLE API KEY*. Otherwise, you can obtain a free API key by visiting [Google AI Studio](https://aistudio.google.com/app/api-keys). After logging in and creating a project, you will be able to generate your personal API key.

**Example .env configuration**

    POSTGRES_HOST = postgres
    POSTGRES_USER = earlycaregateway
    POSTGRES_PASSWORD = your_password
    POSTGRES_DB = earlycaregateway
    POSTGRES_PORT = 5432
    
    PGADMIN_EMAIL = admin@earlycaregateway.com
    PGADMIN_PASSWORD = your_password
    
    SECRET_KEY = your_secret_key
    GOOGLE_API_KEY = your_key
    
    GATEWAY_URL = http://gateway:8000/gateway
    AUTHENTICATION_URL = http://auth_service:8000/authentication
    DATA_PROCESSING_URL = http://data_service:8000/data_processing
    EXPLAINABLE_AI_URL = http://xai_service:8000/explainable_ai
    AUDIT_URL = http://audit_service:8000/audit

**3. Run the system**

You can start the system using the *run.bat* (Windows) or *run.sh* (macOS/Linux) scripts, that automatically launch the services and run automated tests. Alternatively, you may manually start the system with:

    docker-compose up --build

This will:
- Build all Docker images (Backend, Database, Frontend)
- Start all containers
- Link services for communication

**4. Use the system**

Access the web application at: *http://localhost:3000*.
You may also use an API client, such as Postman, to interact directly with the API endpoints following the provided documentation.

### Troubleshooting

- Monitor logs to verify that all services start correctly:

      docker compose logs -f
  
- Ensure no other applications are using ports required by the system.
- If Docker images fail to build, try stopping and removing existing containers and volumes using:

      docker compose down -v
  
- On Linux systems, Docker commands may require sudo.
- Access pgAdmin at *http://localhost:8080* using the credentials provided in your *.env* file.
