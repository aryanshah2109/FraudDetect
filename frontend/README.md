# FraudDetect — Frontend

A production-grade React frontend for the FraudDetect ML fraud detection API.

## Tech Stack
- **React 18** + **Vite 5** — Fast development & build
- **TailwindCSS 3** — Utility-first styling
- **Axios** — API calls with interceptors
- **Space Mono** + **Syne** fonts — Distinctive typography

## Design
Dark cyber-intelligence aesthetic: deep navy/black background, cyan accent (#00d4ff), red danger (#ff3d5a), green safe (#00e5a0). Grid overlay, scanline effects, glowing panels.

## Setup & Run

```bash
# Install dependencies
npm install

# Start dev server (ensure backend is running at http://localhost:8000)
npm run dev

# Build for production
npm run build
```

Open: http://localhost:5173

## Project Structure

```
src/
├── components/
│   ├── Header.jsx         # Sticky nav + live API status
│   ├── HeroSection.jsx    # Title, description, use cases
│   ├── StatsBar.jsx       # Model stats cards
│   ├── PredictionForm.jsx # Transaction input form
│   ├── ResultCard.jsx     # Verdict, probability bar, balance chart
│   └── InfoPanel.jsx      # How-it-works + example payload
├── pages/
│   └── Dashboard.jsx      # Main layout page
├── services/
│   └── fraudApi.js        # Axios API layer
├── hooks/
│   └── usePrediction.js   # Form state + prediction logic
├── styles/
│   └── index.css          # Global styles + animations
├── App.jsx
└── main.jsx
```

## API

Assumes backend at `http://localhost:8000`

```
GET  /          → Health check
POST /predict/  → Fraud prediction
```

### Example Request
```json
POST /predict/
{
  "type": "TRANSFER",
  "amount": 100000,
  "oldbalanceOrg": 50000,
  "newbalanceOrig": 0,
  "oldbalanceDest": 10000,
  "newbalanceDest": 110000
}
```

### Example Response
```json
{
  "prediction": 1,
  "prediction_label": "Fraud",
  "fraud_probability": 0.87
}
```

## UI Features

- 🟢/🔴 Live API status indicator in header
- Real-time form with all 6 transaction fields
- Animated probability bar (red=fraud, green=safe)
- Risk level badge (Low / Medium / High / Critical)
- Balance delta visualization chart
- Transaction summary with balance error detection
- Raw API response viewer (collapsible JSON)
- Loading spinner during inference
- Error handling with descriptive messages
- Responsive grid layout (mobile → desktop)
