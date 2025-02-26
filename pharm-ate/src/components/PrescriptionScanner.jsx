import React from "react";
import { Card, CardContent } from "./ui/Card.jsx";
import { Input } from "./ui/input.jsx";
import { Button } from "./ui/button.jsx";
import { Camera, Search, History } from "lucide-react";

export default function PrescriptionScanner() {
  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gradient-to-b from-blue-100 to-gray-100 min-h-screen">
      <h1 className="text-3xl font-extrabold text-blue-700 mb-6">👋 HI! I AM YOUR PHARM-ATE</h1>
      
      <Card className="w-full max-w-md p-6 shadow-xl rounded-lg bg-white">
        <CardContent className="flex flex-col gap-6">
          <h2 className="text-xl font-semibold text-gray-700">📄 Scan Your Prescription</h2>
          
          <div className="flex items-center gap-3">
            <Input type="file" accept="image/*" className="border p-2 rounded-lg flex-1 text-sm" />
            <Button variant="outline" className="flex items-center gap-2 border-gray-400 hover:bg-gray-200">
              <Camera className="w-5 h-5" /> Upload
            </Button>
          </div>

          <Button className="bg-blue-600 hover:bg-blue-700 text-white transition-all py-2 rounded-lg flex items-center justify-center gap-2">
            <Search className="w-5 h-5" /> Analyze Prescription
          </Button>

          <hr className="border-gray-300" />

          <h2 className="text-lg font-semibold text-gray-700">📜 Past Prescriptions</h2>
          <Button variant="outline" className="flex items-center gap-2 border-gray-400 hover:bg-gray-200">
            <History className="w-5 h-5" /> View History
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
