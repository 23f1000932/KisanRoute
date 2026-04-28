"""
KisanRoute — Data Fetcher Service
Fetches crop price data from data.gov.in (Agmarknet API).

API Details:
  Base URL : https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
  Auth     : api-key query param
  Key fields: state, district, market, commodity,
              arrival_date, min_price, max_price, modal_price
  Prices are in PAISE — divide by 100 to get ₹/kg
  Rate limit: 100 requests/hour on free tier
  Dataset updates: daily by 10 AM IST
"""

import requests
import json
import os
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CROPS = [
    "Tomato", "Onion", "Potato", "Brinjal", "Cauliflower",
    "Cabbage", "Capsicum", "Peas", "Garlic", "Ginger"
]

TARGET_STATES = [
    "Maharashtra", "Uttar Pradesh", "Karnataka",
    "Punjab", "Rajasthan", "Madhya Pradesh",
    "Gujarat", "Andhra Pradesh", "Tamil Nadu"
]

BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


def fetch_crop_data(crop: str, api_key: str) -> list:
    """
    Fetch raw records for a single crop from data.gov.in.

    Returns a list of record dicts, or [] on any failure.
    """
    params = {
        "api-key": api_key,
        "format": "json",
        "filters[commodity]": crop,
        "limit": 500,
        "offset": 0,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code == 401:
            logger.error(
                "DATA_GOV_API_KEY invalid or expired — check your .env file. "
                "Get a free key at https://data.gov.in/user/me/api-keys"
            )
            return []

        if response.status_code != 200:
            logger.warning(
                f"data.gov.in returned HTTP {response.status_code} for crop '{crop}'. "
                f"Skipping this crop."
            )
            return []

        data = response.json()
        records = data.get("records", [])

        if not records:
            logger.info(f"No data returned for '{crop}' — API response was empty.")
            return []

        # Filter to target states client-side (API doesn't support multi-value state filter reliably)
        filtered = [
            r for r in records
            if r.get("state", "").strip() in TARGET_STATES
        ]

        logger.info(
            f"Fetched {len(filtered)} records for '{crop}' "
            f"(raw: {len(records)}, after state filter: {len(filtered)})"
        )
        return filtered

    except requests.exceptions.Timeout:
        logger.error(f"Timeout fetching data for '{crop}' — data.gov.in may be slow.")
        return []
    except requests.exceptions.ConnectionError:
        logger.error(
            f"Connection error fetching data for '{crop}' — "
            "data.gov.in may be down. Will use cached data."
        )
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching '{crop}': {e}", exc_info=True)
        return []


def fetch_all_crops(api_key: str) -> dict:
    """
    Fetch data for all crops in CROPS list.

    Returns dict: { crop_name: [raw_record_dicts] }
    Empty lists are kept (data_cleaner handles stale fallback for those).
    """
    result = {}

    for crop in CROPS:
        logger.info(f"Fetching data for crop: {crop} ...")
        records = fetch_crop_data(crop, api_key)
        result[crop] = records  # always store, even if []

        # Respect rate limit — 0.5s between calls
        time.sleep(0.5)

    total = sum(len(v) for v in result.values())
    logger.info(
        f"Fetch complete. Total records across all crops: {total}"
    )
    return result


# ─── Standalone test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    api_key = os.getenv("DATA_GOV_API_KEY", "")
    if not api_key or api_key == "your_data_gov_in_api_key_here":
        print("[ERROR] DATA_GOV_API_KEY not set in .env")
        print("  → Get a free key at https://data.gov.in/user/me/api-keys")
        print("  → Add it to backend/.env as: DATA_GOV_API_KEY=your_key_here")
        exit(1)

    print(f"[INFO] Starting standalone fetch at {datetime.now().isoformat()}")
    raw = fetch_all_crops(api_key)
    print("\n=== Fetch Summary ===")
    for crop, records in raw.items():
        print(f"  {crop:<15}: {len(records):>4} records")
    print(f"\nTotal: {sum(len(v) for v in raw.values())} records")
