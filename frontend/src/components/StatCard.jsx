function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  danger = false,
}) {
  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-5 card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-gray-500">
            {title}
          </p>

          <h3 className="text-3xl font-bold tracking-tight text-gray-900 mt-2">
            {value}
          </h3>

          {subtitle && (
            <p className="text-xs text-gray-400 mt-2">
              {subtitle}
            </p>
          )}
        </div>

        {Icon && (
          <div
            className={`
              w-10
              h-10
              rounded-xl
              flex
              items-center
              justify-center
              ${
                danger
                  ? "bg-red-50 text-red-600"
                  : "bg-gray-100 text-gray-700"
              }
            `}
          >
            <Icon size={19} />
          </div>
        )}
      </div>

      {trend && (
        <div className="mt-4 flex items-center gap-2">
          <span
            className={`
              text-[11px]
              font-semibold
              px-2
              py-1
              rounded-lg
              ${
                danger
                  ? "bg-red-50 text-red-600"
                  : "bg-emerald-50 text-emerald-600"
              }
            `}
          >
            {trend}
          </span>

          <span className="text-[11px] text-gray-400">
            vs previous run
          </span>
        </div>
      )}
    </div>
  );
}

export default StatCard;