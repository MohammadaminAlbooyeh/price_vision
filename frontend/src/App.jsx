import React, { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import PredictionChart from "./components/PredictionChart";

function App() {
    const [allPredictions, setAllPredictions] = useState([]);

    const handleNewPrediction = (price) => {
      setAllPredictions([...allPredictions, price]);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-start p-8">
            <header className="mb-12 text-center">
              <h1 className="text-5xl font-black text-gray-900 tracking-tight mb-2">
                Price<span className="text-indigo-600">Vision</span>
              </h1>
              <p className="text-gray-500 font-medium italic">Predicting House Prices with Multi-Model Machine Learning</p>
            </header>
            <main className="w-full max-w-4xl grid md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <PredictionForm onPredict={handleNewPrediction} />
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 h-full flex items-center justify-center">
                {allPredictions.length > 0 ? (
                  <PredictionChart predictions={allPredictions} />
                ) : (
                  <p className="text-gray-400 font-medium italic">Predictions chart will appear here...</p>
                )}
              </div>
            </main>
            <footer className="mt-auto pt-16 text-gray-400 text-sm">
              &copy; 2026 PriceVision Project. Professional CV Prototype.
            </footer>
        </div>
    );
}

export default App;
