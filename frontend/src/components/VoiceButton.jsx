import { useState, useEffect } from 'react'

export default function VoiceButton({ text }) {
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [supported, setSupported] = useState(true)

  useEffect(() => {
    if (!('speechSynthesis' in window)) {
      setSupported(false)
    }
    
    // Cleanup on unmount
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel()
      }
    }
  }, [])

  const handleToggle = () => {
    if (isSpeaking) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    } else {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-IN'
      utterance.rate = 0.85
      utterance.pitch = 1.0

      utterance.onend = () => setIsSpeaking(false)
      utterance.onerror = () => setIsSpeaking(false)

      setIsSpeaking(true)
      window.speechSynthesis.speak(utterance)
    }
  }

  if (!supported) return null

  return (
    <button 
      onClick={handleToggle}
      className={`w-full ${isSpeaking ? 'btn-primary bg-red-500 hover:bg-red-600' : 'btn-amber'}`}
    >
      {isSpeaking ? '⏹ Stop Audio' : '🔊 Listen to Advisory'}
    </button>
  )
}
