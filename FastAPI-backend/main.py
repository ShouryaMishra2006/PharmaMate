from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import pandas as pd
import io
import re
import cv2
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from pydantic import BaseModel
from bs4 import BeautifulSoup
from services.hybrid_model_loader import predict_specialist_and_treatment
import requests
from dotenv import load_dotenv
import os
import concurrent.futures
class UMLSClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth_endpoint = "https://utslogin.nlm.nih.gov/cas/v1/api-key"
        self.base_url = "https://uts-ws.nlm.nih.gov"
        self.version = "current"
        self.tgt = self.get_tgt()

    def get_tgt(self):
        params = {'apikey': self.api_key}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.auth_endpoint, data=params, headers=headers)
        if response.status_code == 201:
            tgt = response.headers['location']
            return tgt
        else:
            raise Exception("Failed to obtain TGT")

    def get_service_ticket(self):
        params = {'service': 'http://umlsks.nlm.nih.gov'}
        response = requests.post(self.tgt, data=params)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Failed to obtain service ticket")

    def search_term(self, term):
        ticket = self.get_service_ticket()
        search_url = f"{self.base_url}/rest/search/{self.version}"
        params = {'string': term, 'ticket': ticket}
        response = requests.get(search_url, params=params)
        results = response.json()
        return results['result']['results']

    def get_related_concepts(self, cui):
        ticket = self.get_service_ticket()
        relations_url = f"{self.base_url}/rest/content/{self.version}/CUI/{cui}/relations"
        params = {'ticket': ticket}
        response = requests.get(relations_url, params=params)
        results = response.json()
        return results['result']

def map_symptom_to_conditions(symptom, umls_client, max_conditions=5):
    search_results = umls_client.search_term(symptom)
    print("Search results:", search_results)
    conditions = set()

    relevant_keywords = set(symptom.lower().split())

    for result in search_results:
        cui = result['ui']
        if cui != 'NONE':
            related_concepts = umls_client.get_related_concepts(cui)
            for concept in related_concepts:
                if concept.get('relationLabel') == 'RO' or 'RQ' in concept.get('additionalRelationLabel', ''):
                    related_condition = concept['relatedIdName']
                    print(f"Related Condition: {related_condition}")


                    condition_keywords = set(related_condition.lower().split())
                    if relevant_keywords & condition_keywords: 
                        conditions.add(related_condition)

                if len(conditions) >= max_conditions:
                    break
            if len(conditions) >= max_conditions:
                break

    return list(conditions)
def get_drugs_for_condition(condition):
    base_url = "https://api.fda.gov/drug/label.json"
    params = {
        'search': f'indications_and_usage:"{condition}"',
        'limit': 5
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        drugs = []
        for result in data.get('results', []):
            openfda = result.get('openfda', {})
            brand_names = openfda.get('brand_name', [])
            generic_names = openfda.get('generic_name', [])
            drugs.extend(brand_names + generic_names)
        return list(set(drugs))
    return []


def multi_agent_symptom_to_drugs(symptom, umls_api_key):
    umls_client = UMLSClient(umls_api_key)
    conditions = map_symptom_to_conditions(symptom, umls_client)
    all_drugs = set()
    for condition in conditions:
        drugs = get_drugs_for_condition(condition)
        all_drugs.update(drugs)
        print("drugs:",drugs)
    final = {
        'symptom': symptom,
        'conditions': conditions,
        'recommended_drugs': list(all_drugs)
    }
    print(final)
    return {
        'symptom': symptom,
        'conditions': conditions,
        'recommended_drugs': list(all_drugs)
    }
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)




def analyze_symptoms(text):
    text = text.lower()

    specialist, treatment = predict_specialist_and_treatment(text)

    print(specialist)
    print(treatment)
    return {"extracted_text":text,"specialist": specialist, "treatment": treatment}
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




@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()

        print(contents)
        img = Image.open(io.BytesIO(contents)).convert('RGB') 
        print(img)
        img_np = np.array(img)
        print(img_np)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)  
        print(gray)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        print(thresh)
        extracted_text = pytesseract.image_to_string(thresh)
        print(extracted_text)
        response = analyze_symptoms(extracted_text)
        medicine_list = get_medicine_list(limit=100)
        matched_medicines = identify_medicines(extracted_text, medicine_list)
        print(matched_medicines)
        print(response)
        
        return response
        
    except Exception as e:
        return {"error": str(e)}
@app.post("/suggest-medicines")
async def get_drugs(payload: MedicineRequest):
    umls_api_key = os.getenv("UMLS_API_KEY")
    result = multi_agent_symptom_to_drugs(payload.extracted_text, umls_api_key)
    return result

