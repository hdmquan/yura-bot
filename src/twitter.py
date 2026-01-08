from dataclasses import dataclass

from loguru import logger
from tweety import Twitter

from src.config import cfg, twitter_session


@dataclass
class Tweet:
    id: str
    text: str
    url: str
    media_urls: list[str]
    created_at: str
    author: str


class Scraper:
    def __init__(self) -> None:
        self.app = Twitter("session")
        if twitter_session:
            self.app.session = twitter_session
        self.username = cfg.twitter.username
        self.max_tweets = cfg.twitter.max_tweets_per_check

    def fetch_recent(self, last_id: str | None) -> list[Tweet]:
        try:
            user = self.app.get_user_info(self.username)
            tweets = self.app.get_tweets(user, pages=1, wait_time=2)

            results: list[Tweet] = []
            for tw in tweets:
                if len(results) >= self.max_tweets:
                    break

                if last_id and str(tw.id) == last_id:
                    break

                media: list[str] = []
                if hasattr(tw, "media") and tw.media:
                    for m in tw.media:
                        if hasattr(m, "media_url_https"):
                            media.append(m.media_url_https)
                        elif hasattr(m, "url"):
                            media.append(m.url)

                results.append(
                    Tweet(
                        id=str(tw.id),
                        text=tw.text or "",
                        url=f"https://x.com/{self.username}/status/{tw.id}",
                        media_urls=media,
                        created_at=str(tw.created_on) if hasattr(tw, "created_on") else "",
                        author=self.username,
                    )
                )

            logger.info(f"fetched {len(results)} new tweets")
            return list(reversed(results))

        except Exception as e:
            logger.error(f"fetch_recent failed: {e}")
            return []
