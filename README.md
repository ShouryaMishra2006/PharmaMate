# PharmaMate: AI-powered Clinical Decision Support System

[PharmaMate Demo](https://drive.google.com/file/d/1i1xEozqa_eRYYbxugDlReMW0rJEj1qZe/view?usp=drive_link)


## Overview

PharmaMate is an AI-powered clinical decision support system designed to assist healthcare professionals in making informed decisions based on clinical data. The system combines advanced machine learning and Natural Language Processing (NLP) techniques, including Optical Character Recognition (OCR), hybrid models like SpaCy and ClinicalBERT, and integration with external medical APIs to provide accurate predictions for conditions, treatments, specialists, and drugs. 

## Key Features

### 1. **Hybrid Approach for Named Entity Recognition (NER)**:
   PharmaMate employs a **hybrid approach** for Named Entity Recognition (NER) by combining **SpaCy** and **ClinicalBERT** models. This approach ensures:
   - **SpaCy** is used for traditional NER tasks, such as identifying and classifying key medical entities like conditions, treatments, and specialists in clinical text.
   - **ClinicalBERT**, a BERT-based model fine-tuned on clinical data, enhances the model’s ability to accurately capture medical entities, especially in clinical contexts where complex jargon is used. The accuracy of this hybrid approach exceeds **90%**, ensuring high reliability in recognizing medical terms and relationships.

### 2. **Custom Dataset Creation Using Google SpanBERT**:
   Using **Google SpanBERT**, a transformer model designed for span-based tasks, specialists are added to the dataset to enrich the system's understanding of medical contexts. The dataset is processed to include:
   - **Conditions** (e.g., diseases or medical conditions)
   - **Treatments** (e.g., medication or therapy)
   - **Specialists** (e.g., doctors or medical professionals)
   
   The use of **Google SpanBERT** ensures that the system can accurately map symptoms to relevant specialists, improving the precision of specialist suggestions.

### 3. **Optical Character Recognition (OCR)**:
   The system includes an **OCR process** to extract text from medical images such as prescriptions or doctor notes. Using **Tesseract OCR**, the system converts medical images into text for further analysis. This allows users to upload images of medical documents, and the system will automatically extract relevant text for analysis.

   Key steps in the OCR process:
   - The **FastAPI backend** accepts image files through an API endpoint (`/upload`).
   - **Tesseract OCR** is used to extract text from the image.
   - The extracted text is analyzed for medical information such as symptoms, conditions, and treatments.
   - The system also identifies drugs mentioned in the extracted text by comparing it with a pre-existing list of medications.
     
Optimization:
Grayscale + Thresholding improves accuracy for handwritten prescriptions, allowing for cleaner text extraction even from poor-quality scans.

### 4. **ClinicalBERT for Specialist and Treatment Prediction**:
   After extracting text (either through OCR or user input), **ClinicalBERT** is used to predict the relevant **specialists** and **treatments** based on the medical text. **ClinicalBERT**'s specialized understanding of clinical language ensures accurate prediction, significantly improving clinical decision support.

### 5. **Mapping Symptoms to Possible Conditions**:
   Symptoms provided by the user (either through text or OCR-extracted content) are mapped to possible **medical conditions** using the **UMLS (Unified Medical Language System)**. The system fetches related conditions using the **UMLS API**, identifying the most probable conditions based on the symptoms.

### 6. **Drug Suggestions Based on Conditions**:
   Once conditions are identified, the system queries the **FDA API** to suggest relevant drugs. It retrieves both **brand** and **generic** drug names associated with the conditions, helping healthcare professionals identify potential treatments quickly.

### 7. **Multi-agent System for Condition to Drug Mapping**:
   The system employs a **multi-agent approach** to map symptoms to drugs. It combines information from the **UMLS** to fetch conditions and the **FDA** to suggest drugs. This approach allows for better and more comprehensive decision-making in clinical contexts.

## Workflow Overview

1. **OCR Process**:  
   The user uploads an image (e.g., a prescription or medical document). The image is processed using **Tesseract OCR** to extract the text, which is then passed through the system for further analysis.

2. **Create Custom Dataset Using Google SpanBERT**:  
   A custom dataset is created using **Google SpanBERT** to enrich the data with specialist information, enhancing the model’s ability to predict relevant specialists based on the input text.

3. **Hybrid NER Model**:  
   The system uses a hybrid NER model (combining **SpaCy** and **ClinicalBERT**) to identify key medical entities like conditions, treatments, and specialists. The system has an accuracy rate of more than **90%** for extracting medical entities.

4. **Specialist and Treatment Prediction with ClinicalBERT**:  
   Using **ClinicalBERT**, the system predicts specialists and treatments from the extracted medical text, providing actionable insights for healthcare professionals.

5. **Condition Mapping**:  
   Symptoms or extracted text are used to map potential conditions using the **UMLS API**.
   Concept Mapping:
   The system uses the UMLS (Unified Medical Language System) API to:

   Search and map symptoms to related CUIs (Concept Unique Identifiers).

   Fetch related medical conditions via relations like "RO" (related other) or "RQ" (related qualifier).

7. **Drug Suggestions**:  
   The system suggests drugs associated with the identified conditions, using data from the **FDA API**.
   The extracted text is scanned against a dynamically fetched list of drug names using the OpenFDA API, matching only exact names using regex for precision

## Project Setup

1. Clone the repository and install the necessary dependencies:
   
   git clone https://github.com/ShouryaMishra2006/PharmaMate.git
   
   pip install -r requirements.txt
3. Set up the environment, including API keys for UMLS and other third-party services.
4. Install the required models for SpaCy, ClinicalBERT, and any other dependencies (e.g., Tesseract OCR).
5. Run the FastAPI server and use the provided endpoints to upload medical images or input text.
   
   cd Frontend
   
   npm run dev
   
   cd node-backend
   
   nodemon index.js
   
   cd FastAPI-backend
   
   python -m uvicorn main:app --reload

## API Endpoints

- **POST /upload**:  
   Upload an image for OCR processing. The system extracts text from the image and returns predictions for specialists and treatments.
  
- **POST /suggest-medicines**:  
   Provide text (either extracted from an image or entered by the user), and the system returns a list of possible conditions and suggested drugs.

## Acknowledgments

- **Hugging Face** for their Transformers library, which was used to fine-tune **ClinicalBERT** and build the custom dataset.
- **SpaCy** for its powerful Named Entity Recognition (NER) capabilities.
- **Google SpanBERT** for enhancing the dataset by adding specialists to the system.
- **Tesseract OCR** for extracting text from medical images.
- **UMLS** for providing a medical ontology that helps map symptoms to conditions.
- **FDA API** for providing drug-related data to recommend medications.
- **FastAPI** for creating a fast and efficient web service.

---

## 🔮 Future Scope and Improvements

⚙️ These features are currently under active development to further enhance PharmaMate's performance, scalability, and intelligence.

1. Optimized Symptom-to-Condition Matching via ChromaDB
   
Fetched conditions from the UMLS API will be stored in ChromaDB, a powerful vector store.

This enables semantic similarity search, allowing the system to match user-provided symptoms with medically relevant conditions more effectively and quickly.

Improves accuracy in identifying overlapping or less common clinical presentations.

2. Thread-based Optimization for Parallel Tasks

Key components like condition mapping, treatment prediction, and drug suggestion will be optimized using Python’s threading capabilities.

This allows for parallel execution, significantly reducing processing time and enhancing user experience during peak loads.

3. Scalable Architecture with Redis
   
To efficiently manage multiple simultaneous uploads or API requests, Redis will be integrated for:

Caching frequent API responses (e.g., UMLS or FDA data),

Task queuing for asynchronous processing,

Supporting real-time concurrency and load distribution.

Ensures system responsiveness even under heavy usage.

4. Feedback-driven Learning and Personalization
   
A feedback mechanism is in development that will:

Allow healthcare professionals to validate or correct the system’s suggestions,

Enable continuous fine-tuning of predictions using supervised learning,

Deliver personalized recommendations based on historical interactions.

5. EHR Integration (Planned)
   
Future versions will aim to integrate PharmaMate with Electronic Health Record (EHR) systems, enabling seamless ingestion and analysis of patient data in real clinical environments.

7. Enhanced Data Security & Compliance
   
Ongoing work includes implementing advanced data encryption, user authentication, and ensuring compliance with medical data privacy regulations like HIPAA and GDPR.


Feel free to reach out if you have any questions or suggestions!
