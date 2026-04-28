import json
import os
from flask import Blueprint, request, jsonify

mandis_bp = Blueprint("mandis", __name__)

# Proximity map: farmer's district → nearby mandi names (in prices.json)
PROXIMITY_MAP = {
    "Nashik":    ["Nashik", "Pune", "Nagpur"],
    "Lucknow":   ["Lucknow", "Kanpur", "Agra"],
    "Pune":      ["Pune", "Nashik", "Solapur"],
    "Kanpur":    ["Kanpur", "Lucknow", "Agra"],
    "Nagpur":    ["Nagpur", "Nashik", "Pune"],
    "Agra":      ["Agra", "Kanpur", "Lucknow"],
    "Jalgaon":   ["Nashik", "Nagpur", "Pune"],
    "Varanasi":  ["Lucknow", "Kanpur", "Allahabad"],
    "Solapur":   ["Solapur", "Pune", "Nagpur"],
    "Allahabad": ["Allahabad", "Lucknow", "Kanpur"],
}

# Approximate distances (km) for rank positions
DISTANCE_MAP = [0, 40, 90]


def load_prices():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.json")
    with open(data_path, "r") as f:
        return json.load(f)


def get_top_mandis(crop, district):
    """
    Core logic: returns top-3 mandis for a crop+district combo.
    Used both by the mandis route and the advisory route.
    """
    prices_data = load_prices()

    # Normalise input
    crop = crop.strip().title()
    district = district.strip().title()

    # Fallback if district not in proximity map
    nearby = PROXIMITY_MAP.get(district, list(PROXIMITY_MAP.values())[0])

    # Fallback if crop not in data
    crop_data = prices_data.get(crop, {})
    if not crop_data:
        # Try the first available crop as last resort
        crop = list(prices_data.keys())[0]
        crop_data = prices_data[crop]

    results = []
    for rank, mandi_name in enumerate(nearby):
        mandi_info = crop_data.get(mandi_name)
        if not mandi_info:
            # Use any available mandi from the dataset
            available = [k for k in crop_data.keys() if k not in [r["name"] for r in results]]
            if available:
                mandi_name = available[0]
                mandi_info = crop_data[mandi_name]
            else:
                continue

        prices = mandi_info["prices"]
        avg_last3 = round(sum(prices[-3:]) / 3, 2)

        distance = DISTANCE_MAP[rank] if rank < len(DISTANCE_MAP) else 120

        results.append({
            "name": mandi_name,
            "state": mandi_info["state"],
            "avg_price": avg_last3,
            "trend": mandi_info["trend"],
            "best_day": mandi_info["best_day"],
            "distance_km": distance,
            "risk": mandi_info["risk"],
            "prices": prices,
        })

    # Sort by avg_price descending
    results.sort(key=lambda x: x["avg_price"], reverse=True)

    # Re-assign distances after sort (rank 0 → 0 km, etc.)
    for i, item in enumerate(results):
        item["distance_km"] = DISTANCE_MAP[i] if i < len(DISTANCE_MAP) else 120

    return results[:3]


@mandis_bp.route("/mandis", methods=["GET"])
def get_mandis():
    crop = request.args.get("crop", "").strip()
    district = request.args.get("district", "").strip()

    if not crop or not district:
        return jsonify({"error": "crop and district query parameters are required"}), 400

    try:
        top_mandis = get_top_mandis(crop, district)
        return jsonify(top_mandis), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
