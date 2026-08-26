import logging
import os

import psycopg

logger = logging.getLogger(__name__)

VALID_EVENTS = {
    "page_view",
    "comparison",
    "ocr_request",
    "ocr_success",
    "ocr_failure",
    "ocr_rate_limited",
}

def track_event(event_type: str, source: str | None = None) -> bool:
    if event_type not in VALID_EVENTS:
        raise ValueError(f"Unknown event type: {event_type}")

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        logger.warning("DATABASE_URL not configured; skipping tracking")
        return False

    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO events (event_type, source)
                    VALUES (%s, %s)
                    """,
                    (event_type, source),
                )

        return True

    except psycopg.Error:
        logger.exception("Failed to record tracking event: %s", event_type)
        return False
