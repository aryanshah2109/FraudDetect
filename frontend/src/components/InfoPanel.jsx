const STEPS = [
  {
    num: '01',
    title: 'Input Transaction',
    desc: 'Provide the transaction type, amount, and sender/receiver balances before and after.',
  },
  {
    num: '02',
    title: 'Feature Engineering',
    desc: 'Balance error features are auto-calculated: |amount − balance_delta| for origin and destination.',
  },
  {
    num: '03',
    title: 'XGBoost Inference',
    desc: 'CUDA-accelerated gradient boosting classifier scores the transaction probability.',
  },
  {
    num: '04',
    title: 'Threshold Decision',
    desc: 'Optimized threshold (≥65% precision) converts probability to Fraud / Legitimate verdict.',
  },
];

const EXAMPLE_PAYLOAD = `{
  "type": "TRANSFER",
  "amount": 100000,
  "oldbalanceOrg": 50000,
  "newbalanceOrig": 0,
  "oldbalanceDest": 10000,
  "newbalanceDest": 110000
}`;

export default function InfoPanel() {
  return (
    <div className="space-y-4">
      {/* How It Works */}
      <div className="panel p-5">
        <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-4">
          How It Works
        </div>
        <div className="space-y-4">
          {STEPS.map((step, i) => (
            <div key={step.num} className="flex gap-3">
              <div className="font-mono text-[11px] text-accent font-bold shrink-0 mt-0.5">
                {step.num}
              </div>
              <div>
                <div className="font-display font-600 text-sm text-text-primary mb-0.5">
                  {step.title}
                </div>
                <div className="font-mono text-[11px] text-text-secondary leading-relaxed">
                  {step.desc}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Example cURL */}
      <div className="panel p-5">
        <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3">
          Example API Call
        </div>
        <div className="text-[10px] font-mono text-text-secondary mb-2">
          POST {import.meta.env.VITE_API_URL}/predict/
        </div>
        <pre className="bg-void rounded border border-border p-3 font-mono text-[11px] text-safe overflow-x-auto leading-relaxed">
          {EXAMPLE_PAYLOAD}
        </pre>
        <div className="mt-3 text-[10px] font-mono text-text-muted">
          Expected response:
        </div>
        <pre className="bg-void rounded border border-border p-3 font-mono text-[11px] text-warn overflow-x-auto leading-relaxed mt-1">
{`{
  "prediction": 1,
  "prediction_label": "Fraud",
  "fraud_probability": 0.87
}`}
        </pre>
      </div>

      {/* Model info */}
      <div className="panel p-5">
        <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-3">
          Model Configuration
        </div>
        <div className="space-y-1.5">
          {[
            ['Estimators', '263'],
            ['Max Depth', '11'],
            ['Learning Rate', '0.0816'],
            ['Subsample', '0.5564'],
            ['Col Sample', '0.5639'],
            ['Scale PosWeight', '7.45'],
            ['Objective', 'binary:logistic'],
            ['Device', 'cuda (CUDA)'],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between">
              <span className="font-mono text-[11px] text-text-muted">{k}</span>
              <span className="font-mono text-[11px] text-text-secondary">{v}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
