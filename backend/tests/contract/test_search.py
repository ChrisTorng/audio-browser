from fastapi.testclient import TestClient

def test_search_contract(client: TestClient):
    resp = client.get("/search", params={"term": "kick"})
    # 最終預期 200 — 現在應失敗
    assert resp.status_code == 200
