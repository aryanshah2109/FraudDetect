const stats = [
  {
    label: 'Model',
    value: 'XGBoost',
    sub: '263 estimators',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
      </svg>
    ),
  },
  {
    label: 'Min Precision',
    value: '≥ 65%',
    sub: 'Configurable threshold',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 8v4l3 3" />
      </svg>
    ),
  },
  {
    label: 'Latency',
    value: '<100ms',
    sub: 'Per prediction',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
      </svg>
    ),
  },
  {
    label: 'GPU',
    value: 'CUDA',
    sub: 'Accelerated inference',
    icon: (
      <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <rect x="4" y="6" width="16" height="12" rx="2" />
        <path d="M8 6V4M12 6V4M16 6V4M8 20v-2M12 20v-2M16 20v-2" />
      </svg>
    ),
  },
];

export default function StatsBar() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {stats.map((s) => (
        <div key={s.label} className="panel p-4 flex items-start gap-3">
          <div className="text-accent mt-0.5 shrink-0">{s.icon}</div>
          <div>
            <div className="font-mono text-[10px] uppercase tracking-widest text-text-muted mb-1">
              {s.label}
            </div>
            <div className="font-display font-700 text-text-primary text-lg leading-tight">
              {s.value}
            </div>
            <div className="font-mono text-[10px] text-text-secondary mt-0.5">{s.sub}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
