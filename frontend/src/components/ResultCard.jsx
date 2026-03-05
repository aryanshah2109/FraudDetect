import { useState } from 'react';

// Risk classification matching backend thresholds exactly
function getRisk(probability) {
  if (probability >= 0.8)  return { level: 'CRITICAL', color: '#ff3d5a', bg: 'rgba(255,61,90,0.12)', border: 'rgba(255,61,90,0.35)', emoji: '🟥' };
  if (probability >= 0.4)  return { level: 'HIGH',     color: '#ff7a00', bg: 'rgba(255,122,0,0.12)',  border: 'rgba(255,122,0,0.35)',  emoji: '🟧' };
  if (probability >= 0.15) return { level: 'MEDIUM',   color: '#ffaa00', bg: 'rgba(255,170,0,0.12)', border: 'rgba(255,170,0,0.35)', emoji: '🟨' };
  return                          { level: 'LOW',      color: '#00e5a0', bg: 'rgba(0,229,160,0.12)', border: 'rgba(0,229,160,0.35)', emoji: '🟩' };
}

function ProbabilityBar({ value, risk }) {
  const pct = Math.round(value * 100);
  // Gradient zones: green → yellow → orange → red
  const barGradient = `linear-gradient(90deg, #00e5a0 0%, #ffaa00 40%, #ff7a00 70%, #ff3d5a 100%)`;

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="font-mono text-[11px] uppercase tracking-widest text-text-secondary">Fraud Probability</span>
        <span className="font-mono text-2xl font-bold" style={{ color: risk.color }}>{pct}%</span>
      </div>

      {/* Segmented threshold bar */}
      <div className="relative h-3 bg-void rounded-full overflow-hidden border border-border">
        {/* Full spectrum background */}
        <div className="absolute inset-0 opacity-15 rounded-full" style={{ background: barGradient }} />
        {/* Filled portion */}
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${pct}%`, background: barGradient, clipPath: 'inset(0)' }}
        />
        {/* Threshold tick marks */}
        {[15, 40, 80].map((tick) => (
          <div
            key={tick}
            className="absolute top-0 bottom-0 w-px bg-void/60"
            style={{ left: `${tick}%` }}
          />
        ))}
      </div>

      {/* Threshold labels */}
      <div className="relative h-4">
        {[
          { pct: 0,   label: 'LOW',      color: '#00e5a0' },
          { pct: 15,  label: 'MEDIUM',   color: '#ffaa00' },
          { pct: 40,  label: 'HIGH',     color: '#ff7a00' },
          { pct: 80,  label: 'CRITICAL', color: '#ff3d5a' },
        ].map(({ pct: p, label, color }) => (
          <span
            key={label}
            className="absolute font-mono text-[9px] uppercase tracking-wider transform -translate-x-1/2"
            style={{ left: `${p === 0 ? 4 : p}%`, color }}
          >
            {label}
          </span>
        ))}
      </div>
    </div>
  );
}

function MetricRow({ label, value, highlight }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-border last:border-0">
      <span className="font-mono text-xs text-text-secondary">{label}</span>
      <span className="font-mono text-xs font-bold" style={{ color: highlight || '#e8f0fe' }}>{value}</span>
    </div>
  );
}

function RiskFactors({ factors }) {
  if (!factors || factors.length === 0) return null;
  return (
    <div>
      <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3">
        Risk Factors Detected
      </div>
      <div className="space-y-2">
        {factors.map((factor, i) => (
          <div
            key={i}
            className="flex items-start gap-2.5 px-3 py-2.5 rounded-md border"
            style={{ borderColor: 'rgba(255,61,90,0.2)', background: 'rgba(255,61,90,0.05)' }}
          >
            <svg className="w-3.5 h-3.5 text-danger shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <span className="font-mono text-[11px] text-text-primary leading-relaxed">{factor}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ThresholdBadge({ threshold }) {
  if (threshold == null) return null;
  const pct = (threshold * 100).toFixed(1);
  return (
    <div className="flex items-center justify-between px-3 py-2 rounded-md border border-border bg-void">
      <div className="flex items-center gap-2">
        <svg className="w-3.5 h-3.5 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <polyline points="8 8 12 4 16 8"/><polyline points="16 16 12 20 8 16"/>
        </svg>
        <span className="font-mono text-[11px] text-text-secondary uppercase tracking-wider">Decision Threshold</span>
      </div>
      <span className="font-mono text-sm font-bold text-accent">{pct}%</span>
    </div>
  );
}

function BalanceChart({ input, isFraud }) {
  const bars = [
    { label: 'Sender\nBefore', value: input.oldbalanceOrg },
    { label: 'Sender\nAfter',  value: input.newbalanceOrig },
    { label: 'Recv\nBefore',   value: input.oldbalanceDest },
    { label: 'Recv\nAfter',    value: input.newbalanceDest },
  ];
  const maxVal = Math.max(...bars.map((b) => b.value), 1);
  return (
    <div>
      <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3">Balance Visualization</div>
      <div className="flex items-end gap-2 h-24">
        {bars.map((bar, i) => {
          const heightPct = (bar.value / maxVal) * 100;
          const isAfter = i % 2 === 1;
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1 h-full justify-end">
              <div
                className="w-full rounded-t-sm transition-all duration-700"
                style={{
                  height: `${Math.max(heightPct, 3)}%`,
                  minHeight: '3px',
                  background: isAfter
                    ? isFraud ? 'rgba(255,61,90,0.6)' : 'rgba(0,229,160,0.6)'
                    : 'rgba(0,212,255,0.35)',
                }}
              />
              <div className="font-mono text-[9px] text-text-muted text-center leading-tight whitespace-pre-line">{bar.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function RawResponse({ result }) {
  const { input, ...apiResult } = result;
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between font-mono text-[11px] text-text-muted hover:text-accent transition-colors py-1"
      >
        <span className="uppercase tracking-widest">Raw API Response</span>
        <span className="text-[10px]">{open ? '▲ hide' : '▼ show'}</span>
      </button>
      {open && (
        <pre className="mt-2 p-4 bg-void rounded-md border border-border font-mono text-[11px] text-safe overflow-x-auto leading-relaxed">
          {JSON.stringify(apiResult, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default function ResultCard({ result, isFraud, probability }) {
  if (!result) return null;

  const { input } = result;
  const risk = getRisk(probability);
  const pct = Math.round(probability * 100);
  const balanceDelta = Math.abs(input.amount - (input.oldbalanceOrg - input.newbalanceOrig));

  // Safely extract new API fields
  const riskFactors = Array.isArray(result.risk_factors) ? result.risk_factors : [];
  const threshold = result.threshold ?? null;

  return (
    <div
      className="result-appear panel"
      style={{ boxShadow: `0 0 0 1px ${risk.border}, 0 0 28px ${risk.bg}` }}
    >
      {/* Verdict Banner */}
      <div
        className="px-6 py-5 border-b border-border flex items-center justify-between"
        style={{ background: `linear-gradient(135deg, ${risk.bg}, transparent)` }}
      >
        <div className="flex items-center gap-3">
          {/* Icon */}
          <div className="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
            style={{ background: risk.bg, border: `1px solid ${risk.border}` }}>
            {isFraud ? (
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke={risk.color} strokeWidth="2.5">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            ) : (
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke={risk.color} strokeWidth="2.5">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <polyline points="9 12 11 14 15 10"/>
              </svg>
            )}
          </div>

          <div>
            <div className="font-display font-800 text-xl tracking-tight" style={{ color: risk.color }}>
              {isFraud ? 'FRAUD DETECTED' : 'LEGITIMATE'}
            </div>
            <div className="font-mono text-[11px] text-text-secondary">
              Fraud probability: {pct}%
            </div>
          </div>
        </div>

        {/* Risk Badge */}
        <div
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md font-mono text-xs font-bold uppercase tracking-wider hidden sm:flex"
          style={{ color: risk.color, border: `1px solid ${risk.border}`, background: risk.bg }}
        >
          <span>{risk.emoji}</span>
          {risk.level} RISK
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Probability Bar with threshold zones */}
        <ProbabilityBar value={probability} risk={risk} />

        {/* Decision Threshold */}
        <ThresholdBadge threshold={threshold} />

        {/* Risk Factors — only shown if present */}
        {riskFactors.length > 0 && <RiskFactors factors={riskFactors} />}

        {/* Transaction Summary */}
        <div>
          <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3">Transaction Summary</div>
          <div className="panel p-4">
            <MetricRow label="Type"   value={input.type}  highlight="#00d4ff" />
            <MetricRow
              label="Amount"
              value={`$${input.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
            />
            <MetricRow
              label="Sender Δ Balance"
              value={`$${(input.oldbalanceOrg - input.newbalanceOrig).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
              highlight={Math.abs(input.oldbalanceOrg - input.newbalanceOrig - input.amount) > 1 ? '#ffaa00' : undefined}
            />
            <MetricRow
              label="Receiver Δ Balance"
              value={`$${(input.newbalanceDest - input.oldbalanceDest).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
            />
            <MetricRow
              label="Balance Error"
              value={`$${balanceDelta.toFixed(2)}`}
              highlight={balanceDelta > 100 ? '#ff7a00' : '#00e5a0'}
            />
          </div>
        </div>

        {/* Balance Chart */}
        <BalanceChart input={input} isFraud={isFraud} />

        {/* Raw JSON */}
        <RawResponse result={result} />
      </div>
    </div>
  );
}
