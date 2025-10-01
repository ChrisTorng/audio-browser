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

def test_persistence_flow(client: TestClient):
    client.post("/scan/start")
    assert _wait_for_scan(client)
    files = client.get("/files/list").json()
    fid = files[0]["id"]
    r1 = client.put(f"/files/{fid}/rating", json={"stars": 4})
    assert r1.status_code == 200
    r2 = client.put(f"/files/{fid}/description", json={"description": "warm pad"})
    assert r2.status_code == 200
    r3 = client.get("/files/list")
    assert r3.status_code == 200
