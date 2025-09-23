from fastapi.testclient import TestClient

def test_files_description_contract(client: TestClient):
    resp = client.put("/files/placeholder-id/description", json={"description": "sample"})
    # 最終預期 204 — 現在應失敗
    assert resp.status_code == 204
