import os, yaml, asyncio
import ccxt.async_support as ccxt
from loguru import logger
from flask import Flask, jsonify
import threading

# ——— Load config ———
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

EXCH_CFG   = cfg["exchanges"]
SYMBOLS    = cfg["symbols"]
INTERVAL   = cfg["poll_interval_ms"] / 1000
THRESHOLD  = cfg["profit_threshold"]
RISK       = cfg["risk_factor"]

# ——— Initialize exchange clients ———
async def init_exchanges():
    clients = {}
    for name, e in EXCH_CFG.items():
        cls = getattr(ccxt, name)
        clients[name] = cls({
            "apiKey":    os.getenv(e["key_env"]),
            "secret":    os.getenv(e["secret_env"]),
            "enableRateLimit": True
        })
    return clients

# ——— Fetch top-of-book ———
async def top_of_book(client, symbol):
    ob = await client.fetch_order_book(symbol, limit=1)
    bid = ob["bids"][0][0] if ob["bids"] else 0
    ask = ob["asks"][0][0] if ob["asks"] else float("inf")
    return bid, ask

# ——— Detect & execute ———
async def detect_and_execute(clients):
    for sx, cx in clients.items():
        for sy, cy in clients.items():
            if sx == sy: continue
            fee_x = EXCH_CFG[sx]["fee"]
            fee_y = EXCH_CFG[sy]["fee"]
            for symbol in SYMBOLS:
                bid_x, _ = await top_of_book(cx, symbol)
                _, ask_y = await top_of_book(clients[sy], symbol)
                gross  = bid_x/ask_y - 1
                net    = gross - (fee_x + fee_y)
                if net >= THRESHOLD:
                    # get balances
                    bal_x = (await cx.fetch_balance())[symbol.split("/")[0]]["free"]
                    bal_y = (await clients[sy].fetch_balance())[symbol.split("/")[1]]["free"] / ask_y
                    size  = min(bal_x, bal_y) * RISK
                    if size <= 0: continue

                    # place both orders concurrently
                    buy  = cx.create_limit_buy_order(symbol, size, ask_y)
                    sell = clients[sy].create_limit_sell_order(symbol, size, bid_x)
                    results = await asyncio.gather(buy, sell, return_exceptions=True)
                    logger.info(f"Arb {symbol} via {sy}→{sx}: size={size:.6f}, net%={net:.3%}")
                    logger.debug(results)

# ——— Main loop ———
async def main():
    clients = await init_exchanges()
    try:
        while True:
            await detect_and_execute(clients)
            await asyncio.sleep(INTERVAL)
    finally:
        for c in clients.values():
            await c.close()

# Initialize Flask app
app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

def run_health():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    logger.add("bot.log", rotation="10 MB")

    # start Flask in a background thread
    threading.Thread(target=run_health, daemon=True).start()

    # start the main bot
    asyncio.run(main())
