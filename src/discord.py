import json
from typing import Any
from urllib.request import Request, urlopen

from loguru import logger

from src.config import cfg, discord_webhook
from src.twitter import Tweet


class Notifier:
    def __init__(self) -> None:
        self.webhook = discord_webhook
        self.color_default = cfg.discord.color_default
        self.color_media = cfg.discord.color_media
        self.max_desc = cfg.discord.max_description_length
        self.max_field = cfg.discord.max_field_length

    def send(self, tweet: Tweet) -> None:
        if not self.webhook:
            logger.warning("discord webhook not configured")
            return

        text = tweet.text[: self.max_desc] if len(tweet.text) > self.max_desc else tweet.text
        color = self.color_media if tweet.media_urls else self.color_default

        embed: dict[str, Any] = {
            "title": f"New post from @{tweet.author}",
            "description": text,
            "url": tweet.url,
            "color": color,
            "timestamp": tweet.created_at,
        }

        if tweet.media_urls:
            embed["image"] = {"url": tweet.media_urls[0]}
            if len(tweet.media_urls) > 1:
                fields = []
                for i, url in enumerate(tweet.media_urls[1:], start=2):
                    fields.append({"name": f"Media {i}", "value": f"[Link]({url})", "inline": True})
                embed["fields"] = fields

        payload = {"embeds": [embed]}

        try:
            req = Request(
                self.webhook,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urlopen(req) as resp:
                if resp.status not in (200, 204):
                    logger.error(f"discord webhook failed: {resp.status}")
                else:
                    logger.info(f"sent tweet {tweet.id} to discord")
        except Exception as e:
            logger.error(f"send failed: {e}")
