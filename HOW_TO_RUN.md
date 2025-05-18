# How to Run the Cryptocurrency Arbitrage Bot

This guide provides detailed instructions on how to run the cryptocurrency arbitrage bot on your system.

## Prerequisites

Before running the bot, you need:

1. **API Keys**: Obtain API keys from the exchanges you want to use (Coinbase, Kraken, OKX)
2. **Python**: Python 3.8 or higher installed on your system
3. **Git**: Git installed on your system (for cloning the repository)
4. **Docker** (optional): Docker and Docker Compose installed if you want to run the bot in a container

## Setting Up Environment Variables

The bot requires API keys to authenticate with the exchanges. These keys are provided as environment variables.

### On Windows (PowerShell)

1. Open PowerShell
2. Set the environment variables by running the following commands (replace with your actual API keys):

```powershell
$Env:COINBASE_KEY = "your_coinbase_api_key"
$Env:COINBASE_SECRET = "your_coinbase_api_secret"
$Env:KRAKEN_KEY = "your_kraken_api_key"
$Env:KRAKEN_SECRET = "your_kraken_api_secret"
$Env:OKX_KEY = "your_okx_api_key"  # Optional
$Env:OKX_SECRET = "your_okx_api_secret"  # Optional
```

Alternatively, you can run the provided script:

```powershell
# Navigate to the repository directory
cd path\to\crypto-arb-bot

# Edit kraken_api.txt to include your actual API keys
notepad kraken_api.txt

# Run the script to set environment variables
. .\kraken_api.txt
```

### On Windows (Command Prompt)

```cmd
set COINBASE_KEY=your_coinbase_api_key
set COINBASE_SECRET=your_coinbase_api_secret
set KRAKEN_KEY=your_kraken_api_key
set KRAKEN_SECRET=your_kraken_api_secret
set OKX_KEY=your_okx_api_key
set OKX_SECRET=your_okx_api_secret
```

## Running the Bot Locally

### Method 1: Using the Simple Bot (bot.py)

1. Clone the repository (if you haven't already):
   ```
   git clone https://github.com/yourusername/crypto-arb-bot.git
   cd crypto-arb-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables as described above

4. Run the bot:
   ```
   python bot.py
   ```

### Method 2: Using the Advanced Bot (bot/main.py)

1. Clone the repository (if you haven't already):
   ```
   git clone https://github.com/yourusername/crypto-arb-bot.git
   cd crypto-arb-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables as described above

4. Run the bot:
   ```
   python -m bot.main
   ```

## Running the Bot with Docker

1. Clone the repository (if you haven't already):
   ```
   git clone https://github.com/yourusername/crypto-arb-bot.git
   cd crypto-arb-bot
   ```

2. Create a `.env` file in the repository root with your API keys:
   ```
   COINBASE_KEY=your_coinbase_api_key
   COINBASE_SECRET=your_coinbase_api_secret
   KRAKEN_KEY=your_kraken_api_key
   KRAKEN_SECRET=your_kraken_api_secret
   OKX_KEY=your_okx_api_key
   OKX_SECRET=your_okx_api_secret
   ```

3. Run the bot using Docker Compose:
   ```
   docker-compose up -d
   ```

4. Check the logs:
   ```
   docker-compose logs -f
   ```

## Configuring the Bot

The bot's behavior can be configured by editing the `config.yaml` file:

- **exchanges**: Configure the exchanges you want to use, their fees, and environment variable names
- **symbols**: List of trading pairs to monitor
- **poll_interval_ms**: How often to check for arbitrage opportunities (in milliseconds)
- **profit_threshold**: Minimum profit percentage required to execute a trade
- **risk_factor**: Percentage of available balance to use for each trade

Example:
```yaml
exchanges:
  coinbase:
    fee: 0.006
    key_env: COINBASE_KEY
    secret_env: COINBASE_SECRET
  kraken:
    fee: 0.0026
    key_env: KRAKEN_KEY
    secret_env: KRAKEN_SECRET
symbols:
  - BTC/USDT
  - ETH/USDT
  - XRP/USDT
poll_interval_ms: 5000
profit_threshold: 0.005
risk_factor: 0.5
```

## Monitoring the Bot

The bot provides a health check endpoint at `http://localhost:8000/health` that returns a JSON response with status "ok" if the bot is running.

You can also check the bot's logs:
- For local runs: Check the console output and the `bot.log` file
- For Docker runs: Use `docker-compose logs -f`

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly set as environment variables
2. **Missing Dependencies**: Make sure you've installed all required packages with `pip install -r requirements.txt`
3. **Exchange Connection Issues**: Check your internet connection and firewall settings
4. **Permission Denied**: Run PowerShell or Command Prompt as Administrator if you encounter permission issues

### Getting Help

If you encounter issues not covered in this guide, please:
1. Check the project's GitHub repository for issues and discussions
2. Consult the exchange's API documentation for specific API-related issues
