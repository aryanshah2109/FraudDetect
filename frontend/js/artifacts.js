// FraudDetect — Artifacts Page JS
// Reads API URL from JS/env.js  →  ENV.ARTIFACTS_URL  (GET /artifacts/)

// ── DOM refs ────────────────────────────────────────────
const artLoading  = document.getElementById('art-loading');
const artError    = document.getElementById('art-error');
const artContent  = document.getElementById('art-content');
const artErrorMsg = document.getElementById('art-error-msg');
const runIdEl     = document.getElementById('run-id');
const metricsGrid = document.getElementById('metrics-grid');
const cmTableWrap = document.getElementById('cm-table-wrap');
const chartsGrid  = document.getElementById('charts-grid');
const tcCallout   = document.getElementById('threshold-callout');
const refreshBtn  = document.getElementById('refresh-btn');
const retryBtn    = document.getElementById('art-retry-btn');

// ── Metric definitions ──────────────────────────────────
const METRIC_DEFS = [
  { key: 'accuracy', label: 'Accuracy',  fmt: p4,
    tier: v => v > 0.99 ? 'good' : v > 0.95 ? 'warn' : 'danger',
    note: 'Overall correct predictions' },
  { key: 'precision', label: 'Precision', fmt: p2,
    tier: v => v > 0.65 ? 'good' : v > 0.5 ? 'warn' : 'danger',
    note: 'Of all fraud flags, how many were real' },
  { key: 'recall', label: 'Recall', fmt: p2,
    tier: v => v > 0.95 ? 'good' : v > 0.8 ? 'warn' : 'danger',
    note: 'Fraction of actual fraud caught' },
  { key: 'f1', label: 'F1 Score', fmt: p2,
    tier: v => v > 0.75 ? 'good' : v > 0.6 ? 'warn' : 'danger',
    note: 'Harmonic mean of precision & recall' },
  { key: 'roc_auc', label: 'ROC-AUC', fmt: p4,
    tier: v => v > 0.98 ? 'good' : v > 0.9 ? 'warn' : 'danger',
    note: 'Area under ROC curve' },
  { key: 'pr_auc', label: 'PR-AUC', fmt: p4,
    tier: v => v > 0.95 ? 'good' : v > 0.85 ? 'warn' : 'danger',
    note: 'Primary metric for imbalanced datasets' },
];

// ── Chart titles ────────────────────────────────────────
const CHART_META = {
  'auc_curve.png':        { title: 'ROC-AUC Curve',         badge: 'ROC' },
  'confusion_matrix.png': { title: 'Confusion Matrix Plot',  badge: 'CM'  },
  'pr_auc.png':           { title: 'Precision-Recall Curve', badge: 'PR'  },
};

// ── Formatters ──────────────────────────────────────────
function p4(v) { return (v * 100).toFixed(2) + '%'; }
function p2(v) { return (v * 100).toFixed(2) + '%'; }
function fmtN(n) {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(2) + 'M';
  if (n >= 1_000)     return n.toLocaleString();
  return String(n);
}

// ── UI states ───────────────────────────────────────────
function showLoading() {
  artLoading.style.display = 'flex';
  artError.style.display   = 'none';
  artContent.style.display = 'none';
}
function showError(msg) {
  artLoading.style.display = 'none';
  artError.style.display   = 'flex';
  artContent.style.display = 'none';
  artErrorMsg.textContent  = msg;
}
function showContent() {
  artLoading.style.display = 'none';
  artError.style.display   = 'none';
  artContent.style.display = 'block';
}

// ── Render metrics ──────────────────────────────────────
function renderMetrics(metrics) {
  metricsGrid.innerHTML = '';
  METRIC_DEFS.forEach(def => {
    const v = metrics[def.key];
    if (v === undefined) return;
    const tier = def.tier(v);
    const card = document.createElement('div');
    card.className = `metric-card ${tier}`;
    card.innerHTML = `
      <div class="metric-card-key">${def.label}</div>
      <div class="metric-card-val">${def.fmt(v)}</div>
      <div class="metric-card-note">${def.note}</div>
      <div class="metric-card-bar">
        <div class="metric-card-bar-fill" data-pct="${(v*100).toFixed(1)}"></div>
      </div>`;
    metricsGrid.appendChild(card);
  });
  setTimeout(() => {
    document.querySelectorAll('.metric-card-bar-fill').forEach(el => {
      el.style.width = el.dataset.pct + '%';
    });
  }, 80);
}

