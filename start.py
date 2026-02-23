"""Start both bot and web server"""
import asyncio
import os
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from loguru import logger

class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_web_server():
    """Run web server in separate thread"""
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(("0.0.0.0", port), WebHandler)
    logger.info(f"🌐 Web server started on port {port}")
    server.serve_forever()

async def run_bot():
    """Run Telegram bot"""
    from main import main
    await main()

def start():
    """Start both services"""
    # Start web server in background thread
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Run bot in main thread
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

if __name__ == "__main__":
    start()
