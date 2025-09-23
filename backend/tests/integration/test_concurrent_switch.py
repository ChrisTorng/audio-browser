from fastapi.testclient import TestClient

def test_concurrent_switch_playback(client: TestClient):
    # 快速切換播放：此處僅模擬多個請求
    ids = ["id1", "id2", "id3"]
    for _id in ids:
        r = client.get(f"/files/{_id}/waveform")
        assert r.status_code == 200
