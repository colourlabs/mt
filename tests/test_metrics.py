import asyncio
import pytest
import pytest_asyncio

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from mt.routes import setup_routes

class MockConfig:
    def __init__(self):
        self.port = 8080
        self.replica_timeout = 60
        self.host = "127.0.0.1"
        
@pytest_asyncio.fixture
def mock_config():
    return MockConfig()

@pytest_asyncio.fixture
async def test_client(mock_config):
    app = web.Application()
    app["config"] = mock_config
    setup_routes(app)

    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    resp = await test_client.get("/health")
    assert resp.status == 200
    json_data = await resp.json()
    assert json_data["status"] == "success"

@pytest.mark.asyncio
async def test_push_metrics_missing_data(test_client):
    resp = await test_client.post("/push", json={})
    assert resp.status == 400
    data = await resp.json()
    assert "error" in data["status"]

@pytest.mark.asyncio
async def test_push_and_metrics_flow(test_client):
    payload = {
        "replica_id": "replica-test",
        "metrics": {"cpu_usage": 0.5, "mem_usage": 0.3}
    }
    resp = await test_client.post("/push", json=payload)
    assert resp.status == 200

    resp = await test_client.get("/metrics")
    assert resp.status == 200
    text = await resp.text()
    assert "cpu_usage" in text
    assert "mem_usage" in text

@pytest.mark.asyncio
async def test_multiple_replicas_push_and_metrics_flow_concurrent(test_client):
    replicas = [
        {"replica_id": "replica-1", "metrics": {"cpu_usage": 0.1, "mem_usage": 0.2}},
        {"replica_id": "replica-2", "metrics": {"cpu_usage": 0.3, "mem_usage": 0.4}},
        {"replica_id": "replica-3", "metrics": {"cpu_usage": 0.5, "mem_usage": 0.6}},
        {"replica_id": "replica-4", "metrics": {"cpu_usage": 0.5, "mem_usage": 0.6}},
        {"replica_id": "replica-5", "metrics": {"cpu_usage": 0.5, "mem_usage": 0.6}},
        {"replica_id": "replica-6", "metrics": {"cpu_usage": 0.5, "mem_usage": 0.6}},
    ]

    coros = [test_client.post("/push", json=replica) for replica in replicas]

    responses = await asyncio.gather(*coros)

    for resp in responses:
        assert resp.status == 200

    resp = await test_client.get("/metrics")
    assert resp.status == 200
    text = await resp.text()

    for replica in replicas:
        assert replica["replica_id"] in text
        for metric_name, metric_value in replica["metrics"].items():
            assert str(metric_value) in text