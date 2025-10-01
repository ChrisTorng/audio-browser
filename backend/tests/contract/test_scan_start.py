from fastapi.testclient import TestClient

def test_scan_start_contract(client: TestClient):
    resp = client.post("/scan/start")
    # 預期最終為 202 (掃描啟動接受) — 目前未實作應失敗
    assert resp.status_code == 202
