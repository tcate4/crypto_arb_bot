"""Runtime configuration pulled from environment variables.
   Coolify secrets inject API_KEYS_JSON at runtime.
"""
import json, os
from pathlib import Path

class Settings:
    EXCHANGES   = os.getenv("EXCHANGES", "coinbase,kraken,okx").split(",")
    SYMBOLS     = os.getenv("SYMBOLS", "BTC-USDT,ETH-USDT").split(",")
    API_KEYS    = json.loads(os.getenv("API_KEYS_JSON", "{}"))
    EDGE_THRESH = float(os.getenv("EDGE_THRESHOLD", 0.001))  # 0.1 %
    SIZE_USD    = float(os.getenv("ORDER_SIZE_USD", 50))      # test size

settings = Settings()
