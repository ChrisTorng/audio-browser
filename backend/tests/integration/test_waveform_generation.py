from fastapi.testclient import TestClient

def test_waveform_generation_flow(client: TestClient):
    # 要求 waveform → 若不存在應觸發生成並最終回 200
    r = client.get("/files/placeholder-id/waveform")
    assert r.status_code == 200
