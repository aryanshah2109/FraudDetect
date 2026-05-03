// FraudDetect — Detection Page JS
// Reads API base URL from JS/env.js  →  ENV.PREDICT_URL

// ─── DOM refs ─────────────────────────────────────────────
const $ = (id) => document.getElementById(id);

const detectBtn         = $('detect-btn');
const resetBtn          = $('reset-btn');
const retryBtn          = $('retry-btn');
const copyBtn           = $('copy-btn');
const resultPlaceholder = $('result-placeholder');
const resultContent     = $('result-content');
const resultError       = $('result-error');
const resultVerdict     = $('result-verdict');
const probValue         = $('prob-value');
const probBar           = $('prob-bar');
const resultMetrics     = $('result-metrics');
const riskFactorsWrap   = $('risk-factors-wrap');
const riskFactorsList   = $('risk-factors-list');
const jsonBody          = $('json-body');
const errorMsg          = $('error-msg');

// Form fields
const txnType    = $('txn-type');
const amount     = $('amount');
const oldBalOrig = $('old-bal-orig');
const newBalOrig = $('new-bal-orig');
const oldBalDest = $('old-bal-dest');
const newBalDest = $('new-bal-dest');

// ─── Type mapping: select value → API string ──────────────
const TYPE_API_MAP = {
  TRANSFER: 'TRANSFER',
  CASH_OUT: 'CASH OUT',
  PAYMENT:  'PAYMENT',
  CASH_IN:  'CASH IN',
  DEBIT:    'DEBIT',
};

// ─── Presets ─────────────────────────────────────────────
const PRESETS = {
  fraud: {
    type: 'TRANSFER', amount: 1000000,
    oldbalanceOrg: 1000000, newbalanceOrig: 0,
    oldbalanceDest: 0, newbalanceDest: 1000000,
  },
  legit: {
    type: 'PAYMENT', amount: 5000,
    oldbalanceOrg: 80000, newbalanceOrig: 75000,
    oldbalanceDest: 20000, newbalanceDest: 25000,
  },
  cashout: {
    type: 'CASH_OUT', amount: 500000,
    oldbalanceOrg: 500000, newbalanceOrig: 0,
    oldbalanceDest: 10000, newbalanceDest: 510000,
  },
};

document.querySelectorAll('.preset-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const p = PRESETS[btn.dataset.preset];
    if (!p) return;
    txnType.value    = p.type;
    amount.value     = p.amount;
    oldBalOrig.value = p.oldbalanceOrg;
    newBalOrig.value = p.newbalanceOrig;
    oldBalDest.value = p.oldbalanceDest;
    newBalDest.value = p.newbalanceDest;
  });
});

// ─── Reset ───────────────────────────────────────────────
resetBtn.addEventListener('click', () => {
  txnType.value = 'TRANSFER';
  [amount, oldBalOrig, newBalOrig, oldBalDest, newBalDest].forEach(f => f.value = '');
  showPlaceholder();
});

// ─── UI States ───────────────────────────────────────────
function showPlaceholder() {
  resultPlaceholder.style.display = 'flex';
  resultContent.style.display     = 'none';
  resultError.style.display       = 'none';
}

function showError(msg) {
  resultPlaceholder.style.display = 'none';
  resultContent.style.display     = 'none';
  resultError.style.display       = 'flex';
  errorMsg.textContent            = msg || 'Unknown error.';
}

