import axios from "axios";

const API_URL = ""; // Use relative path for Vite proxy

export const getPrediction = async (data) => {
  try {
    // Map frontend camelCase to backend expected snake_case/aliases
    const payload = {
      mode: data.mode || "sale",
      superficie: data.area,
      stanze: data.rooms,
      bagni: data.bathrooms,
      "posti auto": data.parking || 0,
      "riscaldamento centralizzato": data.heating === "central" ? 1 : 0,
      arredato: data.furnished ? 1 : 0,
      balcone: data.balcony ? 1 : 0,
      "impianto tv": data.tv ? 1 : 0,
      "esposizione esterna": data.outsideExposure ? 1 : 0,
      "fibra ottica": data.fiber ? 1 : 0,
      "cancello elettrico": data.gate ? 1 : 0,
      cantina: data.cellar ? 1 : 0,
      "giardino comune": data.commonGarden ? 1 : 0,
      "giardino privato": data.privateGarden ? 1 : 0,
      "impianto allarme": data.alarm ? 1 : 0,
      portiere: data.doorman ? 1 : 0,
      piscina: data.pool ? 1 : 0,
      villa: data.villa ? 1 : 0,
      "intera proprieta": data.fullProperty ? 1 : 0,
      appartamento: data.apartment ? 1 : 0,
      attico: data.attic ? 1 : 0,
      loft: data.loft ? 1 : 0,
      mansarda: data.attic ? 1 : 0,
      year: data.year || new Date().getFullYear(),
      month: data.month || new Date().getMonth() + 1,
    };
    
    const response = await axios.post(`/predict`, payload);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || error.message || "Unknown error";
    console.error("API Call Error:", message);
    throw new Error(message);
  }
};
