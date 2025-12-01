*(Per Luca: Come integrare le API)*


# 📘 Guida Integrazione Frontend (per Luca)

Ciao! 👋 Qui trovi i dettagli per collegare l'interfaccia al backend AI.
Il sistema funziona in *2 Step*: prima puliamo i dati, poi chiediamo la diagnosi.

## 🌐 Endpoint Base
* **Processor (Pulizia):** `http://localhost:8001`
* **AI Brain (Diagnosi):** `http://localhost:8000`

---

## ⚡ FLUSSO DI CHIAMATA (Workflow)

Per ogni richiesta (che sia testo, immagine o numeri), devi fare sempre queste due chiamate in sequenza:

### STEP 1: Preprocessing
Invia i dati grezzi al processore per anonimizzarli e formattarli.

* **URL:** `POST http://localhost:8001/process`
* **Headers:** `Content-Type: application/json`
* **Body Richiesta:**
    ```json
    {
      "data_type": "text",  // Opzioni: "text", "image", "numeric", "signal"
      "patient_id": "Mario Rossi", // Verrà anonimizzato automaticamente
      "raw_data": "...", // Il testo, o il base64 dell'immagine, o il JSON dei dati cardiaci
      "target_model": "local" // Usa "gemini" SOLO se è l'upload generico di immagini
    }
    ```

* **Risposta (da salvare):**
    Riceverai un oggetto JSON. Devi prendere tutto il contenuto del campo `payload` e usarlo nello step 2.

### STEP 2: Inferenza AI
Invia il payload pulito al cervello AI.

* **URL:** `POST http://localhost:8000/predict`
* **Body Richiesta:**
    ```json
    {
      "type": "text", // Lo stesso tipo usato nello step 1
      "data": ...     // Incolla qui il 'payload' ricevuto dallo Step 1
    }
    ```

---

## 📋 ESEMPI SPECIFICI PER OGNI TAB

### 1. Tab SINTOMI (Testo)
* **Input Utente:** Textarea.
* **Step 1 (`raw_data`):** Stringa del testo.
* **Step 2 Output:**
    ```json
    {
      "status": "success",
      "macro_category": "Cardiovascular / Pulmonary", // Categoria BERT
      "confidence": 0.92,
      "specific_diagnosis": "Angina Pectoris", // Diagnosi fine Gemini
      "xai_explanation": "Il modello ha rilevato..." // Spiegazione da mostrare all'utente
    }
    ```

### 2. Tab RADIOLOGIA (Raggi X) & DERMATOLOGIA (Pelle)
* **Input Utente:** Upload File.
* **Step 1 (`raw_data`):** Stringa dell'immagine in **Base64**.
* **Step 2 Output:**
    ```json
    {
      "status": "success",
      "primary_finding": "Pneumonia", // O 'diagnosis' per la pelle
      "xai_explanation_text": "La polmonite è...", // Spiegazione medica
      "xai_heatmap_base64": "/9j/4AAQSkZJRg..." // STRINGA BASE64 DELLA HEATMAP
    }
    ```
    👉 **Come visualizzare la Heatmap:** Inserisci la stringa nel tag img:
    `<img src="data:image/jpeg;base64,STRINGA_RICEVUTA" />`

### 3. Tab CARDIOLOGIA (Dati Numerici)
* **Input Utente:** Form con campi (Age, Cholesterol, ecc.).
* **Step 1 (`raw_data`):** Oggetto JSON con i valori grezzi:
    `{"age": 60, "sex": 1, "cp": 2, "trestbps": 140, "chol": 260, ...}`
* **Step 2 Output:**
    ```json
    {
      "risk_level": "ALTO",
      "probability_percent": 85.5,
      "key_factors": [
         "Colesterolo elevato (>240)",
         "Pressione alta"
      ] // Lista di stringhe da mostrare come bullet points
    }
    ```

### 4. Tab IMMAGINE GENERICA (Analisi Gemini)
* **Input Utente:** Upload File.
* **Step 1:** Importante! Imposta `"target_model": "gemini"`.
* **Step 2 Output:**
    ```json
    {
      "analysis": "L'immagine mostra una frattura..." // Testo libero descrittivo
    }
 
