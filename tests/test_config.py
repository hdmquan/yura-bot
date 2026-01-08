from src.config import cfg


def test_cfg_loads():
    assert cfg.twitter.username == "yura_hatuki"
    assert cfg.polling.interval_seconds == 3600
    assert cfg.state.dynamodb_table == "yura-bot-state"


def test_twitter_cfg():
    assert cfg.twitter.max_tweets_per_check == 10


def test_discord_cfg():
    assert cfg.discord.color_default == 0x1DA1F2
    assert cfg.discord.max_description_length == 4096


def test_polling_cfg():
    assert cfg.polling.retry_max_attempts == 3
    assert cfg.polling.retry_backoff_base == 2
