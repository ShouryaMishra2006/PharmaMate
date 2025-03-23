import cv2
import pytesseract
import requests
import re

def identify_medicines(extracted_text, medicine_list):
    """
    Identify the medicines from a list that appear in the extracted text.

    Parameters:
    extracted_text (str): The text to search through.
    medicine_list (list): A list of medicine names to look for.

    Returns:
    list: A list of identified medicines found in the extracted text.
    """
    # Convert the extracted text to lower case for case-insensitive comparison
    extracted_text_lower = extracted_text.lower()
    
    # Initialize an empty list to store identified medicines
    identified_medicines = []

    # Loop through the list of medicines and check if they appear in the extracted text
    for medicine in medicine_list:
        # Use a regular expression to search for whole word matches, case insensitive
        if re.search(r'\b' + re.escape(medicine.lower()) + r'\b', extracted_text_lower):
            identified_medicines.append(medicine)
    
    return identified_medicines
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
def process_prescription(extracted_text, medicine_list):
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
