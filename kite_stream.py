from kiteconnect import KiteTicker
import logging
import time
import json

API_KEY = "your_api_key_here"
ACCESS_TOKEN = "your_access_token_here"  

logging.basicConfig(level=logging.DEBUG)

kws = KiteTicker(API_KEY, ACCESS_TOKEN)

INSTRUMENTS = [738561, 256265]



def on_ticks(ws, ticks):
    """Receives live market data"""
    logging.info("📈 Ticks: %s", json.dumps(ticks, indent=2))


def on_connect(ws, response):
    """Subscribes after connection is established"""
    logging.info("✅ Connected: %s", response)
    ws.subscribe(INSTRUMENTS)
    ws.set_mode(ws.MODE_FULL, INSTRUMENTS)


def on_close(ws, code, reason):
    """Handles unexpected close"""
    logging.warning("⚠️ Connection closed: Code=%s Reason=%s", code, reason)


def on_error(ws, code, reason):
    """Handles errors"""
    logging.error("❌ Error: Code=%s Reason=%s", code, reason)


def on_reconnect(ws, attempts_count):
    """Handles automatic reconnection"""
    logging.info("🔄 Reconnecting... Attempt #%s", attempts_count)


def on_noreconnect(ws):
    """If reconnection fails permanently"""
    logging.critical("🚨 Reconnection failed. Exiting...")



kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.on_error = on_error
kws.on_reconnect = on_reconnect
kws.on_noreconnect = on_noreconnect



if __name__ == "__main__":
    while True:
        try:
            logging.info("🚀 Starting Kite WebSocket...")
            kws.connect(threaded=False, disable_ssl_verification=True)
        except Exception as e:
            logging.error("💥 Exception in WebSocket: %s", e)
            time.sleep(5)  
