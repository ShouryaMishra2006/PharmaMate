import axios from "axios";

export const analyzePrescription = async (req, res) => {
  try {
    const { image } = req.body;

    if (!image) {
      return res.status(400).json({ error: "Image file is required" });
    }
    print("mai yaha hu")
    const pythonBackendURL = "http://localhost:8000/upload";

    const response = await axios.post(pythonBackendURL, { image });
    print(response)
    return res.json(response.data);
  } catch (error) {
    console.error("Error analyzing prescription:", error.message);
    return res.status(500).json({ error: "Internal Server Error" });
  }
};
