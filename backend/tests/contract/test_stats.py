from fastapi.testclient import TestClient

def test_stats_contract(client: TestClient):
    resp = client.get("/stats")
    # 最終預期 200 — 現在應失敗
    assert resp.status_code == 200
