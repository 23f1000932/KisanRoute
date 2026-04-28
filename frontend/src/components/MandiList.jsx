export default function MandiList({ mandis }) {
  if (!mandis || mandis.length === 0) return null

  const ranks = ['🥇', '🥈', '🥉']

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'rising': return 'trend-rising'
      case 'stable': return 'trend-stable'
      case 'falling': return 'trend-falling'
      default: return 'text-brand-muted'
    }
  }

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'rising': return '↑'
      case 'stable': return '→'
      case 'falling': return '↓'
      default: return '•'
    }
  }

  return (
    <div className="mt-4">
      <h3 className="text-lg font-heading font-bold text-brand-text mb-3 px-1">
        Nearby Markets — Price Comparison
      </h3>
      
      <div className="mandi-scroll pb-2">
        {mandis.map((mandi, idx) => (
          <div 
            key={idx} 
            className={`mandi-card ${idx === 0 ? 'border-2 border-brand-green bg-green-50/30' : ''}`}
          >
            <div className="flex justify-between items-start mb-1">
              <div>
                <h4 className="font-bold text-brand-text leading-tight">{mandi.name}</h4>
                <p className="text-xs text-brand-muted">{mandi.state}</p>
              </div>
              <span className="text-xl" title={`Rank #${idx + 1}`}>{ranks[idx] || `#${idx+1}`}</span>
            </div>

            <div className="my-1">
              <span className="text-2xl font-bold text-brand-green">
                ₹{mandi.avg_price}
              </span>
              <span className="text-xs text-brand-muted ml-1">/kg avg</span>
            </div>

            <div className="flex flex-col gap-1.5 mt-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-brand-muted text-xs">Trend:</span>
                <span className={`capitalize ${getTrendColor(mandi.trend)}`}>
                  {getTrendIcon(mandi.trend)} {mandi.trend}
                </span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-brand-muted text-xs">Best day:</span>
                <span className="font-medium">{mandi.best_day}</span>
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-brand-muted text-xs">Distance:</span>
                <span className="font-medium">~{mandi.distance_km} km</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
