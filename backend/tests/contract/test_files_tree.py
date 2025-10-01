from fastapi.testclient import TestClient

def test_files_tree_contract(client: TestClient):
    resp = client.get("/files/tree")
    # 預期最終為 200 (樹狀資料) — 現在未實作應失敗
    assert resp.status_code == 200
