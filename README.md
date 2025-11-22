# Early Care Gateway
Gateway that routes clinical data to provide medical decision support. Triage AI filters, predicts, and explains diseases and pathologies based on domain. Emphasis on privacy, traceability, and response times.

# Quickstart

## 1. Clone the repository
```bash
git clone https://github.com/carrieroroberto/early_care_gateway.git
```

## 2. Rename .env.example in .env and fill with your data
You can use *secret_key_generator.py* to generate the secret key.
```bash
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=db_name
POSTGRES_PORT=5432

PGADMIN_EMAIL=pgadmin_email
PGADMIN_PASSWORD=pgadmin_password

SECRET_KEY=secret_key
```

## 3. Run the project
```bash
cd early_care_gateway/backend
docker-compose up --build
```
