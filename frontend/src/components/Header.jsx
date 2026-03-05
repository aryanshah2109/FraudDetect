import { useState, useEffect } from 'react';
import { checkHealth } from '../services/fraudApi';

export default function Header() {
  const [online, setOnline] = useState(null);

  useEffect(() => {
    const check = async () => {
      try {
        await checkHealth();
        setOnline(true);
      } catch {
        setOnline(false);
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="border-b border-border bg-surface/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative w-8 h-8">
            <svg viewBox="0 0 32 32" fill="none" className="w-full h-full">
              <polygon points="16,2 30,9 30,23 16,30 2,23 2,9" 
                stroke="#00d4ff" strokeWidth="1.5" fill="rgba(0,212,255,0.08)" />
              <polygon points="16,8 24,12 24,20 16,24 8,20 8,12" 
                stroke="#00d4ff" strokeWidth="1" fill="rgba(0,212,255,0.04)" />
              <circle cx="16" cy="16" r="3" fill="#00d4ff" />
            </svg>
          </div>
          <div>
            <span className="font-display font-800 text-lg tracking-tight text-text-primary">
              Fraud<span className="text-accent">Detect</span>
            </span>
            <div className="text-[10px] font-mono text-text-muted tracking-widest uppercase">
              ML Intelligence v1.0
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="hidden md:flex items-center gap-6">
          {['Dashboard', 'Predict', 'Docs'].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="font-mono text-xs uppercase tracking-widest text-text-secondary hover:text-accent transition-colors"
            >
              {item}
            </a>
          ))}
        </nav>

        {/* API Status */}
        <div className="flex items-center gap-2">
          <div className="relative flex items-center justify-center w-3 h-3">
            {online === true && (
              <>
                <span className="absolute w-3 h-3 rounded-full bg-safe opacity-40 ping-accent" />
                <span className="w-2 h-2 rounded-full bg-safe block" />
              </>
            )}
            {online === false && (
              <span className="w-2 h-2 rounded-full bg-danger block" />
            )}
            {online === null && (
              <span className="w-2 h-2 rounded-full bg-warn block animate-pulse" />
            )}
          </div>
          <span className="font-mono text-[11px] text-text-secondary">
            {online === true ? 'API Online' : online === false ? 'API Offline' : 'Connecting...'}
          </span>
        </div>
      </div>
    </header>
  );
}
