import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import spacy
csv_path = r"C:\Users\asus\OneDrive\Desktop\Pharm-ate\backend\services\symptoms_specialists.csv"
specialist_df = pd.read_csv(csv_path)
model_path = r"C:\Users\asus\OneDrive\Desktop\Pharm-ate\backend\services\clinicalbert_model\clinicalbert_model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

nlp = spacy.load(r"C:\Users\asus\OneDrive\Desktop\Pharm-ate\backend\services\spacy_ner_model\spacy_ner_model")
specialists = specialist_df['Specialist'].unique()
id2specialist = {i: s for i, s in enumerate(specialists)}

def predict_specialist_and_treatment(text):
    print("in prediction model")
    doc = nlp(text)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "SYMPTOM"]
    if not symptoms:
        symptoms = [text]  

    symptoms_text = ", ".join(symptoms)

    print(symptoms)
    inputs = tokenizer(symptoms_text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    with torch.no_grad():
        output = model(**inputs)
    
    with torch.no_grad():
       output = model(**inputs)
       predicted_index = output.logits.argmax(dim=1).item()

    predicted_specialist = id2specialist[predicted_index]
    print("Predicted specialist:", predicted_specialist)
    matched_specialist = None
    matched_treatment = None

    for _, row in specialist_df.iterrows():
        csv_symptoms = [s.strip().lower() for s in row["Symptoms"].split(",")]
        for symptom in symptoms:
            if symptom in csv_symptoms:
                matched_specialist = row["Specialist"]
                matched_treatment = row["Treatments"]
                break
        if matched_specialist:
            break

    if matched_specialist:
        validated_specialist = matched_specialist
        suggested_treatment = matched_treatment
    else:
        validated_specialist = predicted_specialist
        fallback_rows = specialist_df[specialist_df["Specialist"] == predicted_specialist]
        suggested_treatment = fallback_rows["Treatments"].iloc[0] if not fallback_rows.empty else "No treatment found"
    if len(validated_specialist) < 7:
        validated_specialist = "General Physician"

    print(validated_specialist)
    print(suggested_treatment)
    return validated_specialist, suggested_treatment      