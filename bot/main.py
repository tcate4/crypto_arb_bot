"""Entry‑point.  *python -m bot.main* inside the container."""
import asyncio, logging, decimal, os, gc, time, psutil
from decimal import Decimal
from cryptofeed import FeedHandler
from cryptofeed.defines import L2_BOOK, BID, ASK
from cryptofeed.exchanges import Coinbase, Kraken, OKX
from .edge_detector import EdgeDetector
from .exchange_factory import make_exchange
from .config import settings
import threading
from flask import Flask, jsonify

# Configure logging to file for better monitoring on VPS
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'arbitrage_bot.log')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

decimal.getcontext().prec = 12

class ArbitrageBot:
    def __init__(self):
        self.edge_detector = EdgeDetector(self.on_edge)
        self.exchanges = {}
        self.last_gc_time = time.time()
        self.last_memory_log = time.time()
        self.memory_threshold_mb = 500  # Trigger GC if memory usage exceeds this value
        self.process = psutil.Process(os.getpid())

    async def start(self):
        # spin up authenticated ccxt instances
        for name in settings.EXCHANGES:
            self.exchanges[name] = await make_exchange(name)
        # start cryptofeed
        fh = FeedHandler()
        for ex_cls in [Coinbase, Kraken, OKX]:
            name = ex_cls.id.lower()
            if name not in settings.EXCHANGES:
                continue
            fh.add_feed(ex_cls(max_depth=1,
                               channels=[L2_BOOK],
                               symbols=settings.SYMBOLS,
                               callbacks={L2_BOOK: self._book_cb(name)}))
        loop = asyncio.get_event_loop()
        loop.create_task(fh.run_forever())
        logging.info("FeedHandler started; waiting for data…")

    def _book_cb(self, exchange_name):
        def cb(symbol, book, ts, receipt):
            bid = book[BID][0][0]
            ask = book[ASK][0][0]
            self.edge_detector.update(exchange_name, symbol, bid, ask)
        return cb

    async def on_edge(self, symbol: str, src: str, dst: str, ask: float, bid: float, edge: float):
        logging.info(f"EDGE {edge*100:.2f}% {src}->{dst} {symbol}: buy {ask} sell {bid}")
        size_quote = Decimal(settings.SIZE_USD) / Decimal(ask)
        try:
            exch_src = self.exchanges[src]
            exch_dst = self.exchanges[dst]
            # place IOC orders (simplified)
            buy = await exch_src.create_order(symbol.replace('-', '/'), 'limit', 'buy', float(size_quote), ask, {'timeInForce': 'IOC'})
            sell = await exch_dst.create_order(symbol.replace('-', '/'), 'limit', 'sell', float(size_quote), bid, {'timeInForce': 'IOC'})
            logging.info(f"Filled buy={buy['status']} sell={sell['status']}")
        except Exception as e:
            logging.error(f"Trade failed: {e}")

async def main():
    bot = ArbitrageBot()
    await bot.start()
    # keep running
    while True:
        await asyncio.sleep(60)

# Initialize Flask app for health check
app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

def run_health():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start Flask in a background thread
    threading.Thread(target=run_health, daemon=True).start()
    # Start the main bot
    asyncio.run(main())
