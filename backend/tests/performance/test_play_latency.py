import time
from fastapi.testclient import TestClient

def test_play_latency_performance(client: TestClient):
    start = time.time()
    r = client.get("/files/placeholder-id/waveform")
    elapsed = time.time() - start
    assert r.status_code == 200
    # 目標 < 0.1 秒 — 目前未實作應失敗
    assert elapsed < 0.1
