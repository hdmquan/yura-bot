import sys
from typing import Any

from loguru import logger

from src.config import cfg
from src.discord import Notifier
from src.state import State
from src.twitter import Scraper

logger.remove()
logger.add(
    sys.stderr,
    level=cfg.logging.level,
    format=cfg.logging.format,
)


def run() -> None:
    logger.info("starting yura-bot run")

    state = State()
    scraper = Scraper()
    notifier = Notifier()

    last_id = state.get_last_id()
    logger.info(f"last_id: {last_id}")

    tweets = scraper.fetch_recent(last_id)

    if not tweets:
        logger.info("no new tweets")
        return

    for tweet in tweets:
        notifier.send(tweet)

    state.set_last_id(tweets[-1].id)
    logger.info("run complete")


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        run()
        return {"statusCode": 200, "body": "success"}
    except Exception as e:
        logger.error(f"handler failed: {e}")
        return {"statusCode": 500, "body": f"error: {e}"}


if __name__ == "__main__":
    run()
