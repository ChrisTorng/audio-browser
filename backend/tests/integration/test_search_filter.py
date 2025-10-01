from fastapi.testclient import TestClient

def test_search_filter_flow(client: TestClient):
    # 搜尋 + 星級篩選 (最終應成功)
    r = client.get("/search", params={"term": "snare", "minStars": 4})
    assert r.status_code == 200
