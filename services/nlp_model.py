import pandas as pd
from transformers import pipeline

def load_specialist_mapping(csv_path=r"C:\Users\asus\OneDrive\Desktop\Pharm-ate\backend\services\specialist_mapping.csv"):
    df = pd.read_csv(csv_path)
    return dict(zip(df["Symptom"].str.lower(), df["Specialist"]))
specialist_mapping = load_specialist_mapping()

nlp_model = pipeline("fill-mask", model="bert-base-uncased", device=-1)

def analyze_symptoms(symptoms):
    return specialist_mapping.get(symptoms.lower(), "General Physician")
if __name__ == "__main__":
    symptom = input("Enter your symptom: ")
    specialist = analyze_symptoms(symptom)
    print(f"Recommended Specialist: {specialist}")
