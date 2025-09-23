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

def test_files_rating_contract(client: TestClient):
    client.post("/scan/start")
    assert _wait_for_scan(client)
    files = client.get("/files/list").json()
    fid = files[0]["id"]
    resp = client.put(f"/files/{fid}/rating", json={"stars": 5})
    assert resp.status_code == 200
