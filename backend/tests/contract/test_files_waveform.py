from fastapi.testclient import TestClient

def test_files_waveform_contract(client: TestClient):
    resp = client.get("/files/placeholder-id/waveform")
    # 預期最終為 200 (回應波形或生成狀態) — 現在應失敗
    assert resp.status_code == 200
