import json
import os
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from routes.mandis import get_top_mandis
from services.gemini_service import generate_advisory

advisory_bp = Blueprint("advisory", __name__)

REQUIRED_FIELDS = ["crop", "district", "state", "quantity", "sell_window"]

# District → state lookup for convenience
DISTRICT_STATE = {
    "Nashik": "Maharashtra",
    "Lucknow": "Uttar Pradesh",
    "Pune": "Maharashtra",
    "Kanpur": "Uttar Pradesh",
    "Nagpur": "Maharashtra",
    "Agra": "Uttar Pradesh",
    "Jalgaon": "Maharashtra",
    "Varanasi": "Uttar Pradesh",
    "Solapur": "Maharashtra",
    "Allahabad": "Uttar Pradesh",
}


@advisory_bp.route("/advisory", methods=["POST"])
def post_advisory():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON", "fallback": True}), 400

    # Validate all required fields
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        return (
            jsonify({
                "error": f"Missing required fields: {', '.join(missing)}",
                "fallback": True,
            }),
            400,
        )

    crop = data["crop"].strip().title()
    district = data["district"].strip().title()
    state = data.get("state", DISTRICT_STATE.get(district, "India")).strip()
    quantity = int(data["quantity"])
    sell_window = data["sell_window"].strip()

    # Get top 3 mandis
    try:
        top_mandis = get_top_mandis(crop, district)
    except Exception as e:
        return jsonify({"error": str(e), "fallback": True}), 500

    if not top_mandis:
        return jsonify({"error": "No mandi data found for this combination", "fallback": True}), 404

    best_mandi = top_mandis[0]

    # Generate Gemini advisory
    advisory_text = generate_advisory(
        crop=crop,
        district=district,
        state=state,
        quantity=quantity,
        sell_window=sell_window,
        mandi_data=top_mandis,
    )

    # Compute price range from best mandi last 3 days
    recent_prices = best_mandi["prices"][-3:]
    low_price = min(recent_prices)
    high_price = max(recent_prices)
    avg_price = round(sum(recent_prices) / len(recent_prices), 1)

    estimated_low = int(quantity * low_price)
    estimated_high = int(quantity * high_price)

    def fmt_inr(amount: int) -> str:
        """Format Indian rupee with comma notation."""
        s = str(amount)
        if len(s) > 3:
            last3 = s[-3:]
            rest = s[:-3]
            groups = []
            while len(rest) > 2:
                groups.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                groups.append(rest)
            groups.reverse()
            s = ",".join(groups) + "," + last3
        return f"₹{s}"

    # ── Load cache metadata for data freshness indicator ──────────────────────
    cache_meta_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "cache_meta.json"
    )
    data_freshness = {
        "last_updated": None,
        "source": "data.gov.in — Government of India",
        "status": "stale",
    }
    try:
        with open(cache_meta_path, "r") as f:
            meta = json.load(f)
        last_updated_str = meta.get("last_updated")
        if last_updated_str:
            last_updated_dt = datetime.fromisoformat(last_updated_str)
            if last_updated_dt.tzinfo is None:
                last_updated_dt = last_updated_dt.replace(tzinfo=timezone.utc)
            age_hours = (datetime.now(timezone.utc) - last_updated_dt).total_seconds() / 3600
            data_freshness = {
                "last_updated": last_updated_str,
                "source": "data.gov.in — Government of India",
                "status": "live" if age_hours <= 48 else "stale",
            }
    except Exception:
        pass  # keep default stale — never crash advisory endpoint

    return jsonify({
        "advisory": advisory_text,
        "top_mandis": top_mandis,
        "crop": crop,
        "best_mandi": best_mandi["name"],
        "best_day": best_mandi["best_day"],
        "price_range": f"₹{low_price}–{high_price}/kg",
        "estimated_earnings": f"{fmt_inr(estimated_low)}–{fmt_inr(estimated_high)}",
        "data_freshness": data_freshness,
    }), 200
