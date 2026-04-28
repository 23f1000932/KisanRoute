# KisanRoute 🌾
**Right Market. Right Price. Right Time.**

> AI-powered mandi advisory for Indian smallholder farmers — helping them decide **where to sell**, **when to sell**, and at **what price**, backed by live government data.

---

## 🌍 SDG Alignment
| Goal | How KisanRoute Helps |
|---|---|
| **SDG 2 — Zero Hunger** | Improves agricultural income for smallholder farmers by optimizing market decisions |
| **SDG 10 — Reduced Inequalities** | Democratizes access to real-time market intelligence previously unavailable to rural farmers |

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Advisory (Gemini)** | Generates a 4–5 sentence, actionable advisory based on official mandi price data |
| 📊 **Live Mandi Data** | Fetches real crop prices from India's official **data.gov.in / Agmarknet API** every night |
| 🗓 **Daily Auto-Cache** | APScheduler refreshes `prices.json` at 11 PM IST; also fetches once on startup |
| 🟢 **Data Freshness Badge** | Advisory card shows when data was last updated and its source |
| 📍 **Proximity Ranking** | Compares top 3 nearby mandis by avg price, trend, and distance |
| 🔊 **Voice Playback** | Web Speech API reads out the advisory for low-literacy accessibility |
| ⚡ **Stale Fallback** | If the live API is down, the app serves the last cached `prices.json` without crashing |

---

## 🛠 Tech Stack

| Tier | Technology |
|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Backend** | Python 3.12, Flask 3, Flask-CORS |
| **AI** | Google Gemini API (`gemini-1.5-flash`) |
| **Live Data** | [data.gov.in Agmarknet API](https://data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070) |
| **Scheduler** | APScheduler 3.10 (BackgroundScheduler, Asia/Kolkata) |
| **HTTP Client** | requests 2.31 |

---

## 🏗 Project Structure

```
KisanRoute/
├── backend/
│   ├── app.py                  # Flask app entry point + scheduler init
│   ├── scheduler.py            # APScheduler — daily 23:00 IST + startup fetch
│   ├── requirements.txt
│   ├── .env                    # GEMINI_API_KEY + DATA_GOV_API_KEY
│   ├── data/
│   │   ├── prices.json         # Auto-generated from live API (or stale cache)
│   │   └── cache_meta.json     # last_updated, status, crops_updated
│   ├── routes/
│   │   ├── advisory.py         # POST /api/advisory
│   │   └── mandis.py           # GET /api/mandis, GET /api/cache-status
│   └── services/
│       ├── fetcher.py          # Calls data.gov.in for 10 crops
│       ├── data_cleaner.py     # Cleans raw data → prices.json
│       └── gemini_service.py   # Formats prompt + calls Gemini API
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── AdvisoryCard.jsx  # Shows advisory + 🟢 freshness badge
        │   ├── InputForm.jsx
        │   ├── MandiList.jsx
        │   └── VoiceButton.jsx
        └── services/
            └── api.js
```

---

## 🚀 Setup & Running

### Prerequisites
- Python 3.10+ with `venv`
- Node.js 18+
- A **Gemini API key** (free at [aistudio.google.com](https://aistudio.google.com))
- A **data.gov.in API key** (free at [data.gov.in/user/register](https://data.gov.in/user/register))

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
```

Add your keys to `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_key_here
DATA_GOV_API_KEY=your_data_gov_in_key_here
FLASK_ENV=development
```

```bash
# Start the backend (port 5000)
python app.py
```

On startup you'll see the scheduler log:
```
INFO:scheduler: Scheduler started. Nightly fetch at 23:00 IST. Startup fetch at HH:MM:SS.
INFO:scheduler: Starting daily data fetch from data.gov.in...
INFO:services.fetcher: Fetched 103 records for 'Tomato' ...
INFO:scheduler: Daily fetch complete. prices.json updated successfully.
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/advisory` | Get AI advisory. Body: `{crop, district, state, quantity, sell_window}` |
| `GET` | `/api/mandis?crop=Tomato&district=Nashik` | Get top 3 mandis for a crop+district |
| `GET` | `/api/cache-status` | Returns `cache_meta.json` (last_updated, status, crops) |

### Example Advisory Response
```json
{
  "advisory": "Based on official government market data, you should sell your 500 kg of tomatoes at Nashik Mandi...",
  "best_mandi": "Nashik",
  "best_day": "Tuesday",
  "price_range": "₹18–₹26/kg",
  "estimated_earnings": "₹9,000–₹13,000",
  "data_freshness": {
    "last_updated": "2026-04-28T11:33:56",
    "source": "data.gov.in — Government of India",
    "status": "live"
  }
}
```

---

## 🧠 How the AI Works

```
Farmer Input
    │
    ▼
Flask Backend
    ├── Loads prices.json (auto-refreshed nightly from data.gov.in)
    ├── Ranks top 3 nearby mandis by avg price (last 30 days)
    └── Formats rich prompt:
          "Nashik Mandi (Maharashtra):
            Last 7 days prices (₹/kg): 18, 20, 22, 19, 26, 24, 21
            7-day trend: RISING (+18.3%)
            Best sell day: Tuesday
            Data: Live from Government of India (data.gov.in)"
    │
    ▼
Gemini 1.5 Flash
    └── Returns 4–5 sentence advisory citing official data
    │
    ▼
Frontend (AdvisoryCard)
    ├── Advisory text
    ├── Best Market / Sell Day / Est. Earnings chips
    └── 🟢 "Live data · Updated 28 Apr 2026, 11:33 am · Source: data.gov.in"
```

---

## 🛡 Error Handling

| Scenario | Behaviour |
|---|---|
| data.gov.in API down | Serves last `prices.json` (stale fallback), logs warning |
| API returns no records for a crop | Keeps previous cache entry for that crop |
| `DATA_GOV_API_KEY` missing / invalid | Logs clearly, serves emergency fallback, never crashes |
| Scheduler crash | Wrapped in `try/except`; Flask continues serving |
| `prices.json` corrupted or missing | Falls back to `EMERGENCY_PRICES` dict (hardcoded realistic values) |
| Gemini API down | Returns generic fallback text, endpoint still returns 200 |

---

## 🗺 Supported Districts & Mandis

| District (Farmer) | Nearby Mandis Compared |
|---|---|
| Nashik | Nashik, Pune, Nagpur |
| Pune | Pune, Nashik, Solapur |
| Nagpur | Nagpur, Nashik, Pune |
| Jalgaon | Nashik, Nagpur, Pune |
| Solapur | Solapur, Pune, Nagpur |
| Lucknow | Lucknow, Kanpur, Agra |
| Kanpur | Kanpur, Lucknow, Agra |
| Agra | Agra, Kanpur, Lucknow |
| Varanasi | Lucknow, Kanpur, Allahabad |
| Allahabad | Allahabad, Lucknow, Kanpur |

---

## 🌾 Supported Crops
Tomato · Onion · Potato · Brinjal · Cauliflower · Cabbage · Capsicum · Peas · Garlic · Ginger

---

## 🔮 Roadmap (v3+)
- [ ] Hindi and regional language support (UI + Voice)
- [ ] WhatsApp chatbot for farmers without smartphones
- [ ] GPS-based nearest mandi routing with travel time
- [ ] Push notifications when prices spike
- [ ] Expand to 50+ districts and 20+ crops

---

## 📄 License
MIT License — see [LICENSE](LICENSE)

---

**Team:** Ayan Hussain | IIT Madras BS Data Science
[github.com/23f1000932](https://github.com/23f1000932) | Built for Google Solution Challenge 2026