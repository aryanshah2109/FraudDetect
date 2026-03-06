import HeroSection from '../components/HeroSection';
import StatsBar from '../components/StatsBar';
import PredictionForm from '../components/PredictionForm';
import ResultCard from '../components/ResultCard';
import InfoPanel from '../components/InfoPanel';
import ErrorBoundary from '../components/ErrorBoundary';
import { usePrediction } from '../hooks/usePrediction';

export default function Dashboard() {
  const {
    form,
    result,
    loading,
    error,
    isFraud,
    probability,
    updateField,
    fillForm,
    submit,
    reset,
  } = usePrediction();

  return (
    <main className="max-w-7xl mx-auto px-6 py-10">
      {/* Hero */}
      <section id="dashboard">
        <HeroSection />
      </section>

      {/* Stats */}
      <StatsBar />

      {/* Main prediction layout */}
      <section id="predict">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Form + Result */}
          <div className="lg:col-span-2 space-y-6">
            <PredictionForm
              form={form}
              loading={loading}
              error={error}
              updateField={updateField}
              fillForm={fillForm}
              submit={submit}
              reset={reset}
            />

            {/* Result panel — mutually exclusive states, wrapped in error boundary */}
            <ErrorBoundary>
            {loading ? (
              <div className="panel p-8 flex flex-col items-center justify-center text-center">
                <div className="w-12 h-12 rounded-full border-2 border-accent/20 border-t-accent animate-spin mb-4" />
                <p className="font-display font-600 text-text-primary mb-1">Analyzing Transaction</p>
                <p className="font-mono text-xs text-text-secondary">
                  Running XGBoost inference...
                </p>
              </div>
            ) : result ? (
              <ResultCard
                result={result}
                isFraud={isFraud}
                probability={probability}
              />
            ) : (
              <div className="panel p-8 flex flex-col items-center justify-center text-center border-dashed">
                <div className="w-12 h-12 rounded-full bg-accent/5 border border-accent/20 flex items-center justify-center mb-3">
                  <svg className="w-6 h-6 text-accent/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <p className="font-mono text-xs text-text-muted">
                  Results will appear here after analysis
                </p>
              </div>
            )}
            </ErrorBoundary>
          </div>

          {/* Right: Info panels */}
          <div className="lg:col-span-1" id="docs">
            <InfoPanel />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-16 pt-8 border-t border-border flex items-center justify-between">
        <div className="font-mono text-[11px] text-text-muted">
          FraudDetect v1.0.0 — MIT License
        </div>
        <div className="font-mono text-[11px] text-text-muted">
          Backend: <span className="text-accent">{import.meta.env.VITE_API_URL}</span>
        </div>
      </footer>
    </main>
  );
}
