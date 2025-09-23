from fastapi.testclient import TestClient

def test_persistence_flow(client: TestClient):
    # 先寫入評價
    r1 = client.put("/files/placeholder-id/rating", json={"stars": 4})
    assert r1.status_code == 204
    # 寫入描述
    r2 = client.put("/files/placeholder-id/description", json={"description": "warm pad"})
    assert r2.status_code == 204
    # 再次查詢檔案列表驗證資料 (最終需 API 支援列表帶 annotation)
    r3 = client.get("/files/list")
    assert r3.status_code == 200
