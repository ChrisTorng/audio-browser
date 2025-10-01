from fastapi.testclient import TestClient
import time

def _wait_for_scan(client: TestClient, timeout=3):
    start = time.time()
    while time.time() - start < timeout:
        st = client.get("/scan/status").json()
        if not st.get("running") and st.get("total", 0) > 0 and st.get("progress") == st.get("total"):
            return True
        time.sleep(0.05)
    return False

def test_concurrent_switch_playback(client: TestClient):
    client.post("/scan/start")
    assert _wait_for_scan(client)
    files = client.get("/files/list").json()
    ids = [f["id"] for f in files][:3]
    for fid in ids:
        r = client.get(f"/files/{fid}/waveform")
        assert r.status_code == 200
