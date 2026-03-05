import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[FraudDetect API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error normalization
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      let message = data?.detail || data?.error || 'An error occurred with the server.';
      // FastAPI 422 returns an array of validation errors
      if (status === 422 && Array.isArray(data?.detail)) {
        message = data.detail
          .map((e) => `${e.loc?.slice(-1)[0] ?? 'field'}: ${e.msg}`)
          .join(', ');
      }
      throw { status, message, raw: data };
    } else if (error.request) {
      throw {
        status: 0,
        message: 'Cannot reach the FraudDetect API. Make sure the backend is running at ' + API_BASE_URL,
        raw: null,
      };
    } else {
      throw { status: -1, message: error.message || 'An unexpected error occurred.', raw: null };
    }
  }
);

/**
 * Health check endpoint
 * GET /
 */
export const checkHealth = async () => {
  const response = await api.get('/');
  return response.data;
};

/**
 * Fraud prediction endpoint
 * POST /predict/
 *
 * @param {Object} transaction
 * @param {string} transaction.type - Transaction type (CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER)
 * @param {number} transaction.amount - Transaction amount (≥ 0)
 * @param {number} transaction.oldbalanceOrg - Sender balance before transaction
 * @param {number} transaction.newbalanceOrig - Sender balance after transaction
 * @param {number} transaction.oldbalanceDest - Receiver balance before transaction
 * @param {number} transaction.newbalanceDest - Receiver balance after transaction
 *
 * @returns {Promise<{prediction: number, prediction_label: string, fraud_probability: number}>}
 */
export const predictFraud = async (transaction) => {
  const response = await api.post('/predict/', transaction);
  return response.data;
};

export default api;
