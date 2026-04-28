export default function AdvisoryCard({ 
  advisory, 
  bestMandi, 
  bestDay, 
  priceRange, 
  estimatedEarnings, 
  crop,
  dataFreshness 
}) {
  const isLive = dataFreshness?.status === "live"

  const formatUpdated = (iso) => {
    if (!iso) return ""
    try {
      const d = new Date(iso)
      return d.toLocaleString("en-IN", {
        day: "2-digit", month: "short", year: "numeric",
        hour: "2-digit", minute: "2-digit", hour12: true
      })
    } catch {
      return iso
    }
  }

  return (
    <div className="kr-card advisory-accent">
      <div className="p-5">
        <div className="flex items-center gap-2 mb-4">
          <span className="badge-green">{crop}</span>
          <span className="badge-amber">✨ AI Advisory</span>
        </div>
        
        <p className="text-[17px] leading-[1.8] text-brand-text mb-6">
          {advisory}
        </p>

        <div className="flex gap-2">
          <div className="metric-chip">
            <span className="text-[10px] uppercase font-bold text-brand-muted tracking-wider">
              🏪 Best Market
            </span>
            <span className="text-sm font-bold text-brand-text mt-1">
              {bestMandi}
            </span>
          </div>

          <div className="metric-chip">
            <span className="text-[10px] uppercase font-bold text-brand-muted tracking-wider">
              📅 Sell On
            </span>
            <span className="text-sm font-bold text-brand-text mt-1">
              {bestDay}
            </span>
          </div>

          <div className="metric-chip bg-green-50 border-green-100">
            <span className="text-[10px] uppercase font-bold text-brand-green tracking-wider">
              💰 Est. Earnings
            </span>
            <span className="text-sm font-bold text-brand-green mt-1">
              {estimatedEarnings}
            </span>
          </div>
        </div>

        {/* Data freshness badge */}
        {dataFreshness && (
          <p
            className="mt-3"
            style={{
              fontSize: "11px",
              color: isLive ? "#16a34a" : "#d97706",
              lineHeight: 1.4,
            }}
          >
            {isLive
              ? `🟢 Live data · Updated ${formatUpdated(dataFreshness.last_updated)} · Source: data.gov.in`
              : "🟡 Using cached data · Live update pending"}
          </p>
        )}
      </div>
    </div>
  )
}
