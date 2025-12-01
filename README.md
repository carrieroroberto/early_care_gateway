# Medical AI Hub - Backend System

Questo repository contiene il backend a microservizi per la piattaforma di diagnostica medica AI multimodale. Il sistema supporta analisi di: Testo (Sintomi), Immagini (Raggi X, Dermatoscopia), Dati Tabulari (Rischio Cardiaco) e Segnali (ECG).

# Architettura del Sistema

Il backend è composto da due microservizi Dockerizzati:

*   Data Processor (Porta 8001): Si occupa delle operazioni di pre-processing sui dati in ingresso: Anonimizzazione (GDPR Compliance), Pulizia del testo, Normalizzazione delle immagini, Encoding dei dati numerici, Validazione dei segnali.

*   AI Brain Service (Porta 8000): Contiene i modelli di Deep Learning e l'integrazione per la Explainable AI (XAI): Modelli di Deep Learning (DenseNet, EfficientNet, BERT), Integrazione con Google Gemini per l'Explainable AI (XAI) e l'analisi di immagini generiche.

# Guida all'Installazione e Avvio Rapido

Segui questi passaggi per configurare e avviare il backend sul tuo ambiente di sviluppo.

# 1. Prerequisiti

Assicurati di avere installati e attivi i seguenti strumenti:

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/): Necessario per la gestione dei container Docker.
*   Git: Per clonare il repository.

# 2. Scarica i Modelli di AI (Obbligatorio)

I modelli addestrati sono di grandi dimensioni e non sono inclusi nel repository GitHub. Devi scaricarli manualmente da questo link condiviso: [Modelli AI - One Drive](https://politecnicobari-my.sharepoint.com/:f:/g/personal/l_serio3_studenti_poliba_it/IgDpzrk4U20OTo_HqWFyfv3sAQIHqhYrJQwPMBfHnMQ9tuA?e=jr0YZc). Dopo aver scaricato, estrai i contenuti e posiziona la cartella `models/` nella directory principale (root) del progetto. La struttura finale della cartella `models/` deve essere esattamente come segue:

    models/
    ├── densenet_epoch_3.pth           (Modello per Analisi Raggi X)
    ├── efficientnet_skin_best.pth     (Modello per Analisi Dermatologica)
    ├── xgboost_heart_model.joblib     (Modello per Analisi Rischio Cardiaco)
    └── modello_medico_finale/         (Cartella scompattata del Modello BERT per testo)
        ├── config.json
        ├── pytorch_model.bin
        └── ...

# 3. Configurazione della Chiave API di Google Gemini

Crea un file chiamato `.env` nella directory principale del progetto (la stessa dove si trova questo README.md). In questo file, inserisci la tua chiave API per Google Gemini nel seguente formato:

    GOOGLE_API_KEY=la_tua_chiave_segreta_di_gemini

Sostituisci `la_tua_chiave_segreta_di_gemini` con la tua vera chiave API.

# 4. Avvio del Sistema

Apri il terminale nella directory principale del progetto e esegui il seguente comando:

    docker-compose up --build

Questo comando costruirà le immagini Docker (se necessario) e avvierà entrambi i microservizi. Attendi che i log nel terminale indichino il completamento dell'avvio di entrambi i servizi.

*   Data Processor: Sarà accessibile su `http://localhost:8001`
*   AI Brain Service: Sarà accessibile su `http://localhost:8000`

# Testare il Funzionamento (Opzionale)

Per una verifica rapida che tutti i servizi siano attivi e configurati correttamente, puoi utilizzare lo script di test fornito. Assicurati di avere Python installato localmente.

    python test_system.py

# Tecnologie Utilizzate

*   Framework Web: FastAPI, Uvicorn
*   Intelligenza Artificiale / Machine Learning: PyTorch, Transformers (HuggingFace), XGBoost, Scikit-learn
*   Explainable AI (XAI): Grad-CAM, SHAP Logic, Google Gemini 2.0 Flash
*   Containerizzazione: Docker & Docker Compose
