import time
from fastapi.testclient import TestClient

def _wait_for_scan(client: TestClient, timeout=3):
    start = time.time()
    while time.time() - start < timeout:
        st = client.get("/scan/status").json()
        if not st.get("running") and st.get("total", 0) > 0 and st.get("progress") == st.get("total"):
            return True
        time.sleep(0.02)
    return False

def test_play_latency_performance(client: TestClient):
    client.post("/scan/start")
    assert _wait_for_scan(client)
    files = client.get("/files/list").json()
    fid = files[0]["id"]
    start = time.time()
    r = client.get(f"/files/{fid}/waveform")
    elapsed = time.time() - start
    assert r.status_code == 200
    # 目標 < 0.1 秒（僅 placeholder 實作，仍應非常快）
    assert elapsed < 0.1
