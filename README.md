# yura-bot

Discord bot that monitors @yura_hatuki Twitter and posts to Discord. Runs hourly on AWS Lambda.

## Setup

```bash
make setup
```

Create `.env`:

```
TWITTER_SESSION=your_session_cookie
DISCORD_WEBHOOK_URL=your_webhook_url
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

## Deploy

```bash
make build
cd infra
pulumi login
pulumi stack init prod
pulumi config set twitter_session "SESSION" --secret
pulumi config set discord_webhook "WEBHOOK" --secret
pulumi up
```

## Local Run

```bash
poetry run python -m src.handler
```

## Config

All settings in `config.yaml`.
