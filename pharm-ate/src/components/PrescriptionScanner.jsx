import React, { useEffect, useState } from "react";
import { Card, CardContent } from "./ui/Card.jsx";
import { Button } from "./ui/button.jsx";
import { Camera, Search, History } from "lucide-react";

export default function PrescriptionScanner() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [suggestedMedicines, setSuggestedMedicines] = useState([]);
  const [possibleconditions, setpossibleconditions] = useState([]);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
    }
  };
  const analyzePrescription = async () => {
    if (!selectedImage) {
      alert("Please select an image first!");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const response = await fetch(
        "http://localhost:5000/analyze-prescription",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();
      console.log("Analysis Result:", data);
      setAnalysisResult(data);
    } catch (error) {
      console.error("Error analyzing prescription:", error);
    }
  };

  const suggestMedicines = async () => {
    console.log("here clicked");
    if (!analysisResult) {
      alert("Please upload image and check recommended specialist first");
      return;
    }
    try {
      const response = await fetch("http://localhost:5000/suggest-medicines", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ extracted_text: analysisResult.extracted_text }),
      });

      const data = await response.json();
      console.log("Medicine Suggestions:", data);
      setSuggestedMedicines(data.recommended_drugs || []);
      setpossibleconditions(data.conditions || []);
    } catch (error) {
      console.log("Error suggesting medicines: ", error);
    }
  };
  const formatLinkTitle = (url) => {
    try {
      const path = new URL(url).pathname;
      const segments = path.split("/").filter(Boolean);
      if (segments.length === 0) return "MedlinePlus";

      const rawTitle = segments[segments.length - 1];
      return rawTitle
        .replace(/[-_]/g, " ")
        .replace(/\.\w+$/, "") // remove file extension if any
        .replace(/\b\w/g, (char) => char.toUpperCase()); // capitalize
    } catch {
      return "Resource";
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gradient-to-b from-blue-100 to-gray-100 min-h-screen">
      <h1 className="text-3xl font-extrabold text-blue-700 mb-6">
        👋 HI! I AM YOUR PHARM-ATE
      </h1>

      <Card className="w-full max-w-md p-6 shadow-xl rounded-lg bg-white">
        <CardContent className="flex flex-col gap-6">
          <h2 className="text-xl font-semibold text-gray-700">
            📄 Scan Your Prescription
          </h2>

          <div className="flex flex-col items-center gap-3">
            {/* Hidden File Input */}
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
              id="fileInput"
            />

            {/* Upload Button */}
            <label
              htmlFor="fileInput"
              className="cursor-pointer flex items-center gap-2 border p-2 rounded-lg text-sm w-full justify-center bg-gray-200 hover:bg-gray-300"
            >
              <Camera className="w-5 h-5" />{" "}
              {selectedImage ? "Image Selected" : "Upload Image"}
            </label>
          </div>

          {/* Analyze Prescription Button */}
          <Button
            className="bg-blue-600 hover:bg-blue-700 text-white transition-all py-2 rounded-lg flex items-center justify-center gap-2"
            onClick={analyzePrescription}
          >
            <Search className="w-5 h-5" /> Analyze Prescription
          </Button>
          {analysisResult && (
            <div className="mt-4 p-4 bg-green-50 border border-green-300 rounded-md text-green-800 text-sm">
              <p>
                <strong>📝 Extracted Text:</strong>{" "}
                {analysisResult.extracted_text}
              </p>
              <p>
                <strong>👨‍⚕️ Recommended Specialist:</strong>{" "}
                {analysisResult.specialist}
              </p>
              <p>
                <strong>Suggested Treatments:</strong>{" "}
                {analysisResult.treatment}
              </p>
            </div>
          )}

          <hr className="border-gray-300" />

          <h2 className="text-lg font-semibold text-gray-700">
            📜 Need More Assistance?
          </h2>

          <Button
            variant="outline"
            className="flex items-center gap-2 border-gray-800 hover:bg-gray-100"
            onClick={suggestMedicines}
          >
            <h3 className="text-blue-600">
              See Possible Conditions and Drugs for Cure
            </h3>
          </Button>

          {suggestedMedicines.length > 0 && (
            <div className="mt-8 p-6 bg-blue-50 border-l-4 border-blue-500 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <span className="text-blue-600 text-xl mr-2">*</span>
                <h2 className="text-blue-800 font-semibold text-lg">
                  Suggested Medicines:
                </h2>
              </div>
              <ul className="space-y-3 text-left">
                {suggestedMedicines.map((medicine, index) => (
                  <li key={index} className="font-medium">
                    🔹 {medicine}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {possibleconditions.length > 0 && (
            <div className="mt-8 p-6 bg-blue-50 border-l-4 border-blue-500 rounded-lg shadow-md">
              <div className="flex items-center mb-4">
                <span className="text-blue-600 text-xl mr-2">*</span>
                <h2 className="text-blue-800 font-semibold text-lg">
                  Possible Conditions:
                </h2>
              </div>
              <ul className="space-y-3 text-left">
                {possibleconditions.map((condition, index) => (
                  <li key={index} className="font-medium">
                    🔹 {condition}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
