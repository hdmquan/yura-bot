import os
from typing import Any

import yaml
from pydantic import BaseModel

from src.utils import PATH


class TwitterCfg(BaseModel):
    username: str
    max_tweets_per_check: int


class DiscordCfg(BaseModel):
    color_default: int
    color_media: int
    max_description_length: int
    max_field_length: int
    thumbnail_width: int
    thumbnail_height: int


class StateCfg(BaseModel):
    dynamodb_table: str
    aws_region: str
    last_tweet_key: str


class PollingCfg(BaseModel):
    interval_seconds: int
    retry_backoff_base: int
    retry_max_attempts: int


class RateLimitCfg(BaseModel):
    requests_per_window: int
    window_seconds: int
    cooldown_seconds: int


class LoggingCfg(BaseModel):
    level: str
    format: str


class Cfg(BaseModel):
    twitter: TwitterCfg
    discord: DiscordCfg
    state: StateCfg
    polling: PollingCfg
    rate_limit: RateLimitCfg
    logging: LoggingCfg


def load() -> Cfg:
    with open(PATH.config) as f:
        data: dict[str, Any] = yaml.safe_load(f)
    return Cfg(**data)


cfg = load()

twitter_session = os.getenv("TWITTER_SESSION", "")
discord_webhook = os.getenv("DISCORD_WEBHOOK_URL", "")
aws_key = os.getenv("AWS_ACCESS_KEY_ID", "")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY", "")
aws_region = os.getenv("AWS_REGION", cfg.state.aws_region)
