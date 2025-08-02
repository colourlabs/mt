import asyncio
from prometheus_client import CollectorRegistry

replica_metrics = {}
metrics_lock = asyncio.Lock()
registry = CollectorRegistry()
gauges = {}
