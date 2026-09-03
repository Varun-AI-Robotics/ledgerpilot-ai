import {
  LayoutDashboard,
  RefreshCcw,
  AlertTriangle,
  Bot,
  ShieldCheck,
  ChevronRight,
  Activity,
} from "lucide-react";

function Sidebar({ activePage, setActivePage }) {
  const menu = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      id: "reconciliation",
      label: "Reconciliation",
      icon: RefreshCcw,
    },
    {
      id: "exceptions",
      label: "Exceptions",
      icon: AlertTriangle,
    },
    {
      id: "assistant",
      label: "AI Assistant",
      icon: Bot,
    },
  ];

  return (
    <aside className="fixed left-0 top-0 bottom-0 z-30 w-64 bg-[#111315] text-white">
      {/* Logo */}
      <div className="h-20 px-6 flex items-center border-b border-white/10">
        <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center mr-3">
          <ShieldCheck size={21} className="text-[#111315]" />
        </div>

        <div>
          <h1 className="font-bold text-lg tracking-tight">
            LedgerPilot
          </h1>

          <p className="text-[11px] text-gray-400">
            AI Finance Controller
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="px-4 py-6">
        <p className="px-3 mb-3 text-[10px] uppercase tracking-[0.18em] text-gray-500 font-semibold">
          Workspace
        </p>

        <div className="space-y-1">
          {menu.map((item) => {
            const Icon = item.icon;
            const active = activePage === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`
                  group
                  w-full
                  flex
                  items-center
                  gap-3
                  px-3
                  py-3
                  rounded-xl
                  text-sm
                  transition-all
                  ${
                    active
                      ? "bg-white text-[#111315] shadow-lg"
                      : "text-gray-400 hover:bg-white/5 hover:text-white"
                  }
                `}
              >
                <Icon size={18} />

                <span className="flex-1 text-left">
                  {item.label}
                </span>

                {active && (
                  <ChevronRight size={15} />
                )}
              </button>
            );
          })}
        </div>
      </nav>

      {/* AI status */}
      <div className="absolute left-4 right-4 bottom-24">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />

            <span className="text-xs font-semibold">
              AI Engine Active
            </span>
          </div>

          <p className="text-[11px] leading-5 text-gray-500">
            Gemini-powered exception analysis is ready.
          </p>
        </div>
      </div>

      {/* System */}
      <div className="absolute bottom-5 left-4 right-4">
        <div className="flex items-center gap-2 px-3">
          <Activity size={14} className="text-emerald-400" />

          <span className="text-xs text-gray-500">
            All systems operational
          </span>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;