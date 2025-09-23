from fastapi.testclient import TestClient

def test_files_list_contract(client: TestClient):
    resp = client.get("/files/list")
    # 預期最終為 200 — 現在應失敗
    assert resp.status_code == 200
