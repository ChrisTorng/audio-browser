import time
from fastapi.testclient import TestClient

def test_search_latency_performance(client: TestClient):
    start = time.time()
    r = client.get("/search", params={"term": "kick"})
    elapsed = time.time() - start
    assert r.status_code == 200
    # 目標 < 0.3 秒 — 目前未實作應失敗
    assert elapsed < 0.3
