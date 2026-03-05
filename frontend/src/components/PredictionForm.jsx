const TRANSACTION_TYPES = ['CASH IN', 'CASH OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'];

const FIELDS = [
  { key: 'amount',         label: 'Transaction Amount',      placeholder: '100000.00', hint: 'Total value of the transaction' },
  { key: 'oldbalanceOrg',  label: 'Sender Balance (Before)', placeholder: '50000.00',  hint: "Sender's account balance before the transaction" },
  { key: 'newbalanceOrig', label: 'Sender Balance (After)',  placeholder: '0.00',      hint: "Sender's account balance after the transaction" },
  { key: 'oldbalanceDest', label: 'Receiver Balance (Before)', placeholder: '10000.00', hint: "Receiver's account balance before the transaction" },
  { key: 'newbalanceDest', label: 'Receiver Balance (After)',  placeholder: '110000.00', hint: "Receiver's account balance after the transaction" },
];

const TEST_CASES = [
  {
    label: 'Test Legitimate',
    color: '#00e5a0',
    borderColor: 'rgba(0,229,160,0.3)',
    bgColor: 'rgba(0,229,160,0.06)',
    icon: '🟩',
    data: {
      type: 'TRANSFER',
      amount: 2000,
      oldbalanceOrg: 10000,
      newbalanceOrig: 8000,
      oldbalanceDest: 5000,
      newbalanceDest: 7000,
    },
  },
  {
    label: 'Test Fraud',
    color: '#ff3d5a',
    borderColor: 'rgba(255,61,90,0.3)',
    bgColor: 'rgba(255,61,90,0.06)',
    icon: '🟥',
    data: {
      type: 'TRANSFER',
      amount: 1000000,
      oldbalanceOrg: 1000000,
      newbalanceOrig: 0,
      oldbalanceDest: 0,
      newbalanceDest: 0,
    },
  },
  {
    label: 'Test Edge Case',
    color: '#ffaa00',
    borderColor: 'rgba(255,170,0,0.3)',
    bgColor: 'rgba(255,170,0,0.06)',
    icon: '🟨',
    data: {
      type: 'CASH OUT',
      amount: 75000,
      oldbalanceOrg: 75432,
      newbalanceOrig: 432,
      oldbalanceDest: 120000,
      newbalanceDest: 194500,
    },
  },
];

function LoadingDots() {
  return (
    <span className="inline-flex gap-1 items-center">
      {[0, 1, 2].map((i) => (
        <span key={i} className="w-1.5 h-1.5 rounded-full bg-void animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
      ))}
    </span>
  );
}

export default function PredictionForm({ form, loading, error, updateField, fillForm, submit, reset }) {
  return (
    <div className="panel scanline">
      {/* Header */}
      <div className="border-b border-border px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="font-display font-700 text-text-primary">Transaction Analysis</h2>
          <p className="font-mono text-[11px] text-text-secondary mt-0.5">
            Enter transaction details or use a test preset
          </p>
        </div>
        <div className="tag text-text-muted border-border">POST /predict/</div>
      </div>

      {/* Quick Test Buttons */}
      <div className="px-6 pt-5 pb-0">
        <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-2">Quick Test Presets</div>
        <div className="flex gap-2 flex-wrap">
          {TEST_CASES.map((tc) => (
            <button
              key={tc.label}
              type="button"
              onClick={() => fillForm(tc.data)}
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-2 rounded-md font-mono text-[11px] uppercase tracking-wider transition-all hover:scale-105 active:scale-95 disabled:opacity-40"
              style={{
                color: tc.color,
                border: `1px solid ${tc.borderColor}`,
                background: tc.bgColor,
              }}
            >
              <span>{tc.icon}</span>
              {tc.label}
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={submit} className="p-6 space-y-5">
        {/* Transaction Type */}
        <div>
          <label className="label-text">Transaction Type</label>
          <select
            value={form.type}
            onChange={(e) => updateField('type', e.target.value)}
            className="input-field appearance-none"
            required
          >
            {TRANSACTION_TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        {/* Numeric Fields */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {FIELDS.map(({ key, label, placeholder, hint }) => (
            <div key={key}>
              <label className="label-text">{label}</label>
              <input
                type="number"
                step="0.01"
                min="0"
                placeholder={placeholder}
                value={form[key]}
                onChange={(e) => updateField(key, e.target.value)}
                className="input-field"
                required
              />
              <p className="font-mono text-[10px] text-text-muted mt-1">{hint}</p>
            </div>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div className="border border-danger/30 bg-danger/5 rounded-md px-4 py-3 flex items-start gap-3">
            <svg className="w-4 h-4 text-danger shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" /><path d="M12 8v4M12 16h.01" />
            </svg>
            <p className="font-mono text-xs text-danger leading-relaxed">{error}</p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3 pt-2">
          <button type="submit" disabled={loading} className="btn-primary flex-1 flex items-center justify-center gap-2">
            {loading ? (
              <>Analyzing <LoadingDots /></>
            ) : (
              <>
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                </svg>
                Run Fraud Detection
              </>
            )}
          </button>
          <button
            type="button"
            onClick={reset}
            className="px-4 py-3 rounded-md border border-border text-text-secondary hover:border-accent/40 hover:text-accent transition-all font-mono text-xs uppercase tracking-wider"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}
