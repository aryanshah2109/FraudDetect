// FraudDetect — Frontend JS
// API: https://frauddetect-backend-jpgf.onrender.com

const API_URL = 'https://frauddetect-backend-jpgf.onrender.com/predict/';

// ─── Presets ───────────────────────────────────────────────
const PRESETS = {
  fraud: {
    type: 'TRANSFER',
    amount: 1000000,
    oldbalanceOrg: 1000000,
    newbalanceOrig: 0,
    oldbalanceDest: 0,
    newbalanceDest: 1000000,
  },
  legit: {
    type: 'PAYMENT',
    amount: 5000,
    oldbalanceOrg: 80000,
    newbalanceOrig: 75000,
    oldbalanceDest: 20000,
    newbalanceDest: 25000,
  },
  cashout: {
    type: 'CASH_OUT',
    amount: 500000,
    oldbalanceOrg: 500000,
    newbalanceOrig: 0,
    oldbalanceDest: 10000,
    newbalanceDest: 510000,
  },
};

// ─── DOM refs ─────────────────────────────────────────────
const $ = (id) => document.getElementById(id);

const detectBtn = $('detect-btn');
const resetBtn = $('reset-btn');
const btnLoader = $('btn-loader');
const retryBtn = $('retry-btn');
const copyBtn = $('copy-btn');

const resultPlaceholder = $('result-placeholder');
const resultContent = $('result-content');
const resultError = $('result-error');
const resultVerdict = $('result-verdict');
const probValue = $('prob-value');
const probBar = $('prob-bar');
const resultMetrics = $('result-metrics');
const jsonBody = $('json-body');
const errorMsg = $('error-msg');

// Form fields
const txnType = $('txn-type');
const amount = $('amount');
const oldBalOrig = $('old-bal-orig');
const newBalOrig = $('new-bal-orig');
const oldBalDest = $('old-bal-dest');
const newBalDest = $('new-bal-dest');

// ─── Map CASH_OUT → CASH OUT for display ─────────────────
const TYPE_MAP = {
  TRANSFER: 'TRANSFER',
  CASH_OUT: 'CASH OUT',
  PAYMENT: 'PAYMENT',
  CASH_IN: 'CASH IN',
  DEBIT: 'DEBIT',
};

// ─── Presets ─────────────────────────────────────────────
document.querySelectorAll('.preset-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const preset = PRESETS[btn.dataset.preset];
    if (!preset) return;
    txnType.value = preset.type;
    amount.value = preset.amount;
    oldBalOrig.value = preset.oldbalanceOrg;
    newBalOrig.value = preset.newbalanceOrig;
    oldBalDest.value = preset.oldbalanceDest;
    newBalDest.value = preset.newbalanceDest;
  });
});

// ─── Reset ───────────────────────────────────────────────
resetBtn.addEventListener('click', () => {
  txnType.value = 'TRANSFER';
  amount.value = '';
  oldBalOrig.value = '';
  newBalOrig.value = '';
  oldBalDest.value = '';
  newBalDest.value = '';
  showPlaceholder();
});

// ─── States ───────────────────────────────────────────────
function showPlaceholder() {
  resultPlaceholder.style.display = 'flex';
  resultContent.style.display = 'none';
  resultError.style.display = 'none';
}

