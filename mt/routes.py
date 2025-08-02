from aiohttp import web
from mt.metrics import push_metrics, metrics

async def health(request):
    return web.json_response({"status": "success"})

def setup_routes(app: web.Application):
    app.router.add_post("/push", push_metrics)
    app.router.add_get("/metrics", metrics)
    app.router.add_get("/health", health)