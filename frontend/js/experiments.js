// FraudDetect — Experiments section (embedded in index.html)
// Uses ENV.ARTIFACTS_URL  →  GET /artifacts/

(function () {
  const expSkel    = document.getElementById('exp-skeleton');
  const expErr     = document.getElementById('exp-error');
  const expErrMsg  = document.getElementById('exp-error-msg');
  const expContent = document.getElementById('exp-content');
  const runMeta    = document.getElementById('run-meta');
  const runIdVal   = document.getElementById('run-id-val');
  const runFolderVal = document.getElementById('run-folder-val');
  const metricsGrid  = document.getElementById('metrics-grid');
  const paramsGrid   = document.getElementById('params-grid');
  const paramsToggle = document.getElementById('params-toggle');
  const paramsBody   = document.getElementById('params-body');
  const paramsChev   = document.getElementById('params-chevron');
  const refreshBtn   = document.getElementById('exp-refresh-btn');
  const retryBtn     = document.getElementById('exp-retry-btn');
  const refreshIcon  = document.getElementById('refresh-icon');

  // Plot elements
  const PLOTS = {
    'auc_curve.png':        { img: 'auc-img', skel: 'auc-skel', err: 'auc-err', open: 'auc-open' },
    'confusion_matrix.png': { img: 'cm-img',  skel: 'cm-skel',  err: 'cm-err',  open: 'cm-open'  },
    'pr_auc.png':           { img: 'pr-img',  skel: 'pr-skel',  err: 'pr-err',  open: 'pr-open'  },
  };

  // ── Metric card config ─────────────────────────────────
  const METRIC_DEFS = [
    { key: 'accuracy',  label: 'Accuracy',  fmt: p2, tier: v => v > 0.99 ? 'good' : 'warn' },
    { key: 'precision', label: 'Precision', fmt: p2, tier: v => v > 0.65 ? 'good' : 'warn' },
    { key: 'recall',    label: 'Recall',    fmt: p2, tier: v => v > 0.95 ? 'good' : 'warn' },
    { key: 'f1',        label: 'F1 Score',  fmt: p2, tier: v => v > 0.75 ? 'good' : 'warn' },
    { key: 'roc_auc',   label: 'ROC-AUC',  fmt: p4, tier: v => v > 0.98 ? 'good' : 'warn' },
    { key: 'pr_auc',    label: 'PR-AUC',   fmt: p4, tier: v => v > 0.95 ? 'good' : 'warn' },
  ];

  function p2(v) { return (v * 100).toFixed(2) + '%'; }
  function p4(v) { return (v * 100).toFixed(2) + '%'; }

  // ── UI states ──────────────────────────────────────────
  function showSkel() {
    expSkel.style.display    = 'block';
    expErr.style.display     = 'none';
    expContent.style.display = 'none';
    if (runMeta) runMeta.style.display = 'none';
  }
  function showErr(msg) {
    expSkel.style.display    = 'none';
    expErr.style.display     = 'block';
    expContent.style.display = 'none';
    if (expErrMsg) expErrMsg.textContent = msg;
  }
  function showContent() {
    expSkel.style.display    = 'none';
    expErr.style.display     = 'none';
    expContent.style.display = 'block';
  }

  // ── Render metrics ─────────────────────────────────────
  function renderMetrics(metrics) {
    if (!metricsGrid) return;
    metricsGrid.innerHTML = '';
    METRIC_DEFS.forEach(def => {
      const v = metrics[def.key];
      if (v === undefined) return;
      const tier = def.tier(v);
      const d = document.createElement('div');
      d.className = `metric-card ${tier}`;
      d.innerHTML = `
        <div class="metric-card-key">${def.label}</div>
        <div class="metric-card-val">${def.fmt(v)}</div>
        <div class="metric-card-bar">
          <div class="metric-card-bar-fill" data-pct="${(v*100).toFixed(1)}"></div>
        </div>`;
      metricsGrid.appendChild(d);
    });
    setTimeout(() => {
      document.querySelectorAll('#metrics-grid .metric-card-bar-fill').forEach(el => {
        el.style.width = el.dataset.pct + '%';
      });
    }, 80);
  }

  // ── Render params ──────────────────────────────────────
  function renderParams(params) {
    if (!paramsGrid || !params) return;
    paramsGrid.innerHTML = Object.entries(params)
      .map(([k, v]) => `
        <div class="param-item">
          <span class="param-key">${k}</span>
          <span class="param-val">${v ?? '—'}</span>
        </div>`)
      .join('');
  }

  // ── Render plots ───────────────────────────────────────
  function renderPlots(charts) {
    charts.forEach(chart => {
      const ids = PLOTS[chart.name];
      if (!ids) return;
      const img  = document.getElementById(ids.img);
      const skel = document.getElementById(ids.skel);
      const err  = document.getElementById(ids.err);
      const open = document.getElementById(ids.open);
      if (!img) return;

      if (open) { open.href = chart.url; }

      img.onload = () => {
        if (skel) skel.style.display = 'none';
        img.style.display = 'block';
      };
      img.onerror = () => {
        if (skel) skel.style.display = 'none';
        if (err)  err.style.display  = 'block';
      };
      img.src = chart.url;
    });
  }

  // ── Params toggle ──────────────────────────────────────
  if (paramsToggle && paramsBody) {
    paramsToggle.addEventListener('click', () => {
      const open = paramsBody.style.display !== 'none';
      paramsBody.style.display = open ? 'none' : 'block';
      if (paramsChev) paramsChev.textContent = open ? '▾' : '▴';
    });
  }

  // ── Main fetch ─────────────────────────────────────────
  async function load() {
    showSkel();
    if (refreshIcon) refreshIcon.style.animation = 'spin 0.6s linear infinite';

    try {
      const res = await fetch(ENV.ARTIFACTS_URL, {
        headers: { 'accept': 'application/json' },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();

      // Run meta
      if (runMeta) {
        runMeta.style.display = 'flex';
        if (runIdVal)     runIdVal.textContent     = data.latest_run || '—';
        if (runFolderVal) runFolderVal.textContent = data.latest_run || '—';
      }

      renderMetrics(data.metrics);
      renderParams(data.params || null);
      renderPlots(data.charts || []);

      showContent();
    } catch (err) {
      showErr(`${err.message} — make sure backend is at ${ENV.API_BASE_URL} with CORS enabled.`);
    } finally {
      if (refreshIcon) refreshIcon.style.animation = '';
    }
  }

  if (refreshBtn) refreshBtn.addEventListener('click', load);
  if (retryBtn)   retryBtn.addEventListener('click',   load);

  load();
})();
