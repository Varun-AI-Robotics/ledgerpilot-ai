import { useEffect, useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";

import Dashboard from "./pages/Dashboard";
import Reconciliation from "./pages/Reconciliation";
import Exceptions from "./pages/Exceptions";
import AIAssistant from "./pages/AIAssistant";

import { getMetrics } from "./services/api";

function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [metrics, setMetrics] = useState({
    total: 0,
    matched: 0,
    partial: 0,
    exceptions: 0,
    match_rate: 0,
    unreconciled_amount: 0,
  });
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState(false);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      setApiError(false);

      const data = await getMetrics();
      setMetrics(data);
    } catch (error) {
      console.error("Failed to load metrics:", error);
      setApiError(true);
    } finally {
      setLoading(false);
    }
  };

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard metrics={metrics} />;

      case "reconciliation":
        return <Reconciliation />;

      case "exceptions":
        return <Exceptions />;

      case "assistant":
        return <AIAssistant />;

      default:
        return <Dashboard metrics={metrics} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#f7f8fa]">
      <div className="mobile-sidebar">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />
      </div>

      <main className="ml-64 min-h-screen mobile-main">
        <Header activePage={activePage} />

        <div className="p-4 sm:p-6 lg:p-8">
          {apiError && (
            <div className="mb-5 flex items-center justify-between gap-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              <span>
                Backend connection unavailable. Start FastAPI on
                http://127.0.0.1:8000 and refresh.
              </span>

              <button
                onClick={loadMetrics}
                className="shrink-0 rounded-lg bg-red-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-700"
              >
                Retry
              </button>
            </div>
          )}

          {loading && activePage === "dashboard" ? (
            <div className="flex min-h-[60vh] items-center justify-center">
              <div className="text-center">
                <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-2 border-gray-200 border-t-[#111315]" />
                <p className="text-sm text-gray-500">
                  Loading finance operations...
                </p>
              </div>
            </div>
          ) : (
            renderPage()
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
