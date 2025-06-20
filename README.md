# PharmaMate: AI-powered Clinical Decision Support System

[PharmaMate Demo](https://drive.google.com/file/d/1i1xEozqa_eRYYbxugDlReMW0rJEj1qZe/view?usp=drive_link)


## Overview

PharmaMate is an AI-powered clinical decision support system designed to assist healthcare professionals in making informed decisions based on clinical data. The system combines advanced machine learning and Natural Language Processing (NLP) techniques, including Optical Character Recognition (OCR), hybrid models like SpaCy and ClinicalBERT, and integration with external medical APIs to provide accurate predictions for conditions, treatments, specialists, and drugs. 

## 🔧 Technologies & Features

### 1. 🧠 Hybrid Named Entity Recognition (NER)

PharmaMate uses a hybrid NER pipeline combining:

- **SpaCy** for classical entity recognition of conditions, treatments, and specialist types.
- **ClinicalBERT** for deep contextual understanding of medical language in clinical settings.

> **Accuracy**: This combination achieves over **90%** accuracy in identifying relevant medical entities from text or scanned documents.

---

### 2. 🧬 Custom Dataset with Google SpanBERT

We enhance our data using **Google SpanBERT**, a transformer model fine-tuned for span-based prediction tasks:

- Adds rich context-based span annotations.
- Improves mappings for:
  - **Conditions** (e.g., Asthma, Malaria)
  - **Treatments** (e.g., Antibiotics, Chemotherapy)
  - **Specialists** (e.g., Cardiologist, Oncologist)

---

### 3. 🖼 Optical Character Recognition (OCR)

PharmaMate includes robust OCR for scanned prescriptions and medical notes:

- **Tesseract OCR** converts images into machine-readable text.
- **Preprocessing techniques**:
  - Grayscale conversion
  - Otsu thresholding
  - Binarization

> Improves recognition for **handwritten or poor-quality** prescription images.

---

### 4. 🧑‍⚕️ ClinicalBERT for Specialist & Treatment Prediction

After text extraction (from OCR or direct input), **ClinicalBERT** is used to:

- Predict the **most suitable medical specialist**.
- Suggest **initial treatments or procedures**.

This ensures contextual accuracy and relevance in clinical scenarios.

---

### 5. 🔄 Mapping Symptoms to Conditions using UMLS

Utilizes the **Unified Medical Language System (UMLS)** API to:

- Map user symptoms to medically valid **conditions**.
- Use Concept Unique Identifiers (CUIs) and relationships (`RO`, `RQ`) to extract related diagnoses.

---

### 6. 💊 Drug Suggestions via OpenFDA

Once conditions are identified, PharmaMate queries the **FDA Drug Labeling API**:

- Fetches brand and generic drugs.
- Extracts information from:
  - `indications_and_usage`
  - `openfda.brand_name`
  - `openfda.generic_name`

---

### 7. 🤖 Multi-Agent Intelligence with LangChain

PharmaMate employs a **LangChain-powered multi-agent architecture**:

- **Agent 1**: Analyzes text to determine specialists and treatments.
- **Agent 2**: Maps symptoms to UMLS conditions.
- **Agent 3**: Retrieves drug recommendations from FDA.

> Implemented using `ZeroShotAgent` from **LangChain**, enabling modular reasoning by chaining multiple specialized tools.

---

## ⚙️ Optimizations Performed

- 🧪 **Text Preprocessing**: Lowercasing, de-noising, and medical-aware tokenization.
- 🖼 **OCR Enhancements**: Binarization and noise reduction before OCR for better accuracy.
- 🔍 **Keyword Matching**: Regex-based detection of drugs in OCR output against live FDA data.
- 🔄 **Asynchronous APIs**: FastAPI endpoints are async-enabled for concurrency and faster inference.
- 🧠 **Multi-Agent Reasoning**: LangChain agents are modular and allow natural language orchestration of tasks.

---

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
