# API 說明 (Draft)

> 與 `specs/001-/contracts/audio-api.yaml` 對應；此文件提供快速參考。

## Endpoints

### POST /scan/start
啟動或重新啟動掃描。
- Response 202: `{ "status": "started" }`

### GET /scan/status
回傳掃描進度。
- Response 200 範例：
```json
{ "running": false, "progress": 120, "total": 120 }
```

### GET /files/tree?path=relative/folder
惰性取得資料夾節點。
- Response 200: 節點清單 (未定 schema 詳細，後續補充)

### GET /files/list?folder=path&minStars=3&q=term
取得特定資料夾檔案列表，可附搜尋 / 星級過濾。
- Response 200: `[AudioFileLite, ...]`

### GET /files/{id}/waveform
取得或生成對應 PNG，相對路徑。
- Response 200: `{ "waveformPath": "relative/path/to.png" }`

### PUT /files/{id}/rating
更新星級。
- Request: `{ "stars": 4 }`
- Response 204

### PUT /files/{id}/description
更新描述。
- Request: `{ "description": "..." }`
- Response 204

### GET /search?term=kick&minStars=3
全文搜尋 + 星級過濾。
- Response 200 範例：
```json
{ "query": "kick", "results": [{"id": "...", "display_name": "kick.mp3" }] }
```

### GET /stats
取得統計資訊（格式 / 星級分佈）。
- Response 200 範例：
```json
{ "formats": {"mp3": 10, "wav": 2}, "stars": {"5": 3, "4": 1} }
```

## 型別（部分）
`AudioFile` 參照 `backend/src/models/audio_file.py`。

## 待補 (T066 完成後目標)
- 更精確 JSON Schema
- Error 回應格式統一
- 範例錯誤案例 (404, 422)
- 前端呼叫程式碼片段
