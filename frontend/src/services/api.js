const BASE_URL = '/api'

/**
 * POST /api/advisory
 * @param {Object} formData - { crop, district, state, quantity, sell_window }
 */
export async function getAdvisory(formData) {
  const response = await fetch(`${BASE_URL}/advisory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || `Server error ${response.status}`)
  }

  return data
}

/**
 * GET /api/mandis?crop=X&district=Y
 * @param {string} crop
 * @param {string} district
 */
export async function getMandis(crop, district) {
  const params = new URLSearchParams({ crop, district })
  const response = await fetch(`${BASE_URL}/mandis?${params}`)

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || `Server error ${response.status}`)
  }

  return data
}
