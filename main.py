from fastapi import FastAPI, File, UploadFile
from services.ocr_model import process_prescription
from services.nlp_model import analyze_symptoms

app = FastAPI()

@app.post("/upload")
async def upload_prescription(file: UploadFile = File(...)):
    medicine = process_prescription(file)
    return {"medicine": medicine}

@app.post("/symptoms")
async def check_symptoms(symptoms: str):
    specialist = analyze_symptoms(symptoms)
    return {"specialist": specialist}
