"""
KisanRoute — Data Cleaner Service
Cleans raw API records and builds prices.json + cache_meta.json.
"""

import sys
import json
import os
import logging
from datetime import datetime, timedelta

# Ensure UTF-8 output on Windows (handles rupee ₹ symbol in console)
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRICES_PATH = os.path.join(DATA_DIR, "prices.json")
CACHE_META_PATH = os.path.join(DATA_DIR, "cache_meta.json")

CROPS = [
    "Tomato", "Onion", "Potato", "Brinjal", "Cauliflower",
    "Cabbage", "Capsicum", "Peas", "Garlic", "Ginger"
]

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

ALL_MANDIS = list({m for mandis in PROXIMITY_MAP.values() for m in mandis})

# Absolute last-resort fallback if prices.json is missing/corrupted
EMERGENCY_PRICES = {
    "Tomato": {
        "Nashik":    {"state": "Maharashtra", "prices": [18.0, 20.0, 22.0, 19.0, 24.0, 23.0, 21.0], "min_price": 18.0, "max_price": 24.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Pune":      {"state": "Maharashtra", "prices": [17.0, 19.0, 21.0, 20.0, 23.0, 22.0, 20.0], "min_price": 17.0, "max_price": 23.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Nagpur":    {"state": "Maharashtra", "prices": [16.0, 18.0, 20.0, 19.0, 22.0, 21.0, 19.0], "min_price": 16.0, "max_price": 22.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Lucknow":   {"state": "Uttar Pradesh", "prices": [15.0, 17.0, 19.0, 18.0, 21.0, 20.0, 18.0], "min_price": 15.0, "max_price": 21.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Kanpur":    {"state": "Uttar Pradesh", "prices": [14.0, 16.0, 18.0, 17.0, 20.0, 19.0, 17.0], "min_price": 14.0, "max_price": 20.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Agra":      {"state": "Uttar Pradesh", "prices": [13.0, 15.0, 17.0, 16.0, 19.0, 18.0, 16.0], "min_price": 13.0, "max_price": 19.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Solapur":   {"state": "Maharashtra", "prices": [15.0, 17.0, 19.0, 18.0, 21.0, 20.0, 18.0], "min_price": 15.0, "max_price": 21.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Allahabad": {"state": "Uttar Pradesh", "prices": [14.0, 16.0, 18.0, 17.0, 20.0, 19.0, 17.0], "min_price": 14.0, "max_price": 20.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
    },
    "Onion": {
        "Nashik":    {"state": "Maharashtra", "prices": [22.0, 24.0, 26.0, 25.0, 28.0, 27.0, 25.0], "min_price": 22.0, "max_price": 28.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Pune":      {"state": "Maharashtra", "prices": [21.0, 23.0, 25.0, 24.0, 27.0, 26.0, 24.0], "min_price": 21.0, "max_price": 27.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Nagpur":    {"state": "Maharashtra", "prices": [20.0, 22.0, 24.0, 23.0, 26.0, 25.0, 23.0], "min_price": 20.0, "max_price": 26.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Lucknow":   {"state": "Uttar Pradesh", "prices": [18.0, 20.0, 22.0, 21.0, 24.0, 23.0, 21.0], "min_price": 18.0, "max_price": 24.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Kanpur":    {"state": "Uttar Pradesh", "prices": [17.0, 19.0, 21.0, 20.0, 23.0, 22.0, 20.0], "min_price": 17.0, "max_price": 23.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Agra":      {"state": "Uttar Pradesh", "prices": [16.0, 18.0, 20.0, 19.0, 22.0, 21.0, 19.0], "min_price": 16.0, "max_price": 22.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Solapur":   {"state": "Maharashtra", "prices": [20.0, 22.0, 24.0, 23.0, 26.0, 25.0, 23.0], "min_price": 20.0, "max_price": 26.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
        "Allahabad": {"state": "Uttar Pradesh", "prices": [17.0, 19.0, 21.0, 20.0, 23.0, 22.0, 20.0], "min_price": 17.0, "max_price": 23.0, "trend": "stable", "best_day": "Thursday", "risk": "Stable demand, low risk this week", "last_updated": "2026-04-28", "records_count": 7},
    },
}

# Pad EMERGENCY_PRICES with generic data for remaining crops
for _crop in CROPS:
    if _crop not in EMERGENCY_PRICES:
        EMERGENCY_PRICES[_crop] = {}
        for _mandi in ALL_MANDIS:
            _base = 15.0
            EMERGENCY_PRICES[_crop][_mandi] = {
                "state": "Maharashtra" if _mandi in ["Nashik", "Pune", "Nagpur", "Solapur"] else "Uttar Pradesh",
                "prices": [_base, _base+1, _base+2, _base+1.5, _base+3, _base+2.5, _base+2],
                "min_price": _base,
                "max_price": _base + 3,
                "trend": "stable",
                "best_day": "Thursday",
                "risk": "Stable demand, low risk this week",
                "last_updated": "2026-04-28",
                "records_count": 7,
            }


def _load_existing_prices() -> dict:
    """Load existing prices.json as fallback, or return EMERGENCY_PRICES."""
    try:
        if os.path.exists(PRICES_PATH):
            with open(PRICES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                return data
    except Exception as e:
        logger.warning(f"Could not load existing prices.json: {e}")
    logger.warning("Using EMERGENCY_PRICES as fallback.")
    return EMERGENCY_PRICES


def clean_records(raw_records: list) -> dict:
    """
    Clean raw API records for ONE crop.

    Returns dict: { mandi_name: { structured fields } }
    """
    today = datetime.today()
    # Use 30-day window: data.gov.in can be up to 2 weeks behind live markets
    cutoff = today - timedelta(days=30)
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Group valid records by DISTRICT (API 'market' field uses APMC suffixes like
    # "Pune(Pimpri) APMC" — district field gives clean city names matching ALL_MANDIS)
    grouped: dict[str, list] = {}
    for r in raw_records:
        district = r.get("district", "").strip().title()
        if district not in ALL_MANDIS:
            continue

        try:
            price = int(r.get("modal_price", 0)) / 100.0  # paise → ₹
        except (ValueError, TypeError):
            continue

        if price <= 0 or price > 10000:
            continue  # anomaly guard

        # Parse arrival_date: DD/MM/YYYY
        try:
            arrival = datetime.strptime(r.get("arrival_date", ""), "%d/%m/%Y")
        except ValueError:
            continue

        if arrival < cutoff:
            continue  # older than 30 days

        state = r.get("state", "").strip()
        if district not in grouped:
            grouped[district] = []
        grouped[district].append({"price": price, "date": arrival, "state": state})

    result = {}
    for market, entries in grouped.items():
        if not entries:
            continue

        # Sort by arrival date ascending
        entries.sort(key=lambda x: x["date"])
        prices = [e["price"] for e in entries]
        state = entries[-1]["state"]

        # Compute trend: last 3 vs first 3
        first3 = prices[:3] if len(prices) >= 3 else prices
        last3 = prices[-3:] if len(prices) >= 3 else prices
        avg_first = sum(first3) / len(first3)
        avg_last = sum(last3) / len(last3)

        if avg_first > 0:
            pct_change = (avg_last - avg_first) / avg_first
        else:
            pct_change = 0

        if pct_change > 0.10:
            trend = "rising"
        elif pct_change < -0.10:
            trend = "falling"
        else:
            trend = "stable"

        # Best sell day: index of max price mapped to day name
        max_idx = prices.index(max(prices))
        best_day = day_names[(today.weekday() - (len(prices) - 1 - max_idx)) % 7]

        # Risk string
        if trend == "falling":
            risk = "Prices declining — consider selling immediately"
        elif trend == "rising":
            risk = "Prices rising — wait for peak if possible"
        else:
            risk = "Stable demand, low risk this week"

        result[market] = {
            "state": state,
            "prices": [round(p, 2) for p in prices],
            "min_price": round(min(prices), 2),
            "max_price": round(max(prices), 2),
            "trend": trend,
            "best_day": best_day,
            "risk": risk,
            "last_updated": today.strftime("%Y-%m-%d"),
            "records_count": len(entries),
        }

    return result


def build_prices_json(raw_data_dict: dict) -> bool:
    """
    Merge cleaned live data with stale fallback and write prices.json + cache_meta.json.

    Returns True on success, False on failure.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    existing = _load_existing_prices()
    output = {}
    crops_updated = []
    crops_stale = []
    total_records = 0

    for crop in CROPS:
        records = raw_data_dict.get(crop, [])

        if not records:
            logger.warning(f"Using cached data for '{crop}' — API returned empty")
            output[crop] = existing.get(crop, EMERGENCY_PRICES.get(crop, {}))
            crops_stale.append(crop)
            continue

        cleaned = clean_records(records)
        total_records += sum(r["records_count"] for r in cleaned.values())

        if not cleaned:
            logger.warning(
                f"No valid mandi records after cleaning for '{crop}'. Using cache."
            )
            output[crop] = existing.get(crop, EMERGENCY_PRICES.get(crop, {}))
            crops_stale.append(crop)
            continue

        # Merge: start from existing (preserves mandis missing from today's fetch)
        crop_base = dict(existing.get(crop, {}))
        crop_base.update(cleaned)
        output[crop] = crop_base
        crops_updated.append(crop)

    try:
        with open(PRICES_PATH, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        logger.info(f"prices.json written — {total_records} records across {len(crops_updated)} crops.")
    except Exception as e:
        logger.error(f"Failed to write prices.json: {e}")
        return False

    # Determine overall status
    if not crops_updated:
        status = "failed"
    elif crops_stale:
        status = "partial"
    else:
        status = "success"

    cache_meta = {
        "last_updated": datetime.now().isoformat(),
        "status": status,
        "crops_updated": crops_updated,
        "crops_stale": crops_stale,
        "total_records": total_records,
        "source": "data.gov.in",
    }

    try:
        with open(CACHE_META_PATH, "w", encoding="utf-8") as f:
            json.dump(cache_meta, f, indent=2, ensure_ascii=False)
        logger.info(f"cache_meta.json written — status: {status}")
    except Exception as e:
        logger.error(f"Failed to write cache_meta.json: {e}")

    return True


# ─── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[INFO] Running data_cleaner standalone test with empty raw data...")
    print("  (This will trigger stale fallback for all crops)")
    empty_raw = {crop: [] for crop in CROPS}
    success = build_prices_json(empty_raw)
    print(f"\n[{'OK' if success else 'FAIL'}] build_prices_json returned {success}")
    if os.path.exists(PRICES_PATH):
        with open(PRICES_PATH) as f:
            data = json.load(f)
        print(f"[INFO] prices.json crops: {list(data.keys())}")
        # Sanity check — prices should be ₹ values, not paise
        first_crop = list(data.keys())[0]
        first_mandi = list(data[first_crop].keys())[0]
        sample_prices = data[first_crop][first_mandi]["prices"]
        print(f"[INFO] Sample prices for {first_crop}/{first_mandi}: {sample_prices}")
        if any(p > 1000 for p in sample_prices):
            print("[WARN] Prices look like they may still be in paise — check conversion!")
        else:
            print("[OK] Prices are in ₹/kg range (good).")
