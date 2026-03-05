import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import './styles/index.css';

export default function App() {
  return (
    <div className="min-h-screen bg-void grid-bg">
      <Header />
      <Dashboard />
    </div>
  );
}
