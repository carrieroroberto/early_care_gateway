# Early Care Gateway

![MIT License](https://img.shields.io/badge/License-MIT-3DA639?logo=opensourceinitiative&logoColor=white)
![LaTeX](https://img.shields.io/badge/Documentation-LaTeX-008080?logo=latex&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)

**Early Care Gateway** is a gateway that routes clinical data to provide medical decision support.  
The system leverages a **Explainable AI** models to filter, predict, and explain diseases and pathologies based on the medical domain.  
Special emphasis is placed on **privacy**, **traceability**, and **response times**.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Configure environment variables](#2-configure-environment-variables)
  - [3. Run the project](#3-run-the-project)
- [Optional: Verify the setup](#optional-verify-the-setup)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

---

## Prerequisites

Before running the project, make sure the following tools are installed:

- **Python 3** (for generating the secret key)
- **Docker** (for containerized deployment)
- **Docker Compose** (for orchestrating multi-container setup)
- **Git** (for cloning the repository)

Check versions:

```bash
python --version
docker --version
docker-compose --version
git --version
```

## Quickstart

**1. Clone the repository**

    git clone https://github.com/carrieroroberto/early_care_gateway.git
    cd early_care_gateway

**2. Configure environment variables**

The file .env.example is only a template of the environment configuration used by the system (not pushed on GitHub as a security best practice). You should either rename it to .env or create a new .env file with the correct values.

**Generate a secret key**

If you have Python installed locally:

    python3 backend/secret_key_generator.py

Copy the generated key into your .env file under SECRET_KEY.

**Example .env configuration**

    POSTGRES_USER=postgres_user
    POSTGRES_PASSWORD=postgres_password
    POSTGRES_DB=db_name
    POSTGRES_PORT=5432

    PGADMIN_EMAIL=pgadmin_email
    PGADMIN_PASSWORD=pgadmin_password

    SECRET_KEY=generated_secret_key_here

**3. Run the project**

Navigate to the backend directory and start the project using Docker Compose:

    cd backend
    docker-compose up --build

This will:
- Build all Docker images (backend, database, pgAdmin)
- Start all containers
- Automatically link services for proper communication

**Optional: Verify the setup**

- Monitor the logs in the terminal to ensure that all services have been initialized without errors.
- Access pgAdmin using the credentials in your .env to manage the database in a user-friendly interface.

## Troubleshooting

Ensure that no other services are running on the ports used by the system (e g., PostgreSQL: 5432, pgAdmin: 8080) to avoid conflicts.

If Docker images fail to build, stop and remove existing containers:

    docker-compose down
    docker-compose up --build

On Linux systems, Docker commands may require sudo.
