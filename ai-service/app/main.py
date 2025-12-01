import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any

# Importiamo le strategie
from app.strategies.text import text_analyzer
from app.strategies.image import image_analyzer
from app.strategies.numeric import numeric_analyzer
from app.strategies.signal import signal_analyzer

app = FastAPI(title="Medical AI Hub")


class RequestPayload(BaseModel):
    type: str  # "text", "xray", "skin", "heart", "ecg", "generic"
    data: Any  # Il contenuto vero e proprio


@app.post("/predict")
async def predict(payload: RequestPayload):
    mode = payload.type.lower()

    if mode == "text":
        return text_analyzer.analyze(payload.data)

    elif mode in ["xray", "skin", "generic"]:
        # Passiamo il tipo specifico alla strategia immagini
        return image_analyzer.analyze(mode, payload.data)

    elif mode == "heart":
        return numeric_analyzer.analyze(payload.data)

    elif mode == "ecg":
        return signal_analyzer.analyze(payload.data)

    else:
        raise HTTPException(400, f"Tipo '{mode}' non supportato.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)