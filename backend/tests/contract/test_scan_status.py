from fastapi.testclient import TestClient

def test_scan_status_contract(client: TestClient):
    resp = client.get("/scan/status")
    # 預期最終為 200 返回進度資訊 — 現在未實作應失敗
    assert resp.status_code == 200
