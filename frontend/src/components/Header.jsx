import {
  Bell,
  Search,
  Sparkles,
} from "lucide-react";

function Header({ activePage }) {
  const titles = {
    dashboard: {
      title: "Financial Overview",
      subtitle: "Monitor your reconciliation operations",
    },
    reconciliation: {
      title: "Reconciliation",
      subtitle: "Review payment and settlement matching",
    },
    exceptions: {
      title: "Exception Center",
      subtitle: "Investigate unresolved financial discrepancies",
    },
    assistant: {
      title: "AI Finance Assistant",
      subtitle: "Ask LedgerPilot about your financial operations",
    },
  };

  const page = titles[activePage] || titles.dashboard;

  return (
    <header className="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-8">
      <div>
        <h2 className="text-xl font-bold text-gray-900">
          {page.title}
        </h2>

        <p className="text-xs text-gray-500 mt-1">
          {page.subtitle}
        </p>
      </div>

      <div className="flex items-center gap-4">
        {/* Search */}
        <div className="hidden lg:flex items-center w-56 h-10 rounded-xl bg-gray-50 border border-gray-200 px-3">
          <Search size={16} className="text-gray-400" />

          <input
            placeholder="Search..."
            className="bg-transparent outline-none text-sm px-2 w-full"
          />
        </div>

        {/* AI status */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-gray-50 border border-gray-200">
          <Sparkles size={15} />

          <span className="text-xs font-medium text-gray-700">
            AI Online
          </span>

          <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
        </div>

        {/* Notification */}
        <button className="w-10 h-10 rounded-xl border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition">
          <Bell size={17} className="text-gray-600" />
        </button>

        {/* Profile */}
        <div className="w-10 h-10 rounded-xl bg-[#111315] text-white flex items-center justify-center text-sm font-bold">
          V
        </div>
      </div>
    </header>
  );
}

export default Header;