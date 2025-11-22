# Early Care Gateway
Gateway that routes clinical data to provide medical decision support. Triage AI filters, predicts, and explains diseases and pathologies based on domain. Emphasis on privacy, traceability, and response times.

# Quickstart

## 1. Clone the repository
```markdown
```console
git clone https://github.com/carrieroroberto/early_care_gateway.git
```

## 2. Rename .env.example in .env and fill with your data
```markdown
```console
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=db_name
POSTGRES_PORT=5432

PGADMIN_EMAIL=pgadmin_email
PGADMIN_PASSWORD=pgadmin_password

SECRET_KEY=secret_key
```

## 3. Run the project
```markdown
```console
cd early_care_gateway/backend
docker-compose up --build
```