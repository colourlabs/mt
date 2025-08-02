import time
from aiohttp import web
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from mt.state import replica_metrics, metrics_lock, registry, gauges

async def push_metrics(request):
    data = await request.json()
    replica_id = data.get("replica_id")
    metrics = data.get("metrics")

    if not replica_id or not isinstance(metrics, dict):
        return web.json_response({"status": "error", "message": "missing replica_id or metrics dict"}, status=400)

    now = time.time()

    async with metrics_lock:
        replica_metrics[replica_id] = {
            "timestamp": now,
            "metrics": metrics,
        }

    return web.json_response({"status": "success"})

async def metrics(request):
    now = time.time()
    inactive_cutoff = now - request.app["config"].replica_timeout

    async with metrics_lock:
        for replica_id in list(replica_metrics):
            if replica_metrics[replica_id]["timestamp"] < inactive_cutoff:
                del replica_metrics[replica_id]

        active_replicas = set(replica_metrics.keys())

        for metric_name, gauge in gauges.items():
            for replica_id in list(gauge._metrics.keys()):
                if replica_id not in active_replicas:
                    try:
                        gauge.remove(replica_id)
                    except KeyError:
                        pass

        for replica_id, entry in replica_metrics.items():
            metrics = entry["metrics"]
            for metric_name, value in metrics.items():
                if metric_name not in gauges:
                    gauges[metric_name] = Gauge(
                        metric_name,
                        f"metric {metric_name}",
                        ['replica_id'],
                        registry=registry,
                    )
                gauges[metric_name].labels(replica_id=replica_id).set(float(value))

    data = generate_latest(registry)
    return web.Response(body=data, headers={"Content-Type": CONTENT_TYPE_LATEST})
