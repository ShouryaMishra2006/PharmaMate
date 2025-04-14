import express from "express";
import cors from "cors";
import analyzeRoutes from "./routes/analyzeRoute.js"
const app = express();
const PORT = process.env.PORT || 5000;
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("PharmaMate Backend is Running...");
});


app.use("/", analyzeRoutes);

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
