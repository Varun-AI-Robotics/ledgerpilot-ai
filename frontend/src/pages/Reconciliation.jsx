import {
  RefreshCcw,
  Search,
  CheckCircle2,
  AlertTriangle,
  Clock3,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import { useEffect, useState } from "react";

import { getReconciliation } from "../services/api";


function Reconciliation() {

  const [data, setData] = useState([]);

  const [search, setSearch] = useState("");

  const [page, setPage] = useState(1);

  const [total, setTotal] = useState(0);

  const [pages, setPages] = useState(1);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  const limit = 100;


  // ==========================================
  // Load reconciliation data
  // ==========================================

  const loadData = async (
    selectedPage = page,
    selectedSearch = search
  ) => {

    try {

      setLoading(true);
      setError("");

      const result = await getReconciliation(
        selectedPage,
        limit,
        selectedSearch
      );


      // New paginated API response
      setData(result.data || []);

      setTotal(result.total || 0);

      setPage(result.page || selectedPage);

      setPages(result.pages || 1);

    } catch (error) {

      console.error(
        "Failed to load reconciliation:",
        error
      );

      setError(
        "Unable to load reconciliation records."
      );

      setData([]);

    } finally {

      setLoading(false);

    }
  };


  // ==========================================
  // Initial load
  // ==========================================

  useEffect(() => {

    loadData(1, "");

  }, []);


  // ==========================================
  // Search
  // ==========================================

  const handleSearch = (e) => {

    const value = e.target.value;

    setSearch(value);

    setPage(1);

    loadData(1, value);
  };


  // ==========================================
  // Previous page
  // ==========================================

  const handlePrevious = () => {

    if (page > 1) {

      const newPage = page - 1;

      setPage(newPage);

      loadData(newPage, search);
    }
  };


  // ==========================================
  // Next page
  // ==========================================

  const handleNext = () => {

    if (page < pages) {

      const newPage = page + 1;

      setPage(newPage);

      loadData(newPage, search);
    }
  };


  return (

    <div className="fade-in space-y-5">


      {/* ======================================
          Header
      ====================================== */}

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">

        <div>

          <h1 className="text-2xl font-bold text-gray-900">
            Reconciliation
          </h1>

          <p className="text-sm text-gray-500 mt-1">
            Review every payment reconciliation result.
          </p>

        </div>


        <button
          onClick={() => loadData(page, search)}
          disabled={loading}
          className="flex items-center justify-center gap-2 px-4 py-2.5 bg-[#111315] text-white rounded-xl text-sm font-medium hover:bg-black transition disabled:opacity-50"
        >

          <RefreshCcw
            size={15}
            className={
              loading
                ? "animate-spin"
                : ""
            }
          />

          {loading ? "Loading..." : "Refresh"}

        </button>

      </div>


      {/* ======================================
          Search
      ====================================== */}

      <div className="bg-white border border-gray-200 rounded-2xl p-4">

        <div className="flex items-center gap-3">

          <Search
            size={17}
            className="text-gray-400"
          />

          <input
            value={search}
            onChange={handleSearch}
            placeholder="Search payment ID..."
            className="outline-none w-full text-sm text-gray-800"
          />

        </div>

      </div>


      {/* ======================================
          Error
      ====================================== */}

      {error && (

        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">

          {error}

        </div>

      )}


      {/* ======================================
          Record information
      ====================================== */}

      {!loading && !error && (

        <div className="flex items-center justify-between text-sm text-gray-500">

          <span>

            Showing{" "}

            <strong className="text-gray-900">
              {data.length}
            </strong>{" "}

            of{" "}

            <strong className="text-gray-900">
              {total.toLocaleString()}
            </strong>{" "}

            records

          </span>


          <span>

            Page{" "}

            <strong className="text-gray-900">
              {page}
            </strong>{" "}

            of{" "}

            <strong className="text-gray-900">
              {pages}
            </strong>

          </span>

        </div>

      )}


      {/* ======================================
          Table
      ====================================== */}

      <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">

        <div className="overflow-x-auto">

          <table className="w-full text-sm">

            <thead>

              <tr className="border-b border-gray-100 bg-gray-50/70">

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Payment
                </th>

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Payment Amount
                </th>

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Settlement
                </th>

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Bank
                </th>

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Status
                </th>

                <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500">
                  Reason
                </th>

              </tr>

            </thead>


            <tbody>

              {loading ? (

                <tr>

                  <td
                    colSpan="6"
                    className="text-center py-16"
                  >

                    <div className="flex flex-col items-center">

                      <div className="h-8 w-8 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin mb-3" />

                      <p className="text-sm text-gray-400">
                        Loading reconciliation...
                      </p>

                    </div>

                  </td>

                </tr>

              ) : data.length > 0 ? (

                data.map((item) => (

                  <tr
                    key={item.payment_id}
                    className="border-b border-gray-100 hover:bg-gray-50 transition"
                  >

                    <td className="px-6 py-4 font-semibold text-gray-900">
                      {item.payment_id}
                    </td>


                    <td className="px-6 py-4">

                      ₹
                      {Number(
                        item.payment_amount || 0
                      ).toLocaleString("en-IN", {
                        maximumFractionDigits: 2,
                      })}

                    </td>


                    <td className="px-6 py-4">

                      ₹
                      {Number(
                        item.settlement_amount || 0
                      ).toLocaleString("en-IN", {
                        maximumFractionDigits: 2,
                      })}

                    </td>


                    <td className="px-6 py-4">

                      ₹
                      {Number(
                        item.bank_amount || 0
                      ).toLocaleString("en-IN", {
                        maximumFractionDigits: 2,
                      })}

                    </td>


                    <td className="px-6 py-4">

                      <StatusBadge
                        status={item.status}
                      />

                    </td>


                    <td className="px-6 py-4 text-gray-500 max-w-xs">

                      <div className="truncate max-w-[300px]">

                        {item.reason || "—"}

                      </div>

                    </td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td
                    colSpan="6"
                    className="text-center py-16 text-gray-400"
                  >

                    No reconciliation records found.

                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>


        {/* ======================================
            Pagination
        ====================================== */}

        {!loading && total > 0 && (

          <div className="flex items-center justify-between border-t border-gray-100 px-5 py-4">

            <p className="text-xs text-gray-500">

              {search
                ? `Search results for "${search}"`
                : "All reconciliation records"}

            </p>


            <div className="flex items-center gap-2">

              <button
                onClick={handlePrevious}
                disabled={page <= 1 || loading}
                className="flex items-center gap-1 px-3 py-2 rounded-lg border border-gray-200 text-xs font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
              >

                <ChevronLeft size={14} />

                Previous

              </button>


              <span className="px-3 text-xs font-semibold text-gray-700">

                {page} / {pages}

              </span>


              <button
                onClick={handleNext}
                disabled={page >= pages || loading}
                className="flex items-center gap-1 px-3 py-2 rounded-lg border border-gray-200 text-xs font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
              >

                Next

                <ChevronRight size={14} />

              </button>

            </div>

          </div>

        )}

      </div>

    </div>
  );
}


// ==========================================
// Status Badge
// ==========================================

function StatusBadge({ status }) {

  const normalized = status?.toUpperCase();


  if (normalized === "MATCHED") {

    return (

      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-semibold">

        <CheckCircle2 size={13} />

        Matched

      </span>

    );

  }


  if (normalized === "PARTIAL") {

    return (

      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-50 text-amber-700 text-xs font-semibold">

        <Clock3 size={13} />

        Partial

      </span>

    );

  }


  return (

    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-red-50 text-red-700 text-xs font-semibold">

      <AlertTriangle size={13} />

      Exception

    </span>

  );
}


export default Reconciliation;