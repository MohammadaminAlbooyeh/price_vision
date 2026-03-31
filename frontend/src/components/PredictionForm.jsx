import React, { useState } from "react";
import { getPrediction } from "../services/api";
import { Calculator, Home, Send, Bath, Car, Wind, Sofa, Square } from "lucide-react";

function PredictionForm({ onPredict }) {
  const [formData, setFormData] = useState({
    mode: "sale",
    area: 70,
    rooms: 2,
    bathrooms: 1,
    parking: 1,
    heating: "none",
    furnished: false,
    balcony: false,
    tv: false,
    outsideExposure: false,
    fiber: false,
    gate: false,
    cellar: false,
    commonGarden: false,
    privateGarden: false,
    alarm: false,
    doorman: false,
    pool: false,
    villa: false,
    fullProperty: false,
    apartment: true,
    attic: false,
    loft: false,
    mansard: false,
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const finalValue = type === "checkbox" ? checked : (type === "number" ? (parseFloat(value) || "") : value);
    setFormData({ ...formData, [name]: finalValue });
  };

  const validate = () => {
    if (formData.area <= 0) return "Area must be greater than 0.";
    if (formData.rooms < 0) return "Rooms cannot be negative.";
    if (formData.bathrooms < 0) return "Bathrooms cannot be negative.";
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await getPrediction(formData);
      setPrediction(result.predicted_price);
      if (onPredict) {
        onPredict(result.predicted_price);
      }
    } catch (err) {
      setError(err.message || "Failed to get prediction. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8 border border-gray-100">
      <div className="flex items-center mb-6">
        <Calculator className="w-8 h-8 text-indigo-600 mr-2" />
        <h2 className="text-2xl font-bold text-gray-800">Price Estimator</h2>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center justify-between gap-3 rounded-lg border border-gray-200 p-3 bg-gray-50">
          <label className="text-sm font-semibold text-gray-700">Type</label>
          <div className="flex items-center gap-4">
            <label className="flex items-center space-x-1 text-sm">
              <input
                type="radio"
                name="mode"
                value="sale"
                checked={formData.mode === "sale"}
                onChange={handleChange}
                className="accent-indigo-600"
              />
              <span>Sale</span>
            </label>
            <label className="flex items-center space-x-1 text-sm">
              <input
                type="radio"
                name="mode"
                value="rent"
                checked={formData.mode === "rent"}
                onChange={handleChange}
                className="accent-indigo-600"
              />
              <span>Rent</span>
            </label>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 flex items-center">
              <Square className="w-3 h-3 mr-1" /> Area (m²)
            </label>
            <input
              type="number"
              name="area"
              value={formData.area}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="e.g. 120"
            />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 flex items-center">
              <Home className="w-3 h-3 mr-1" /> Rooms
            </label>
            <input
              type="number"
              name="rooms"
              value={formData.rooms}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="e.g. 3"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 flex items-center">
              <Bath className="w-3 h-3 mr-1" /> Bathrooms
            </label>
            <input
              type="number"
              name="bathrooms"
              value={formData.bathrooms}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="e.g. 2"
            />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 flex items-center">
              <Car className="w-3 h-3 mr-1" /> Parking
            </label>
            <input
              type="number"
              name="parking"
              value={formData.parking}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="0"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase text-gray-500 mb-1 flex items-center">
            <Wind className="w-3 h-3 mr-1" /> Heating
          </label>
          <select 
            name="heating" 
            value={formData.heating} 
            onChange={handleChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-white"
          >
            <option value="none">None / Independent</option>
            <option value="central">Centralized</option>
          </select>
        </div>

        <div className="flex space-x-6 py-2">
          <label className="flex items-center space-x-2 cursor-pointer group">
            <input 
              type="checkbox" 
              name="furnished" 
              checked={formData.furnished} 
              onChange={handleChange}
              className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <span className="text-sm text-gray-700 group-hover:text-indigo-600 transition-colors flex items-center">
              <Sofa className="w-4 h-4 mr-1 opacity-50" /> Furnished
            </span>
          </label>
          <label className="flex items-center space-x-2 cursor-pointer group">
            <input 
              type="checkbox" 
              name="balcony" 
              checked={formData.balcony} 
              onChange={handleChange}
              className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <span className="text-sm text-gray-700 group-hover:text-indigo-600 transition-colors">Balcony</span>
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-indigo-700 transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center space-x-2 shadow-lg shadow-indigo-100"
        >
          {loading ? "Calculating..." : <><Send className="w-4 h-4" /> <span>Calculate Price</span></>}
        </button>
      </form>


      {error && (
        <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-lg border border-red-100 flex items-center">
          <p>{error}</p>
        </div>
      )}

      {prediction !== null && (
        <div className="mt-8 p-6 bg-green-50 rounded-xl border border-green-100 text-center animate-pulse">
          <p className="text-gray-600 text-sm font-medium uppercase tracking-wider mb-2">Estimated Price</p>
          <h3 className="text-4xl font-extrabold text-green-700">
            ${prediction.toLocaleString()}
          </h3>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;