import { useState } from 'react';
import { predictFraud } from '../services/fraudApi';

const INITIAL_FORM = {
  type: 'TRANSFER',
  amount: '',
  oldbalanceOrg: '',
  newbalanceOrig: '',
  oldbalanceDest: '',
  newbalanceDest: '',
};

export function usePrediction() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateField = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setError(null);
  };

  const fillForm = (data) => {
    setForm({
      type: data.type,
      amount: String(data.amount),
      oldbalanceOrg: String(data.oldbalanceOrg),
      newbalanceOrig: String(data.newbalanceOrig),
      oldbalanceDest: String(data.oldbalanceDest),
      newbalanceDest: String(data.newbalanceDest),
    });
    setResult(null);
    setError(null);
  };

  const reset = () => {
    setForm(INITIAL_FORM);
    setResult(null);
    setError(null);
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        type: form.type,
        amount: parseFloat(form.amount),
        oldbalanceOrg: parseFloat(form.oldbalanceOrg),
        newbalanceOrig: parseFloat(form.newbalanceOrig),
        oldbalanceDest: parseFloat(form.oldbalanceDest),
        newbalanceDest: parseFloat(form.newbalanceDest),
      };

      const data = await predictFraud(payload);
      setResult({ ...data, input: payload });
    } catch (err) {
      setError(err.message || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isFraud = result?.prediction === 1;
  const probability = result?.fraud_probability ?? null;

  return {
    form,
    result,
    loading,
    error,
    isFraud,
    probability,
    updateField,
    fillForm,
    submit,
    reset,
  };
}
