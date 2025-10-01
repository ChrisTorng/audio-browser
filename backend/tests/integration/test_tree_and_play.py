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

def test_tree_and_play_flow(client: TestClient):
    r1 = client.post("/scan/start")
    assert r1.status_code == 202
    assert _wait_for_scan(client)
    r3 = client.get("/files/tree")
    assert r3.status_code == 200
    files = client.get("/files/list").json()
    first_id = files[0]["id"]
    r4 = client.get(f"/files/{first_id}/waveform")
    assert r4.status_code == 200
