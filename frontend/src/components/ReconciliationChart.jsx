import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function ReconciliationChart({ metrics }) {
  const data = [
    {
      name: "Matched",
      value: metrics?.matched || 0,
    },
    {
      name: "Partial",
      value: metrics?.partial || 0,
    },
    {
      name: "Exceptions",
      value: metrics?.exceptions || 0,
    },
  ];

  const COLORS = [
    "#10b981",
    "#f59e0b",
    "#ef4444",
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 h-[360px]">
      <div className="mb-3">
        <h3 className="font-bold text-gray-900">
          Reconciliation Health
        </h3>

        <p className="text-xs text-gray-400 mt-1">
          Current transaction distribution
        </p>
      </div>

      <div className="h-[270px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={70}
              outerRadius={105}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell
                  key={entry.name}
                  fill={COLORS[index]}
                />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default ReconciliationChart;