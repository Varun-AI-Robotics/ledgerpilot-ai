import {
  CreditCard,
  CheckCircle2,
  AlertTriangle,
  Clock3,
  ArrowUpRight,
  ShieldCheck,
} from "lucide-react";

import StatCard from "../components/StatCard";
import ReconciliationChart from "../components/ReconciliationChart";

function Dashboard({ metrics }) {
  const matchRate = metrics?.match_rate ?? 0;
  const total = metrics?.total ?? 0;
  const matched = metrics?.matched ?? 0;
  const partial = metrics?.partial ?? 0;
  const exceptions = metrics?.exceptions ?? 0;

  return (
    <div className="fade-in space-y-6">
      {/* Hero */}
      <section className="bg-[#111315] rounded-3xl p-7 text-white relative overflow-hidden">
        <div className="absolute -right-16 -top-16 w-52 h-52 rounded-full bg-white/5" />

        <div className="absolute right-20 bottom-[-70px] w-48 h-48 rounded-full bg-white/5" />

        <div className="relative">
          <div className="flex items-center gap-2 text-gray-400 text-xs mb-3">
            <SparkIcon />

            <span>
              AUTONOMOUS FINANCE CONTROL
            </span>
          </div>

          <h1 className="text-3xl font-bold tracking-tight">
            Financial operations,
            <br />
            under control.
          </h1>

          <p className="text-gray-400 text-sm mt-3 max-w-lg">
            LedgerPilot continuously reconciles payments,
            settlements and bank transactions while AI
            investigates the exceptions that need attention.
          </p>
        </div>
      </section>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard
          title="Total Transactions"
          value={total.toLocaleString()}
          subtitle="Processed by reconciliation engine"
          icon={CreditCard}
        />

        <StatCard
          title="Match Rate"
          value={`${Number(matchRate).toFixed(1)}%`}
          subtitle="Successfully reconciled"
          icon={CheckCircle2}
          trend="+2.4%"
        />

        <StatCard
          title="Partial Matches"
          value={partial}
          subtitle="Require additional verification"
          icon={Clock3}
        />

        <StatCard
          title="Exceptions"
          value={exceptions}
          subtitle="Require investigation"
          icon={AlertTriangle}
          danger={exceptions > 0}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
        <ReconciliationChart metrics={metrics} />

        <div className="bg-white border border-gray-200 rounded-2xl p-6">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-bold text-gray-900">
                Control Health
              </h3>

              <p className="text-xs text-gray-400 mt-1">
                Automated financial controls
              </p>
            </div>

            <ShieldCheck
              size={20}
              className="text-emerald-500"
            />
          </div>

          <div className="mt-6 space-y-5">
            <HealthRow
              label="Payment Integrity"
              value="Healthy"
              percentage={98}
            />

            <HealthRow
              label="Settlement Matching"
              value="Healthy"
              percentage={94}
            />

            <HealthRow
              label="Bank Reconciliation"
              value="Healthy"
              percentage={96}
            />

            <HealthRow
              label="Exception Detection"
              value="Active"
              percentage={100}
            />
          </div>
        </div>
      </div>

      {/* Bottom insight */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-gray-900">
              Finance Operations Summary
            </h3>

            <p className="text-xs text-gray-400 mt-1">
              Latest reconciliation cycle
            </p>
          </div>

          <ArrowUpRight size={18} />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-7">
          <MiniMetric
            label="Matched"
            value={matched}
            positive
          />

          <MiniMetric
            label="Partial"
            value={partial}
          />

          <MiniMetric
            label="Exceptions"
            value={exceptions}
            negative
          />

          <MiniMetric
            label="Unreconciled"
            value={metrics?.unreconciled_amount ?? 0}
            money
          />
        </div>
      </div>
    </div>
  );
}

function HealthRow({ label, value, percentage }) {
  return (
    <div>
      <div className="flex justify-between mb-2">
        <span className="text-sm text-gray-700">
          {label}
        </span>

        <span className="text-xs font-semibold text-emerald-600">
          {value}
        </span>
      </div>

      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500 rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

function MiniMetric({
  label,
  value,
  positive,
  negative,
  money,
}) {
  return (
    <div>
      <p className="text-xs text-gray-400">
        {label}
      </p>

      <p
        className={`
          text-xl
          font-bold
          mt-1
          ${
            positive
              ? "text-emerald-600"
              : negative
                ? "text-red-600"
                : "text-gray-900"
          }
        `}
      >
        {money ? `₹${Number(value).toLocaleString()}` : value}
      </p>
    </div>
  );
}

function SparkIcon() {
  return (
    <div className="w-5 h-5 rounded-md bg-white/10 flex items-center justify-center">
      ✦
    </div>
  );
}

export default Dashboard;