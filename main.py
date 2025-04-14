# from fastapi import FastAPI, File, UploadFile
# from services.ocr_model import process_prescription
# from services.nlp_model import analyze_symptoms

# app = FastAPI()

# @app.post("/upload")
# async def upload_prescription(file: UploadFile = File(...)):
#     medicine = process_prescription(file)
#     return {"medicine": medicine}

# @app.post("/symptoms")
# async def check_symptoms(symptoms: str):
#     specialist = analyze_symptoms(symptoms)
#     return {"specialist": specialist}
# from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import pandas as pd
import io
import re
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from pydantic import BaseModel
from bs4 import BeautifulSoup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_specialist_mapping(csv_path=r"C:\Users\asus\OneDrive\Desktop\Pharm-ate\backend\services\specialist_mapping.csv"):
    df = pd.read_csv(csv_path)
    return dict(zip(df["Symptom"].str.lower(), df["Specialist"]))

specialist_mapping = load_specialist_mapping()

# def analyze_symptoms(text):
#     words = text.lower().split()
#     print(words)
#     for word in words:
#         print(word)
#         if word in specialist_mapping:
#             print(specialist_mapping[word])
#             return specialist_mapping[word]

def analyze_symptoms(text):
    text = text.lower()
    for symptom, specialist in specialist_mapping.items():
        if symptom in text:
            return specialist
    return "General Physician"
class MedicineRequest(BaseModel):
    extracted_text: str
def get_medicine_list(limit=100):
    """Fetch medicine names from OpenFDA API"""
    url = f"https://api.fda.gov/drug/label.json?limit={limit}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        medicines = set()
        for entry in data.get("results", []):
            if "openfda" in entry and "brand_name" in entry["openfda"]:
                medicines.update([name.lower() for name in entry["openfda"]["brand_name"]])

        return list(medicines)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching medicines from OpenFDA: {e}")
        return []

def identify_medicines(extracted_text, medicine_list):
    extracted_text_lower = extracted_text.lower()
    identified_medicines = []
    print(medicine_list)
    for medicine in medicine_list:
        if re.search(r'\b' + re.escape(medicine.lower()) + r'\b', extracted_text_lower):
            identified_medicines.append(medicine)

    return identified_medicines
# @app.post("/suggest-medicines")
# async def suggest_medicines(payload: MedicineRequest):
#     try:
#         medicine_list = get_medicine_list(limit=100)
#         found_medicines = identify_medicines(payload.extracted_text, medicine_list)

#         return {
#             "identified_medicines": found_medicines
#         }

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
def get_medlineplus_info(symptom):
    url = f"https://connect.medlineplus.gov/application"
    params = {
        "mainSearchCriteria.v.c": symptom,
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.103",
        "informationRecipient.languageCode.c": "en"
    }

    try:
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if "medlineplus.gov" in a['href']]

        return links if links else ["No direct match found."]
    except Exception as e:
        return [f"Error fetching data: {str(e)}"]
@app.post("/suggest-medicines")
async def symptom_to_topic(payload: MedicineRequest):
    links = get_medlineplus_info(payload.extracted_text)
    return {"related_links": links}

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        extracted_text = pytesseract.image_to_string(img)
        specialist = analyze_symptoms(extracted_text)
        return {
            "extracted_text": extracted_text.strip(),
            "recommended_specialist": specialist
        }
    except Exception as e:
        return {"error": str(e)}