function showResult(data) {
  resultPlaceholder.style.display = 'none';
  resultContent.style.display = 'block';
  resultError.style.display = 'none';

  const isFraud = data.prediction === 1;
  const prob = data.fraud_probability;
  const probPct = Math.round(prob * 100);
  const threshold = data.threshold || 0.35;

  // Verdict
  resultVerdict.className = `result-verdict ${isFraud ? 'fraud' : 'legit'}`;
  resultVerdict.innerHTML = `
    <span class="verdict-icon">${isFraud ? '⚠️' : '✅'}</span>
    <div class="verdict-body">
      <div class="verdict-label">${isFraud ? 'FRAUD DETECTED' : 'LEGITIMATE'}</div>
      <div class="verdict-sub">${isFraud ? 'This transaction appears fraudulent' : 'No fraud indicators found'}</div>
    </div>
    <span class="verdict-tag">${isFraud ? 'ALERT' : 'SAFE'}</span>
  `;

  // Probability bar
  probValue.textContent = `${probPct}%`;
  probBar.className = `prob-bar-fill ${isFraud ? 'danger' : 'safe'}`;

  // Animate bar after a tiny delay
  setTimeout(() => {
    probBar.style.width = `${probPct}%`;
  }, 50);

  // Threshold line position (threshold * 100%)
  const thresholdLine = document.getElementById('threshold-line');
  if (thresholdLine) {
    thresholdLine.style.left = `${Math.round(threshold * 100)}%`;
    thresholdLine.title = `Decision threshold: ${(threshold * 100).toFixed(1)}%`;
  }

  // Metrics
  const txnDisplayType = TYPE_MAP[txnType.value] || txnType.value;
  resultMetrics.innerHTML = `
    <div class="metric-item">
      <div class="metric-key">Prediction</div>
      <div class="metric-val" style="color: ${isFraud ? 'var(--danger)' : 'var(--accent)'}">
        ${data.prediction_label || (isFraud ? 'Fraud' : 'Legitimate')}
      </div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Fraud Probability</div>
      <div class="metric-val">${(prob * 100).toFixed(2)}%</div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Threshold</div>
      <div class="metric-val">${(threshold * 100).toFixed(1)}%</div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Txn Type</div>
      <div class="metric-val">${txnDisplayType}</div>
    </div>
  `;

  // JSON
  jsonBody.textContent = JSON.stringify(data, null, 2);
}

function showError(msg) {
  resultPlaceholder.style.display = 'none';
  resultContent.style.display = 'none';
  resultError.style.display = 'flex';
  errorMsg.textContent = msg || 'Unknown error. Please try again.';
}

// ─── Detect ───────────────────────────────────────────────
async function runDetection() {
  // Validate
  if (!amount.value || amount.value === '') {
    amount.focus();
    shakeField(amount);
    return;
  }

  const payload = {
    type: TYPE_MAP[txnType.value] || txnType.value,
    amount: parseFloat(amount.value) || 0,
    oldbalanceOrg: parseFloat(oldBalOrig.value) || 0,
    newbalanceOrig: parseFloat(newBalOrig.value) || 0,
    oldbalanceDest: parseFloat(oldBalDest.value) || 0,
    newbalanceDest: parseFloat(newBalDest.value) || 0,
  };

  // Loading state
  detectBtn.classList.add('loading');
  detectBtn.querySelector('.btn-text').textContent = 'Analyzing...';

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    showResult(data);
  } catch (err) {
    const isNetwork = err instanceof TypeError;
    showError(
      isNetwork
        ? 'Cannot reach the API server. It may be waking up (Render free tier — wait 30s and retry).'
        : `API Error: ${err.message}`
    );
  } finally {
    detectBtn.classList.remove('loading');
    detectBtn.querySelector('.btn-text').textContent = 'Run Fraud Detection';
  }
}

detectBtn.addEventListener('click', runDetection);
retryBtn.addEventListener('click', runDetection);

// ─── Copy JSON ────────────────────────────────────────────
copyBtn.addEventListener('click', () => {
  const text = jsonBody.textContent;
  navigator.clipboard.writeText(text).then(() => {
    copyBtn.textContent = 'Copied!';
    setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
  });
});

// ─── Field shake animation ─────────────────────────────────
function shakeField(el) {
  el.style.animation = 'none';
  el.offsetHeight; // reflow
  el.style.animation = 'shake 0.4s ease';
  el.style.borderColor = 'var(--danger)';
  setTimeout(() => {
    el.style.animation = '';
    el.style.borderColor = '';
  }, 600);
}

// Inject shake keyframe
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}`;
document.head.appendChild(shakeStyle);

// ─── Keyboard shortcut: Enter ──────────────────────────────
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    runDetection();
  }
});

// ─── Active nav link highlight on scroll ──────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((link) => {
          link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
        });
      }
    });
  },
  { rootMargin: '-50% 0px -50% 0px' }
);

sections.forEach((s) => observer.observe(s));