// ─── Render result ────────────────────────────────────────
function showResult(data) {
  resultPlaceholder.style.display = 'none';
  resultContent.style.display     = 'block';
  resultError.style.display       = 'none';

  const isFraud   = data.prediction === 1;
  const prob      = data.fraud_probability ?? 0;
  const probPct   = Math.round(prob * 100);
  const threshold = data.threshold ?? 0;

  // Verdict
  resultVerdict.className = `result-verdict ${isFraud ? 'fraud' : 'legit'}`;
  resultVerdict.innerHTML = `
    <span class="verdict-icon">${isFraud ? '⚠️' : '✅'}</span>
    <div class="verdict-body">
      <div class="verdict-label">${isFraud ? 'FRAUD DETECTED' : 'LEGITIMATE'}</div>
      <div class="verdict-sub">${isFraud
        ? 'This transaction appears fraudulent'
        : 'No fraud indicators found'}</div>
    </div>
    <span class="verdict-tag">${isFraud ? 'ALERT' : 'SAFE'}</span>
  `;

  // Probability bar
  probValue.textContent = `${probPct}%`;
  probBar.className     = `prob-bar-fill ${isFraud ? 'danger' : 'safe'}`;
  setTimeout(() => { probBar.style.width = `${probPct}%`; }, 50);

  // Threshold marker
  const tLine = $('threshold-line');
  if (tLine) {
    const pct = Math.min(Math.max(threshold * 100, 0), 100);
    tLine.style.left = `${pct.toFixed(2)}%`;
    tLine.title      = `Decision threshold: ${(threshold * 100).toFixed(4)}%`;
  }

  // Key metrics
  const txnDisplay = TYPE_API_MAP[txnType.value] || txnType.value;
  resultMetrics.innerHTML = `
    <div class="metric-item">
      <div class="metric-key">Prediction</div>
      <div class="metric-val" style="color:${isFraud ? 'var(--danger)' : 'var(--accent)'}">
        ${data.prediction_label || (isFraud ? 'Fraud' : 'Legitimate')}
      </div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Fraud Probability</div>
      <div class="metric-val">${(prob * 100).toFixed(2)}%</div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Threshold</div>
      <div class="metric-val">${(threshold * 100).toFixed(4)}%</div>
    </div>
    <div class="metric-item">
      <div class="metric-key">Txn Type</div>
      <div class="metric-val">${txnDisplay}</div>
    </div>
  `;

  // Risk Factors
  const factors = data.risk_factors;
  if (factors && Array.isArray(factors) && factors.length > 0) {
    riskFactorsWrap.style.display = 'block';
    riskFactorsList.innerHTML = factors.map(f => `
      <div class="risk-factor-item">
        <span class="risk-bullet"></span>
        <span class="risk-factor-text">${f}</span>
      </div>`).join('');
  } else {
    riskFactorsWrap.style.display = 'none';
  }

  // JSON preview
  jsonBody.textContent = JSON.stringify(data, null, 2);
}

// ─── Detection call ───────────────────────────────────────
async function runDetection() {
  if (!amount.value) { shakeField(amount); amount.focus(); return; }

  const payload = {
    type:           TYPE_API_MAP[txnType.value] || txnType.value,
    amount:         parseFloat(amount.value)     || 0,
    oldbalanceOrg:  parseFloat(oldBalOrig.value) || 0,
    newbalanceOrig: parseFloat(newBalOrig.value) || 0,
    oldbalanceDest: parseFloat(oldBalDest.value) || 0,
    newbalanceDest: parseFloat(newBalDest.value) || 0,
  };

  detectBtn.classList.add('loading');
  detectBtn.querySelector('.btn-text').textContent = 'Analyzing...';

  try {
    const res = await fetch(ENV.PREDICT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const e = await res.json().catch(() => ({}));
      throw new Error(e.detail || `HTTP ${res.status}`);
    }
    showResult(await res.json());
  } catch (err) {
    showError(err instanceof TypeError
      ? `Cannot reach ${ENV.API_BASE_URL}. Is the backend running?`
      : `API Error: ${err.message}`
    );
  } finally {
    detectBtn.classList.remove('loading');
    detectBtn.querySelector('.btn-text').textContent = 'Run Fraud Detection';
  }
}

detectBtn.addEventListener('click', runDetection);
retryBtn.addEventListener('click',  runDetection);

// ─── Copy JSON ────────────────────────────────────────────
copyBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(jsonBody.textContent).then(() => {
    copyBtn.textContent = 'Copied!';
    setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1500);
  });
});

// ─── Shake ───────────────────────────────────────────────
function shakeField(el) {
  el.style.animation = 'none'; el.offsetHeight;
  el.style.animation = 'shake 0.4s ease';
  el.style.borderColor = 'var(--danger)';
  setTimeout(() => { el.style.animation = ''; el.style.borderColor = ''; }, 600);
}
const ss = document.createElement('style');
ss.textContent = `@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}`;
document.head.appendChild(ss);

// ─── Ctrl+Enter ───────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) runDetection();
});

// ─── Nav scroll highlight ─────────────────────────────────
const navLinks = document.querySelectorAll('.nav-link');
new IntersectionObserver(
  entries => entries.forEach(entry => {
    if (entry.isIntersecting)
      navLinks.forEach(l =>
        l.classList.toggle('active', l.getAttribute('href') === `#${entry.target.id}`)
      );
  }),
  { rootMargin: '-50% 0px -50% 0px' }
).observe(...document.querySelectorAll('section[id]'));
