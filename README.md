# KisanRoute 🌾
**Right Market. Right Price. Right Time.**

AI-powered mandi (wholesale market) advisory for Indian smallholder farmers, helping them decide **where to sell**, **when to sell**, and at **what price**.

## 🌍 SDG Alignment
- **SDG 2 (Zero Hunger):** Improves agricultural productivity and farmer incomes.
- **SDG 10 (Reduced Inequalities):** Democratizes access to market intelligence for smallholder farmers.

## ✨ Features
1. **AI-Powered Advisories:** Uses Google Gemini 1.5 Flash to generate localized, actionable advice.
2. **Mandi Price Ranking:** Compares nearby markets based on price trends and distance.
3. **Voice Playback:** Web Speech API integration reads out advisories for accessibility.

## 🛠 Tech Stack
| Tier | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | Python 3.11, Flask, Flask-CORS |
| AI | Google Gemini API (`gemini-1.5-flash`) |
| Data | Static mock Agmarknet data (`prices.json`) |

## 🚀 Setup Instructions

### 1. Backend Setup
1. Open a terminal and navigate to the `backend` folder: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
6. Run the server: `python app.py` (Starts on `http://localhost:5000`)

### 2. Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
4. Open the displayed local URL (usually `http://localhost:5173`) in your browser.

## 🧠 How the AI Works
KisanRoute acts as an intelligent layer over raw mandi data. When a farmer submits their details:
1. The Flask backend retrieves the last 7 days of price data for nearby markets from `prices.json`.
2. It ranks the top 3 markets by average price.
3. This data, along with the farmer's crop, district, and quantity, is fed into a crafted prompt to the Gemini API.
4. Gemini analyzes the trends, risks, and prices to generate a concise, easy-to-understand 4-sentence advisory tailored to the farmer.

## 🔮 Future Scope (v2)
- Hindi and regional language support (UI and Voice).
- WhatsApp chatbot integration for lower tech barriers.
- Live integration with the actual Government Agmarknet API.
- GPS-based automated mandi distance routing.

---
**Team:** Ayan Hussain | IIT Madras BS Data Science | [github.com/23f1000932](https://github.com/23f1000932)