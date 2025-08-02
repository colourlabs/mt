import asyncio
import signal
from aiohttp import web
from mt.routes import setup_routes
from mt.utils.logger import setup_logger
from mt.utils.config import Config

logger = setup_logger()
config = Config()

async def main():
    app = web.Application()
    setup_routes(app)

    app["config"] = config

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, config.host, config.port)
    await site.start()

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _shutdown():
        logger.info("received shutdown signal")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _shutdown)

    logger.info(f"starting mt on {config.host}:{config.port}")
    await stop_event.wait()

    logger.info("shutting down...")
    try:
        await asyncio.wait_for(runner.cleanup(), timeout=10.0)
    except asyncio.TimeoutError:
        logger.warning("shutdown timed out, forcing exit")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"fatal error on startup: {e}")
