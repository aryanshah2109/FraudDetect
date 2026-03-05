const USE_CASES = [
  {
    icon: '🏦',
    title: 'Banking Transfers',
    desc: 'Detect suspicious large-value TRANSFER and CASH_OUT transactions in real time.',
  },
  {
    icon: '🛒',
    title: 'E-commerce Payments',
    desc: 'Flag fraudulent PAYMENT transactions before they complete checkout.',
  },
  {
    icon: '💳',
    title: 'Debit Card Abuse',
    desc: 'Identify anomalous DEBIT patterns that deviate from account history.',
  },
  {
    icon: '🔍',
    title: 'Balance Manipulation',
    desc: 'Catch transactions where balance changes don\'t match reported amounts.',
  },
];

export default function HeroSection() {
  return (
    <div className="mb-10">
      {/* Title Block */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-3">
          <span className="tag text-accent border-accent/30 bg-accent/5">ML-Powered</span>
          <span className="tag text-text-muted border-border">Real-Time</span>
          <span className="tag text-text-muted border-border">XGBoost</span>
        </div>
        <h1 className="font-display font-800 text-4xl md:text-5xl text-text-primary leading-tight mb-3">
          Credit Card Fraud<br />
          <span className="text-accent">Intelligence System</span>
        </h1>
        <p className="text-text-secondary font-mono text-sm leading-relaxed max-w-2xl">
          FraudDetect is a production-grade ML system that analyzes financial transaction 
          patterns in real time — flagging fraud with sub-100ms latency using an XGBoost 
          classifier trained on millions of transactions with precision-constrained 
          threshold optimization.
        </p>
      </div>

      {/* Use Cases */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {USE_CASES.map((uc) => (
          <div
            key={uc.title}
            className="panel p-4 hover:border-accent/30 transition-colors cursor-default"
          >
            <div className="text-2xl mb-2">{uc.icon}</div>
            <div className="font-display font-600 text-sm text-text-primary mb-1">{uc.title}</div>
            <div className="font-mono text-[11px] text-text-secondary leading-relaxed">{uc.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
