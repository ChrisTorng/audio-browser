from fastapi.testclient import TestClient

def test_tree_and_play_flow(client: TestClient):
    # 1. 啟動掃描
    r1 = client.post("/scan/start")
    assert r1.status_code == 202
    # 2. 查詢狀態 (最終 200 with progress)
    r2 = client.get("/scan/status")
    assert r2.status_code == 200
    # 3. 取得根目錄樹
    r3 = client.get("/files/tree")
    assert r3.status_code == 200
    # 4. 選取第一個檔案並請求 waveform
    r4 = client.get("/files/placeholder-id/waveform")
    assert r4.status_code == 200
