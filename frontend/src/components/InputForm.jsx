import { useState } from 'react'

const CROPS = [
  "Tomato", "Onion", "Potato", "Brinjal", "Cauliflower",
  "Cabbage", "Capsicum", "Peas", "Garlic", "Ginger"
]

const DISTRICTS = [
  "Nashik", "Lucknow", "Pune", "Kanpur", "Nagpur",
  "Agra", "Jalgaon", "Varanasi", "Solapur", "Allahabad"
]

// Auto-derive state from district so user doesn't need to fill it separately
const DISTRICT_STATE = {
  "Nashik":    "Maharashtra",
  "Lucknow":   "Uttar Pradesh",
  "Pune":      "Maharashtra",
  "Kanpur":    "Uttar Pradesh",
  "Nagpur":    "Maharashtra",
  "Agra":      "Uttar Pradesh",
  "Jalgaon":   "Maharashtra",
  "Varanasi":  "Uttar Pradesh",
  "Solapur":   "Maharashtra",
  "Allahabad": "Uttar Pradesh",
}

export default function InputForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    crop: '',
    district: '',
    quantity: '',
    sell_window: 'This week'
  })
  
  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }))
    }
  }

  const handleRadioChange = (val) => {
    setFormData(prev => ({ ...prev, sell_window: val }))
  }

  const validate = () => {
    const newErrors = {}
    if (!formData.crop) newErrors.crop = "Please select a crop"
    if (!formData.district) newErrors.district = "Please select your district"
    if (!formData.quantity) {
      newErrors.quantity = "Quantity is required"
    } else if (isNaN(formData.quantity) || formData.quantity < 1 || formData.quantity > 50000) {
      newErrors.quantity = "Enter a valid quantity (1 - 50,000)"
    }
    return newErrors
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const newErrors = validate()
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    // Inject state derived from district before sending to API
    const payload = {
      ...formData,
      state: DISTRICT_STATE[formData.district] || "India"
    }
    onSubmit(payload)
  }

  return (
    <div className="kr-card p-6">
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        
        {/* Crop Selection */}
        <div>
          <label htmlFor="crop" className="form-label">Select Your Crop</label>
          <select 
            id="crop"
            name="crop"
            value={formData.crop}
            onChange={handleChange}
            className={`form-control ${errors.crop ? 'border-red-500' : ''}`}
          >
            <option value="">-- Choose a crop --</option>
            {CROPS.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          {errors.crop && <p className="text-red-500 text-xs mt-1">{errors.crop}</p>}
        </div>

        {/* District Selection */}
        <div>
          <label htmlFor="district" className="form-label">Your District</label>
          <select 
            id="district"
            name="district"
            value={formData.district}
            onChange={handleChange}
            className={`form-control ${errors.district ? 'border-red-500' : ''}`}
          >
            <option value="">-- Choose your district --</option>
            {DISTRICTS.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
          {errors.district && <p className="text-red-500 text-xs mt-1">{errors.district}</p>}
        </div>

        {/* Quantity */}
        <div>
          <label htmlFor="quantity" className="form-label">Quantity Available (kg)</label>
          <input 
            type="number"
            id="quantity"
            name="quantity"
            min="1"
            max="50000"
            placeholder="e.g. 200"
            value={formData.quantity}
            onChange={handleChange}
            className={`form-control ${errors.quantity ? 'border-red-500' : ''}`}
          />
          {errors.quantity && <p className="text-red-500 text-xs mt-1">{errors.quantity}</p>}
        </div>

        {/* Sell Window */}
        <div>
          <label className="form-label mb-2">When do you plan to sell?</label>
          <div className="flex gap-3">
            <div 
              className={`radio-option flex-1 ${formData.sell_window === 'This week' ? 'selected' : ''}`}
              onClick={() => handleRadioChange('This week')}
            >
              <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${formData.sell_window === 'This week' ? 'border-brand-green' : 'border-gray-400'}`}>
                {formData.sell_window === 'This week' && <div className="w-2 h-2 rounded-full bg-brand-green"></div>}
              </div>
              <span className="text-sm font-medium">This week</span>
            </div>
            <div 
              className={`radio-option flex-1 ${formData.sell_window === 'Next week' ? 'selected' : ''}`}
              onClick={() => handleRadioChange('Next week')}
            >
              <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${formData.sell_window === 'Next week' ? 'border-brand-green' : 'border-gray-400'}`}>
                {formData.sell_window === 'Next week' && <div className="w-2 h-2 rounded-full bg-brand-green"></div>}
              </div>
              <span className="text-sm font-medium">Next week</span>
            </div>
          </div>
        </div>

        <button type="submit" className="btn-primary mt-2">
          Get Advisory →
        </button>

        <p className="text-center text-xs text-brand-muted mt-2">
          This is an AI-generated advisory. Final selling decisions are yours.
        </p>
      </form>
    </div>
  )
}
