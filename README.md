# yura-bot

Discord bot that monitors Twitter account and posts updates to Discord webhook. Runs on AWS Lambda with hourly polling.

## Features

- Monitors @yura_hatuki Twitter account
- Posts text, images, videos, and links to Discord
- Tracks last posted tweet in DynamoDB
- Runs hourly via AWS EventBridge
- No Twitter API fees (uses web scraping)

## Architecture

- **Language**: Python 3.11
- **Deployment**: AWS Lambda (serverless)
- **State Storage**: DynamoDB
- **Scheduling**: EventBridge (1 hour interval)
- **Infrastructure**: Pulumi
- **CI/CD**: GitHub Actions

## Setup

### 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

```bash
make setup
```

This installs dependencies and sets up pre-commit hooks.

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

Required variables:
- `TWITTER_SESSION`: Your Twitter session cookie
- `DISCORD_WEBHOOK_URL`: Discord webhook URL for posting
- `AWS_ACCESS_KEY_ID`: AWS credentials
- `AWS_SECRET_ACCESS_KEY`: AWS credentials

### 4. Configure Pulumi

```bash
cd infra
pulumi login
pulumi stack init prod
pulumi config set twitter_session "YOUR_SESSION" --secret
pulumi config set discord_webhook "YOUR_WEBHOOK" --secret
```

### 5. Deploy

Build Lambda package:
```bash
bash scripts/build_lambda.sh
```

Deploy infrastructure:
```bash
cd infra
pulumi up
```

## Local Testing

Run manually:
```bash
poetry run python -m src.handler
```

## Configuration

All settings in `config.yaml`:
- Polling interval (default: 1 hour)
- Rate limits
- Discord embed styling
- DynamoDB settings

## GitHub Actions Secrets

Required secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `TWITTER_SESSION`
- `DISCORD_WEBHOOK_URL`
- `PULUMI_ACCESS_TOKEN`

## Development

Lint:
```bash
poetry run black .
poetry run ruff check .
poetry run mypy src
```

Test:
```bash
poetry run pytest
```

## Rate Limits

Polls every hour to avoid Twitter rate limits. Using tweety more aggressively can result in read-only Twitter account restrictions.

## Cost Estimate

AWS free tier covers:
- Lambda: 1M requests/month
- DynamoDB: 25GB + 25 read/write units
- EventBridge: 1M events/month

Estimated cost: **$0/month** for typical usage.
