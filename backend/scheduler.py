"""
KisanRoute — APScheduler Cron Job
Runs a daily fetch from data.gov.in at 23:00 IST and once on startup.
"""

import logging
import os
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

logger = logging.getLogger(__name__)


def run_daily_fetch():
    """Fetch fresh crop price data and rebuild prices.json."""
    try:
        # Lazy imports to avoid circular dependency at module load time
        from services import fetcher, data_cleaner

        logger.info("=" * 60)
        logger.info("Starting daily data fetch from data.gov.in...")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")

        api_key = os.getenv("DATA_GOV_API_KEY", "")
        if not api_key or api_key == "your_data_gov_in_api_key_here":
            logger.error(
                "DATA_GOV_API_KEY not set in .env — skipping live fetch. "
                "App will continue serving existing prices.json."
            )
            return

        raw_data = fetcher.fetch_all_crops(api_key)
        success = data_cleaner.build_prices_json(raw_data)

        if success:
            logger.info("Daily fetch complete. prices.json updated successfully.")
        else:
            logger.warning("Daily fetch completed with errors. Using previous cached data.")

        logger.info("=" * 60)

    except Exception:
        logger.error(
            "Unhandled exception in run_daily_fetch — scheduler continues running.\n"
            + traceback.format_exc()
        )


def init_scheduler():
    """
    Create and start the BackgroundScheduler.

    Jobs:
      1. Nightly cron at 23:00 IST (after markets close)
      2. One-shot date trigger 10 seconds after startup (data fresh immediately)

    Returns the scheduler instance (caller should store it and register atexit).
    """
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # ── Nightly cron ──────────────────────────────────────────────────────────
    scheduler.add_job(
        run_daily_fetch,
        trigger="cron",
        hour=23,
        minute=0,
        id="nightly_fetch",
        name="Nightly data.gov.in fetch",
        replace_existing=True,
    )

    # ── Startup one-shot (10 s delay so Flask is fully up) ────────────────────
    startup_time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(
        run_daily_fetch,
        trigger="date",
        run_date=startup_time,
        id="startup_fetch",
        name="Startup data fetch",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        f"Scheduler started. Nightly fetch at 23:00 IST. "
        f"Startup fetch at {startup_time.strftime('%H:%M:%S')}."
    )
    return scheduler
