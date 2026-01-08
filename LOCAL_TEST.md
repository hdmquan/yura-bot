# Local Testing

## Get Twitter Session Cookie

Open Twitter in browser, open DevTools (F12), go to Network tab, refresh page, click any twitter.com request, find Cookie header, copy entire value.

## Create Discord Webhook

Discord Server Settings > Integrations > Webhooks > New Webhook. Copy webhook URL.

## Setup

```bash
cp .env.example .env
```

Edit `.env`:

```
TWITTER_SESSION=your_cookie_here
DISCORD_WEBHOOK_URL=your_webhook_url
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

## Run

```bash
make setup
poetry run python -m src.handler
```

## State Management

Local mode uses `.state.json` file. Production mode uses DynamoDB. Bot chooses automatically based on AWS credentials.
