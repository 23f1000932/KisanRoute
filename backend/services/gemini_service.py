import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

SYSTEM_PROMPT = """You are KisanRoute, a trusted agricultural market advisor helping Indian 
smallholder farmers get the best price for their produce. You speak in 
clear, simple English that is easy to understand.

You will receive the farmer's crop, location, quantity, preferred selling 
window, and recent mandi (wholesale market) price data for nearby markets.

The price data you receive is sourced live from India's official government 
mandi database (data.gov.in / Agmarknet). Reference this credibility in 
your advisory: mention it is based on official market data.

Write a concise advisory of 3-5 sentences covering:
1. Which mandi (market) the farmer should go to and why (price-based reason)
2. Which specific day this week is best to sell and the expected price range
3. Estimated total earnings (quantity x expected price, shown as a range)
4. One practical risk or tip to watch out for this week

Rules:
- Be specific: use actual mandi names, exact rupee amounts, exact day names
- No bullet points, no lists, no headers — flowing natural sentences only
- Keep total response under 100 words
- End with one short encouraging sentence
- Do not use any Hindi words
- Complete every sentence fully — do not stop mid-sentence"""


def format_mandi_data(mandi_data: list) -> str:
    """Format mandi list into a rich human-readable string for the prompt."""
    lines = []
    for mandi in mandi_data:
        prices = mandi["prices"]
        prices_str = ", ".join(str(p) for p in prices)
        min_p = mandi.get("avg_price", min(prices))
        max_p = max(prices)
        modal = round(sum(prices[-3:]) / min(3, len(prices)), 1)
        trend = mandi["trend"].upper()

        # Compute % change for display
        first3 = prices[:3] if len(prices) >= 3 else prices
        last3 = prices[-3:] if len(prices) >= 3 else prices
        avg_first = sum(first3) / len(first3)
        avg_last = sum(last3) / len(last3)
        pct = round(((avg_last - avg_first) / avg_first) * 100, 1) if avg_first else 0
        pct_str = f"+{pct}%" if pct >= 0 else f"{pct}%"

        lines.append(
            f"{mandi['name']} Mandi ({mandi['state']}):\n"
            f"   Last 7 days prices (₹/kg): {prices_str}\n"
            f"   Today's range: ₹{min(prices)}–₹{max_p} | Modal: ₹{modal}\n"
            f"   7-day trend: {trend} ({pct_str})\n"
            f"   Best sell day: {mandi['best_day']}\n"
            f"   Market risk: {mandi['risk']}\n"
            f"   Data: Live from Government of India (data.gov.in)"
        )
    return "\n\n".join(lines)


def generate_advisory(
    crop: str,
    district: str,
    state: str,
    quantity: int,
    sell_window: str,
    mandi_data: list,
) -> str:
    """Call Gemini API and return advisory string."""
    fallback = (
        "We're unable to generate an advisory right now. "
        "Please try again in a moment."
    )

    if not GEMINI_API_KEY:
        return fallback

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=600,
            ),
        )

        mandi_formatted = format_mandi_data(mandi_data)

        user_prompt = f"""Crop: {crop}
Farmer's District: {district}, {state}
Quantity available: {quantity} kg
Preferred selling window: {sell_window}

Recent mandi prices for {crop} (₹/kg, last 7 days):
{mandi_formatted}

What is your advisory for this farmer?"""

        response = model.generate_content(user_prompt)
        return response.text.strip()

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return fallback
