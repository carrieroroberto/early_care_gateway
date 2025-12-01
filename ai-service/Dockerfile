FROM python:3.9-slim

# Installa librerie di sistema per XGBoost e PyTorch
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installa Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice della cartella app dentro il container
COPY app ./app

# Avvia il server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]