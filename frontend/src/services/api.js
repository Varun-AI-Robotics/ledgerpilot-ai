import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});


// ==========================================
// Metrics
// ==========================================

export const getMetrics = async () => {
  const response = await API.get("/api/metrics");

  return response.data;
};


// ==========================================
// Reconciliation
// ==========================================

export const getReconciliation = async (
  page = 1,
  limit = 100,
  search = ""
) => {
  const response = await API.get("/api/reconciliation", {
    params: {
      page,
      limit,
      search,
    },
  });

  return response.data;
};


// ==========================================
// Exceptions
// ==========================================

export const getExceptions = async () => {
  const response = await API.get("/api/exceptions");

  return response.data;
};


// ==========================================
// Matched
// ==========================================

export const getMatched = async () => {
  const response = await API.get("/api/matched");

  return response.data;
};


// ==========================================
// Partial
// ==========================================

export const getPartial = async () => {
  const response = await API.get("/api/partial");

  return response.data;
};


// ==========================================
// AI Assistant
// ==========================================

export const askAI = async (question) => {
  const response = await API.post(
    "/api/ai/ask",
    {
      question,
    }
  );

  return response.data;
};


// ==========================================
// AI Investigation
// ==========================================

export const investigatePayment = async (paymentId) => {
  const response = await API.post(
    `/api/ai/investigate/${paymentId}`
  );

  return response.data;
};


export default API;