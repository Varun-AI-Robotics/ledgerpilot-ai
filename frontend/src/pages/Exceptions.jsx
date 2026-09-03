import {
  AlertTriangle,
  Sparkles,
  Search,
  Loader2,
  Brain,
  ShieldAlert,
} from "lucide-react";

import { useEffect, useState } from "react";

import {
  getExceptions,
  investigatePayment,
} from "../services/api";

function Exceptions() {
  const [exceptions, setExceptions] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadExceptions();
  }, []);

  const loadExceptions = async () => {
    try {
      const result = await getExceptions();
      setExceptions(result);
    } catch (error) {
      console.error(error);
    }
  };

  const investigate = async (paymentId) => {
    setLoading(true);
    setSelected(paymentId);
    setAnalysis(null);

    try {
      const result = await investigatePayment(paymentId);
      setAnalysis(result);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const filtered = exceptions.filter((item) =>
    item.payment_id
      ?.toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="fade-in space-y-5">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-red-50 flex items-center justify-center">
            <ShieldAlert
              size={18}
              className="text-red-600"
            />
          </div>

          <h1 className="text-2xl font-bold text-gray-900">
            Exception Center
          </h1>
        </div>

        <p className="text-sm text-gray-500 mt-2">
          Investigate financial discrepancies with AI-assisted analysis.
        </p>
      </div>

      {/* Search */}
      <div className="bg-white border border-gray-200 rounded-2xl p-4">
        <div className="flex items-center gap-3">
          <Search size={17} className="text-gray-400" />

          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search payment ID..."
            className="outline-none text-sm w-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-[1.25fr_0.75fr] gap-5">
        {/* Exceptions */}
        <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold text-gray-900">
                  Unresolved Exceptions
                </h2>

                <p className="text-xs text-gray-400 mt-1">
                  {filtered.length} records require attention
                </p>
              </div>

              <span className="px-2.5 py-1 rounded-lg bg-red-50 text-red-600 text-xs font-bold">
                {filtered.length}
              </span>
            </div>
          </div>

          <div className="divide-y divide-gray-100">
            {filtered.map((item) => (
              <div
                key={item.payment_id}
                className={`
                  p-5
                  transition
                  ${
                    selected === item.payment_id
                      ? "bg-gray-50"
                      : "hover:bg-gray-50"
                  }
                `}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <AlertTriangle
                        size={15}
                        className="text-red-500"
                      />

                      <span className="font-bold text-sm text-gray-900">
                        {item.payment_id}
                      </span>
                    </div>

                    <p className="text-sm text-gray-600 mt-2">
                      {item.reason}
                    </p>

                    <div className="flex gap-6 mt-4 text-xs">
                      <div>
                        <p className="text-gray-400">
                          Payment
                        </p>

                        <p className="font-semibold mt-1">
                          ₹{Number(
                            item.payment_amount || 0
                          ).toLocaleString()}
                        </p>
                      </div>

                      <div>
                        <p className="text-gray-400">
                          Settlement
                        </p>

                        <p className="font-semibold mt-1">
                          ₹{Number(
                            item.settlement_amount || 0
                          ).toLocaleString()}
                        </p>
                      </div>

                      <div>
                        <p className="text-gray-400">
                          Difference
                        </p>

                        <p className="font-semibold text-red-600 mt-1">
                          ₹{Number(
                            item.amount_difference || 0
                          ).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() =>
                      investigate(item.payment_id)
                    }
                    className="shrink-0 flex items-center gap-2 px-3 py-2 rounded-xl bg-[#111315] text-white text-xs font-semibold hover:bg-black transition"
                  >
                    <Sparkles size={14} />
                    Investigate
                  </button>
                </div>
              </div>
            ))}

            {filtered.length === 0 && (
              <div className="py-16 text-center text-gray-400">
                No exceptions found.
              </div>
            )}
          </div>
        </div>

        {/* AI panel */}
        <div className="bg-[#111315] rounded-2xl text-white overflow-hidden min-h-[500px]">
          <div className="p-6 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center">
                <Brain
                  size={20}
                  className="text-[#111315]"
                />
              </div>

              <div>
                <h2 className="font-bold">
                  AI Investigation
                </h2>

                <p className="text-xs text-gray-500 mt-1">
                  Gemini-powered analysis
                </p>
              </div>
            </div>
          </div>

          <div className="p-6">
            {!selected && !loading && (
              <div className="h-[380px] flex flex-col items-center justify-center text-center">
                <Sparkles
                  size={30}
                  className="text-gray-500 mb-4"
                />

                <h3 className="font-semibold">
                  Select an exception
                </h3>

                <p className="text-xs text-gray-500 mt-2 max-w-xs">
                  Choose an exception from the list to let
                  LedgerPilot investigate the discrepancy.
                </p>
              </div>
            )}

            {loading && (
              <div className="h-[380px] flex flex-col items-center justify-center">
                <Loader2
                  size={30}
                  className="animate-spin mb-4"
                />

                <p className="font-semibold">
                  Investigating exception...
                </p>

                <p className="text-xs text-gray-500 mt-2">
                  Gemini is analyzing the supplied evidence.
                </p>
              </div>
            )}

            {analysis && !loading && (
              <div className="slide-up space-y-6">
                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-500">
                    Classification
                  </p>

                  <p className="text-lg font-bold mt-2">
                    {analysis.classification}
                  </p>
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-2">
                    <span className="text-gray-400">
                      Confidence
                    </span>

                    <span className="font-bold">
                      {Math.round(
                        analysis.confidence * 100
                      )}%
                    </span>
                  </div>

                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-white rounded-full"
                      style={{
                        width: `${analysis.confidence * 100}%`,
                      }}
                    />
                  </div>
                </div>

                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-500">
                    Reason
                  </p>

                  <p className="text-sm leading-6 text-gray-300 mt-2">
                    {analysis.reason}
                  </p>
                </div>

                <div>
                  <p className="text-[10px] uppercase tracking-widest text-gray-500">
                    Recommended Action
                  </p>

                  <p className="text-sm leading-6 text-gray-300 mt-2">
                    {analysis.recommended_action}
                  </p>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-white/10">
                  <span className="text-xs text-gray-500">
                    Priority
                  </span>

                  <span className="px-3 py-1 rounded-lg bg-red-500/10 text-red-400 text-xs font-bold">
                    {analysis.priority}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Exceptions;