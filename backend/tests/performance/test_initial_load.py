import time
from fastapi.testclient import TestClient

def test_initial_load_performance(client: TestClient):
    start = time.time()
    r = client.get("/files/tree")
    elapsed = time.time() - start
    assert r.status_code == 200
    # 預期目標 < 2 秒 — 現階段失敗可接受 (尚未實作)
    assert elapsed < 2.0
