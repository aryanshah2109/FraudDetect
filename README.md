# FraudDetect: Credit Card Fraud Detection System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-green.svg)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.1.3-orange.svg)](https://xgboost.readthedocs.io/)
[![MLflow](https://img.shields.io/badge/MLflow-3.9.0-red.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> A production-ready, end-to-end machine learning system for detecting fraudulent credit card transactions in real-time with industry-level experimentation and tracking.

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Docker Setup](#-docker-setup)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Frontend](#-frontend)
- [Project Structure](#-project-structure)
- [Data Pipeline](#-data-pipeline)
- [Model Training](#-model-training)
- [Configuration](#-configuration)
- [Monitoring & Logging](#-monitoring--logging)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**FraudDetect** is a sophisticated, production-grade ML system that detects fraudulent credit card transactions with high precision and minimal false positives. It combines:

- **Advanced ML Engineering**: XGBoost classifier with GPU acceleration (CUDA)
- **MLOps Best Practices**: MLflow experiment tracking, DVC data versioning, reproducible pipelines
- **Real-Time API**: FastAPI-based REST microservice for sub-100ms predictions
- **Intelligent Thresholding**: Precision-recall optimization with configurable constraints
- **Enterprise-Ready**: Full logging, error handling, CORS support, singleton pattern

### Key Statistics

- **Model**: XGBoost Classifier with 263 estimators
- **Training Data**: Stratified 80-20 split with cross-validation
- **Precision Constraint**: ≥65% minimum (user-configurable)
- **Threshold Optimization**: Precision-recall curves on validation set
- **Inference Latency**: <100ms per prediction
- **GPU Support**: CUDA-optimized training and inference

---

## ✨ Key Features

### 🔮 Real-Time Fraud Detection
- Sub-100ms prediction latency via optimized XGBoost model
- REST API endpoint for seamless integration
- Probability scores with binary fraud/legitimate classifications
- Structured JSON responses for easy client handling

### ⚡ GPU-Accelerated Training
- CUDA-optimized XGBoost with histogram tree method
- Faster training on large-scale transaction datasets
- GPU predictor for accelerated inference
- Fallback to CPU if CUDA unavailable

### 🏭 Production-Grade Infrastructure
- **Logging**: Comprehensive DEBUG-level logging (configurable)
- **Error Handling**: Global exception handlers with detailed responses
- **CORS**: Cross-origin requests enabled for multiple clients
- **Efficiency**: Singleton pattern—model loaded once, reused for all requests

### ⚖️ Imbalanced Data Handling
- `scale_pos_weight=7.45` weights minority fraud class heavily
- Stratified train-test splits maintain class distribution
- Precision-constrained threshold optimization (default: ≥65%)
- Automatic fallback to F1-score if precision constraint unmet

### 📊 Experiment Tracking & Versioning
- **MLflow**: Run tracking, parameter logging, metrics comparison
- **DVC**: Data versioning and reproducibility
- **DagHub**: Remote MLflow tracking server
- **Artifacts**: Timestamped experiment outputs (params, metrics, plots)

### 🔧 Automated Feature Engineering
- Balance error detection: `|amount - balance_delta|`
- One-hot encoding for categorical transaction types
- StandardScaler normalization for numerical features
- Domain-aware missing value imputation (median/mode)

---

## 🛠️ Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **API** | FastAPI | 0.128.0 | REST framework |
| **Server** | Uvicorn | 0.40.0 | ASGI server |
| **Frontend** | HTML, CSS, JS | ... | User interface |
| **ML Model** | XGBoost | 3.1.3 | Gradient boosting classifier |
| **Preprocessing** | scikit-learn | 1.8.0 | Data transformation |
| **Data** | pandas, numpy | 2.3.3, 2.4.2 | Data manipulation |
| **MLOps** | MLflow | 3.9.0 | Experiment tracking |
| **Serialization** | joblib | 1.5.3 | Model persistence |
| **Validation** | Pydantic | 2.12.5 | Request/response validation |
| **Viz** | matplotlib, seaborn | 3.10.8, 0.13.2 | Plotting |

---

## 📦 Prerequisites

- **Python**: 3.9 or higher
- **CUDA** (optional): Required for GPU acceleration; CPU fallback available
- **pip**: Python package manager
- **Virtual Environment**: venv or conda (recommended)
- **Disk Space**: ~2-5GB for data, models, artifacts
- **Network**: Internet access for MLflow and DagHub
- **Docker** (optional): For containerized deployment and easy setup

---

## 💾 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/FraudDetect.git
cd FraudDetect
```

### Step 2: Create Virtual Environment
```bash
# Using venv (recommended)
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install project in development mode
pip install -e .
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```bash
MLFLOW_TRACKING_URI=https://dagshub.com/yourusername/FraudDetect.mlflow
MLFLOW_EXPERIMENT_NAME=Main_Experiment
LOG_LEVEL=DEBUG
API_HOST=0.0.0.0
API_PORT=8000
```

### Step 5: Verify Installation
```bash
# Check packages
pip list | grep -E 'fastapi|xgboost|mlflow'

# Test imports
python -c "import fastapi; import xgboost; import mlflow; print('✓ All packages installed')"
```

### Step 6: Frontend (static)
The repository includes a lightweight static frontend located in the `frontend/` folder. You can open the HTML files directly in your browser or serve them with a simple static server.

---

## � Docker Setup

If you prefer using Docker, you can run the application with Docker Compose. This is recommended for easy deployment and to avoid dependency conflicts.

### Prerequisites for Docker
- Docker installed on your system
- Docker Compose installed

### Build and Run with Docker Compose
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

This will start the backend API on http://localhost:8000.

**Access points (Local Development):**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Frontend: http://localhost:5500

**Access points (Production):**
- API: https://frauddetect-backend-jpgf.onrender.com/
- Interactive Docs: https://frauddetect-backend-jpgf.onrender.com/docs
- Frontend: https://frauddetect-1gju.onrender.com//

---

## �🚀 Quick Start

### Start the API Server
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Access points (Local Development):**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Start the Frontend
You can open the frontend directly or serve it with a simple static server.

Open in browser (quick):

1. Open `frontend/index.html` in your browser (double-click or `File → Open`).

Serve with Python (recommended for correct URL handling):

```bash
# from project root
cd frontend
# serve on port 4173 (or any free port)
python -m http.server 4173
# then open: http://localhost:4173/index.html
```

Or use any static file server you prefer (live-server, http-server, etc.).

### Make a Prediction
```bash
curl -X POST "https://frauddetect-backend-jpgf.onrender.com/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TRANSFER",
    "amount": 100000,
    "oldbalanceOrg": 50000,
    "newbalanceOrig": 0,
    "oldbalanceDest": 10000,
    "newbalanceDest": 110000
  }'

# Response:
# {
#   "prediction": 1,
#   "prediction_label": "Fraud",
#   "fraud_probability": 0.87
# }
```

### Train the Model
```bash
# Run complete training pipeline
python -m test.py

# This will:
# 1. Load raw data
# 2. Split: Train 80%, Test 20%
# 3. Feature engineering & preprocessing
# 4. XGBoost training
# 5. Threshold optimization on validation set
# 6. Evaluation on test set
# 7. Save artifacts
# 8. Log experiment to MLflow
```

---

## 📡 API Documentation

### Base URL
```
Local Development: http://localhost:8000
Production: https://frauddetect-backend-jpgf.onrender.com/
```

### Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "FraudDetect - A High Level Fraud Detection System"
}
```

### Fraud Detection Endpoint
```http
POST /predict/
Content-Type: application/json
```

#### Request
```json
{
  "type": "TRANSFER",
  "amount": 100000.0,
  "oldbalanceOrg": 50000.0,
  "newbalanceOrig": 0.0,
  "oldbalanceDest": 10000.0,
  "newbalanceDest": 110000.0
}
```

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `type` | string | ✓ | CASH IN, CASH OUT, DEBIT, PAYMENT, TRANSFER | Transaction type |
| `amount` | float | ✓ | ≥ 0 | Transaction amount |
| `oldbalanceOrg` | float | ✓ | ≥ 0 | Sender's balance before |
| `newbalanceOrig` | float | ✓ | ≥ 0 | Sender's balance after |
| `oldbalanceDest` | float | ✓ | ≥ 0 | Receiver's balance before |
| `newbalanceDest` | float | ✓ | ≥ 0 | Receiver's balance after |

#### Response
```json
{
  "prediction": 1,
  "prediction_label": "Fraud",
  "fraud_probability": 0.8734
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | integer | 0=Legitimate, 1=Fraud |
| `prediction_label` | string | Human-readable label |
| `fraud_probability` | float | Confidence (0.0-1.0) |

#### Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Validation error |
| 500 | Server error |

#### Example: Python Client
```python
import requests

url = "https://frauddetect-backend-jpgf.onrender.com/predict/"
payload = {
    "type": "TRANSFER",
    "amount": 100000,
    "oldbalanceOrg": 50000,
    "newbalanceOrig": 0,
    "oldbalanceDest": 10000,
    "newbalanceDest": 110000
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Prediction: {result['prediction_label']}")
print(f"Fraud Probability: {result['fraud_probability']:.2%}")
```

---

## 🎨 Frontend

The frontend is a lightweight static UI implemented with plain HTML, CSS and vanilla JavaScript. It consumes the backend API (`/predict/` and `/artifacts/`) to display predictions and experiment artifacts.

### Features
- **Real-Time Predictions**: Submit transaction data and receive instant fraud detection results
- **Responsive Layout**: Works across desktop and mobile devices with CSS-based responsiveness
- **Client-side Error Handling**: Friendly messages when the API is unavailable
- **Lightweight, easy to host**: No build step required for the included UI

### Technologies
- **Vanilla JavaScript**: API calls, DOM manipulation
- **Plain CSS**: Custom styles located in `frontend/css/`
- **Static HTML**: Entry points in `frontend/index.html` and `frontend/artifacts.html`

### Usage
1. Start the backend API (see Quick Start)
2. Start the frontend (see Quick Start)
3. Open http://localhost:5500 in your browser
4. Enter transaction details and submit for fraud detection

---

## 📁 Project Structure

```
FraudDetect/
├── app/                          # FastAPI application
│   ├── main.py                   # App, CORS, exception handlers
│   ├── core/config.py            # Model loading
│   ├── routers/                  # API endpoints
│   ├── schemas/                  # Pydantic models
│   └── services/                 # Prediction logic
│
├── frontend/                     # Static frontend (HTML/CSS/JS)
│   ├── index.html                # Main UI (Detect)
│   ├── artifacts.html            # Artifacts / Experiments page
│   ├── css/                      # Stylesheets
│   │   ├── styles.css
│   │   └── artifacts.css
│   └── js/                       # Frontend scripts
│       ├── app.js
│       ├── artifacts.js
│       ├── experiments.js
│       └── env.js                # API base URL configuration
│
├── src/                          # ML training & utilities
│   ├── config/                   # Configuration (YAML)
│   ├── data/                     # Data loading & preprocessing
│   ├── evaluation/               # Metrics & threshold optimization
│   ├── pipelines/                # Training orchestration
│   ├── training/                 # XGBoost trainer
│   ├── utils/                    # Artifacts & MLflow setup
│   └── visualization/            # Plotting utilities
│
├── data/
│   ├── raw/                      # Original data
│   ├── interim/                  # Intermediate data
│   └── processed/                # Final train/test splits
│
├── models/
│   ├── best_model.pkl            # Serialized XGBoost
│   ├── best_preprocessor.pkl     # Preprocessing pipeline
│   └── best_metrics.json         # Threshold & metrics
│
├── artifacts/                    # Experiment outputs (timestamped)
├── logs/                         # Application logs
├── notebooks/                    # Jupyter notebooks
├── reports/                      # Generated reports
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Project packaging
├── Makefile                      # Make commands
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 🔄 Data Pipeline

```
Raw Data → Load → Split (80:20) → Feature Engineering → Preprocessing 
→ Training → Validation → Threshold Optimization → Test Evaluation 
→ Serialization
```

### Features

**Numerical Input (7):**
- `amount`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`
- `errorBalanceOrig`, `errorBalanceDest` (calculated)

**Categorical Input (1):**
- `type` - Transaction type

**Target:**
- `isFraud` - 0=Legitimate, 1=Fraud

**Dropped:**
- `step`, `nameOrig`, `nameDest`, `isFlaggedFraud`

---

## 🤖 Model Training

### XGBoost Configuration
```yaml
n_estimators: 263
max_depth: 11
learning_rate: 0.0816
subsample: 0.5564
colsample_bytree: 0.5639
scale_pos_weight: 7.45 (imbalance handling)
objective: binary:logistic
tree_method: hist
device: cuda (GPU acceleration)
```

### Training Steps
1. Load & split data (80:20 stratified)
2. Feature engineering & preprocessing
3. Train XGBoost model
4. Optimize threshold on validation set
   - **Constraint**: Precision ≥ 65%
   - **Objective**: Maximize recall
   - **Fallback**: F1-score
5. Evaluate on test set
6. Save model & metrics to MLflow

### Metrics Tracked
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC, PR-AUC (primary)
- Confusion Matrix

---

## ⚙️ Configuration

### Main Config: `src/config/config.yaml`
```yaml
# All parameters in one YAML file
# Edit to customize model, training, and feature parameters
```

### Environment: `.env`
```bash
MLFLOW_TRACKING_URI=https://dagshub.com/yourusername/FraudDetect.mlflow
LOG_LEVEL=DEBUG
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📊 Monitoring & Logging

### Logs
```bash
# Real-time
tail -f logs/app.log

# View all
cat logs/app.log
```

### MLflow
```bash
# Start UI
mlflow ui
# Visit: http://localhost:5000
```

### Error Responses
```json
{
  "error": "Model Inference Failed",
  "detail": "Error message here"
}
```

---

## 🔧 Common Commands

```bash
# Setup
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cd frontend && npm install && cd ..

# Run Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run Frontend
cd frontend && npm run dev

# Train
python -m test.py

# Monitor
mlflow ui
tail -f logs/app.log
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| CUDA not available | Model uses CPU fallback |
| Port 8000 busy | Use `--port 8001` |
| Port 5173 busy | Use `npm run dev -- --port 5174` |
| Model not found | Train: `python -m src.pipelines.training_pipeline` |
| MLflow error | Check `MLFLOW_TRACKING_URI` in `.env` |
| Frontend build error | `cd frontend && npm install` |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/your-feature`
3. **Make changes** (follow PEP 8, add tests)
4. **Commit**: `git commit -m "Add: Description"`
5. **Push**: `git push origin feature/your-feature`
6. **Pull Request**: Submit PR with clear description

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👥 Contact

| Item | Details |
|------|---------|
| **Author** | [Aryan Shah] |
| **Email** | [aryanrshah2109@gmail.com] |
| **GitHub** | [@aryanshah2109](https://github.com/aryanshah2109) |
| **Issues** | [GitHub Issues](https://github.com/aryanshah2109/FraudDetect/issues) |

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [DVC Documentation](https://dvc.org/doc)

---

**Version**: 1.0.0  
**Last Updated**: March 5, 2026  
**Status**: Production Ready ✓
