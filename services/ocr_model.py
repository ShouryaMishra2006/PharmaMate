import cv2
import pytesseract
import requests
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
def extract_text_from_image(image_path):
    """Extract text from an image using OCR"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)
    
    return extracted_text.lower() 
def identify_medicines(extracted_text, medicine_list):
    """Find medicines mentioned in the extracted text"""
    found_medicines = [med for med in medicine_list if med in extracted_text]
    return found_medicines
if __name__ == "__main__":
    image_path = "prescription.jpg"  
    extracted_text = extract_text_from_image(image_path)

    print("Extracted Text:", extracted_text)

    medicine_list = get_medicine_list(limit=200)
    identified_medicines = identify_medicines(extracted_text, medicine_list)

    print("Identified Medicines:", identified_medicines)