// ── Render confusion matrix ──────────────────────────────
// API sends: [[TN, FP], [FN, TP]]
function renderCM(cm) {
  const TN = cm[0][0], FP = cm[0][1], FN = cm[1][0], TP = cm[1][1];
  cmTableWrap.innerHTML = `
    <table class="cm-table">
      <tr>
        <td></td><td></td>
        <td class="cm-header-cell" colspan="2">Predicted</td>
      </tr>
      <tr>
        <td></td><td></td>
        <td class="cm-header-cell">Legit (0)</td>
        <td class="cm-header-cell">Fraud (1)</td>
      </tr>
      <tr>
        <td class="cm-axis-label row-label"
            rowspan="2"
            style="writing-mode:vertical-rl;transform:rotate(180deg);
                   padding-right:10px;color:var(--text-muted);
                   font-size:11px;letter-spacing:.8px;
                   text-transform:uppercase;font-family:var(--mono)">
          Actual
        </td>
        <td class="cm-header-cell" style="padding-right:10px;text-align:right">Legit (0)</td>
        <td class="cm-cell tn">
          <div class="cm-cell-inner">
            <span class="cm-cell-val">${fmtN(TN)}</span>
            <span class="cm-cell-label">TN</span>
          </div>
        </td>
        <td class="cm-cell fp">
          <div class="cm-cell-inner">
            <span class="cm-cell-val">${fmtN(FP)}</span>
            <span class="cm-cell-label">FP</span>
          </div>
        </td>
      </tr>
      <tr>
        <td class="cm-header-cell" style="padding-right:10px;text-align:right">Fraud (1)</td>
        <td class="cm-cell fn">
          <div class="cm-cell-inner">
            <span class="cm-cell-val">${fmtN(FN)}</span>
            <span class="cm-cell-label">FN</span>
          </div>
        </td>
        <td class="cm-cell tp">
          <div class="cm-cell-inner">
            <span class="cm-cell-val">${fmtN(TP)}</span>
            <span class="cm-cell-label">TP</span>
          </div>
        </td>
      </tr>
    </table>`;
}

// ── Render charts ─────────────────────────────────────────
function renderCharts(charts) {
  chartsGrid.innerHTML = '';
  charts.forEach(chart => {
    const meta = CHART_META[chart.name] || { title: chart.name, badge: 'IMG' };
    const card = document.createElement('div');
    card.className = 'chart-card';
    card.innerHTML = `
      <div class="chart-card-header">
        <span class="chart-card-title">${meta.title}</span>
        <span class="chart-card-badge">${meta.badge}</span>
      </div>
      <div class="chart-img-wrap">
        <img class="chart-img" src="${chart.url}" alt="${meta.title}" loading="lazy"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
        <div class="chart-img-placeholder" style="display:none">
          <span class="chart-img-placeholder-icon">🖼</span>
          <span class="chart-img-placeholder-text">Image unavailable</span>
        </div>
        <a class="chart-expand-btn" href="${chart.url}" target="_blank" title="Open full size">⤢</a>
      </div>`;
    const img = card.querySelector('.chart-img');
    img.addEventListener('click', () => openLightbox(chart.url, meta.title));
    img.style.cursor = 'zoom-in';
    chartsGrid.appendChild(card);
  });
}

// ── Lightbox ─────────────────────────────────────────────
let lightbox = null;
function buildLightbox() {
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = `
    <div class="lightbox-inner">
      <img class="lightbox-img" id="lb-img" src="" alt="" />
    </div>
    <button class="lightbox-close" id="lb-close">✕</button>`;
  document.body.appendChild(lb);
  lb.addEventListener('click', e => { if (e.target === lb || e.target.id === 'lb-close') closeLightbox(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });
  return lb;
}
function openLightbox(src, alt) {
  if (!lightbox) lightbox = buildLightbox();
  lightbox.querySelector('#lb-img').src = src;
  lightbox.querySelector('#lb-img').alt = alt;
  lightbox.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLightbox() {
  if (!lightbox) return;
  lightbox.classList.remove('open');
  document.body.style.overflow = '';
}

// ── Threshold callout ─────────────────────────────────────
function renderThresholdCallout(metrics) {
  tcCallout.innerHTML = `
    <div class="tc-icon">⚖️</div>
    <div class="tc-body">
      <div class="tc-title">Threshold Optimization Strategy</div>
      <div class="tc-desc">
        Threshold selected on the validation set under a hard constraint of
        <strong>Precision ≥ 65%</strong>. Within that constraint the threshold
        maximising Recall was chosen. Fallback to F1 if constraint unmet.
      </div>
    </div>
    <div class="tc-metrics">
      <div class="tc-metric">
        <span class="tc-metric-val">${(metrics.threshold * 100).toFixed(4)}%</span>
        <span class="tc-metric-label">Threshold</span>
      </div>
      <div class="tc-metric">
        <span class="tc-metric-val">${(metrics.precision * 100).toFixed(2)}%</span>
        <span class="tc-metric-label">Precision</span>
      </div>
      <div class="tc-metric">
        <span class="tc-metric-val">${(metrics.recall * 100).toFixed(2)}%</span>
        <span class="tc-metric-label">Recall</span>
      </div>
    </div>`;
}

// ── Fetch & render ────────────────────────────────────────
async function loadArtifacts() {
  showLoading();
  refreshBtn.classList.add('spinning');

  try {
    const res = await fetch(ENV.ARTIFACTS_URL, {
      headers: { 'accept': 'application/json' },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);

    const data = await res.json();

    runIdEl.textContent = data.latest_run || '—';

    renderMetrics(data.metrics);

    if (Array.isArray(data.metrics.confusion_matrix)) {
      renderCM(data.metrics.confusion_matrix);
    }

    renderCharts(data.charts || []);
    renderThresholdCallout(data.metrics);

    showContent();
  } catch (err) {
    showError(
      `${err.message}. ` +
      `Make sure the backend is running at ${ENV.API_BASE_URL} and CORS is enabled.`
    );
  } finally {
    refreshBtn.classList.remove('spinning');
  }
}

refreshBtn.addEventListener('click', loadArtifacts);
retryBtn.addEventListener('click',   loadArtifacts);

loadArtifacts();
