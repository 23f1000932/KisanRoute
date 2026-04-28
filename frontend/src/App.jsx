import { useState } from 'react'
import { getAdvisory } from './services/api'
import InputForm from './components/InputForm'
import AdvisoryCard from './components/AdvisoryCard'
import MandiList from './components/MandiList'
import VoiceButton from './components/VoiceButton'

function App() {
  const [step, setStep] = useState('input') // 'input' | 'loading' | 'result' | 'error'
  const [result, setResult] = useState(null)
  const [errorMsg, setErrorMsg] = useState(null)

  const handleGetAdvisory = async (formData) => {
    setStep('loading')
    setErrorMsg(null)
    try {
      const data = await getAdvisory(formData)
      setResult(data)
      setStep('result')
    } catch (err) {
      console.error(err)
      setErrorMsg(err.message || "Failed to fetch advisory.")
      setStep('error')
    }
  }

  const handleReset = () => {
    setResult(null)
    setErrorMsg(null)
    setStep('input')
  }

  return (
    <div className="min-h-screen pb-12">
      {/* Header */}
      <header className="hero-gradient text-white py-8 px-4 rounded-b-3xl shadow-md mb-8">
        <div className="max-w-md mx-auto text-center">
          <div className="text-5xl mb-2">🌾</div>
          <h1 className="text-3xl font-heading font-bold mb-1">KisanRoute</h1>
          <p className="text-green-100 font-medium opacity-90 text-sm">
            Right Market. Right Price. Right Time.
          </p>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-md mx-auto px-4">
        {step === 'input' && (
          <div className="animate-fade-in-up">
            <InputForm onSubmit={handleGetAdvisory} />
          </div>
        )}

        {step === 'loading' && (
          <div className="flex flex-col items-center justify-center py-20 animate-fade-in-up">
            <div className="spinner mb-6"></div>
            <p className="text-brand-text font-semibold text-center pulse-glow inline-block rounded-full px-6 py-2 bg-green-50">
              Generating your advisory... <br/> this takes a few seconds
            </p>
          </div>
        )}

        {step === 'error' && (
          <div className="kr-card p-6 text-center animate-fade-in-up">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-heading font-bold text-red-600 mb-2">Oops! Something went wrong</h2>
            <p className="text-brand-text mb-6">{errorMsg}</p>
            <button onClick={handleReset} className="btn-primary">
              Try Again
            </button>
          </div>
        )}

        {step === 'result' && result && (
          <div className="flex flex-col gap-6 animate-fade-in-up">
            <AdvisoryCard 
              advisory={result.advisory}
              bestMandi={result.best_mandi}
              bestDay={result.best_day}
              priceRange={result.price_range}
              estimatedEarnings={result.estimated_earnings}
              crop={result.crop}
            />
            
            <VoiceButton text={result.advisory} />
            
            <MandiList mandis={result.top_mandis} />

            <button 
              onClick={handleReset}
              className="w-full py-4 rounded-xl font-heading font-bold text-lg text-brand-green bg-green-50 border-2 border-green-200 hover:bg-green-100 transition-colors mt-4"
            >
              ← Get New Advisory
            </button>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
