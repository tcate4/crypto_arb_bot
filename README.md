# Cryptocurrency Arbitrage Bot

This bot automatically detects and exploits price differences between different cryptocurrency exchanges, including Coinbase, Kraken, and others.

## Features

- Monitors price differences for cryptocurrency pairs across exchanges
- Calculates gross and net profit after accounting for exchange fees
- Executes trades when profit exceeds configurable threshold
- Manages risk based on available balances
- Provides health check endpoint for monitoring

## Configuration

The bot is configured via environment variables and a config.yaml file:

- `config.yaml`: Contains exchange fees, symbols to trade, polling interval, profit threshold, and risk factor
- Environment variables: API keys and secrets for exchanges

## Supported Exchanges

- Coinbase
- Kraken
- OKX

## Deployment on Digital Ocean

### Prerequisites

1. A GitHub account with this repository
2. A Digital Ocean account
3. API keys for the exchanges you want to use

### Deployment Steps

1. **Fork this repository to your GitHub account**

2. **Create a Digital Ocean App**
   - Log in to your Digital Ocean account
   - Go to Apps and click "Create App"
   - Select GitHub as the source
   - Connect your GitHub account and select this repository
   - Configure the app:
     - Type: Web Service
     - Resource: Basic ($5/month)
     - Region: Choose a region close to your exchanges' servers

3. **Set Environment Variables**
   - In the "Environment Variables" section, add the following:
     - `COINBASE_KEY`: Your Coinbase API key
     - `COINBASE_SECRET`: Your Coinbase API secret
     - `KRAKEN_KEY`: Your Kraken API key
     - `KRAKEN_SECRET`: Your Kraken API secret
     - `OKX_KEY`: Your OKX API key (if using)
     - `OKX_SECRET`: Your OKX API secret (if using)

4. **Deploy the App**
   - Click "Create and Deploy"
   - Digital Ocean will build and deploy your app

5. **Monitor the Bot**
   - Once deployed, you can monitor the bot's health by visiting the health endpoint:
     - `https://your-app-url/health`
   - You can also view logs in the Digital Ocean dashboard

### Updating the Bot

When you push changes to your GitHub repository, Digital Ocean can automatically redeploy your app:

1. Enable automatic deployments in your Digital Ocean App settings
2. Make changes to your local repository
3. Commit and push to GitHub
4. Digital Ocean will detect the changes and redeploy your app

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables (see kraken_api.txt for example)
4. Run the bot: `python bot.py` or `python -m bot.main`

## Docker Deployment

You can also run the bot using Docker:

```bash
docker-compose up -d
```

Make sure to set the environment variables in your shell or in a .env file before running docker-compose.
