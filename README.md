# Audio Browser

大量音頻瀏覽、即時播放、波形快取與標記搜尋工具。

> 目標：在單機環境中，快速瀏覽指定根資料夾（含子層）下的短音檔，透過鍵盤操作即時切換播放、觀看波形，並對音檔加上星級與描述以利後續搜尋與篩選。

---
## ✨ 核心功能概述
- 遞迴掃描使用者指定根資料夾 (WAV / MP3 / FLAC / OGG / AAC)
- 自動建立資料夾 / 檔案樹狀結構（延遲載入避免卡頓）
- 缺少對應波形 PNG 時於背景生成（與音檔同資料夾、同檔名副檔名改為 `.png`）
- 即時播放：切換時自動停止前一檔避免重疊
- 鍵盤導覽：上下方向鍵瀏覽，Enter 播放，支援展開 / 收合
- 星級 (0–5) 與描述標記，使用本地 SQLite 永續儲存
- 全文搜尋：檔名（含路徑片段）+ 描述，並可組合星級篩選 (>= 指定值)
- 統計資訊：格式分佈、星級分佈
- 不支援或損毀檔案計數與略過處理

> 部分延伸項 (Roadmap)：排序（名稱 / 星級）、長音檔抽樣波形、保留 UI 展開狀態。

---
## 🧱 系統架構 (Overview)
為避免中文字寬度在等寬字型中造成 ASCII 圖錯位，下方架構圖僅使用 ASCII；中文補充說明置於圖後。
```
+---------------------+        +----------------------------+
| Frontend (TS)       |  REST  | FastAPI Backend            |
|  - Tree UI          +------->+  - /scan /files ...        |
|  - Player / Waveform|        |  - Waveform generation     |
|  - Search / Rating  |        |  - SQLite persistence      |
+---------------------+        +---------------+------------+
                                                 |
                                                 | File system scan
                                                 v
                                     Audio folders + waveform PNG
```
中文對應：
- Player / Waveform = 播放器與波形顯示
- Search / Rating = 搜尋與星級 / 描述標記
- SQLite persistence = 星級與描述等資料永續儲存
- File system scan = 檔案系統遞迴掃描，缺少波形則背景生成

### 主要元件
- `backend/`：FastAPI 服務（掃描、搜尋、統計、標記、波形檢查/生成）
- `frontend/`：純 TypeScript UI（目前無框架，使用原生/輕量模組）
- `specs/`：需求與規格文件 (例如 `specs/001-/spec.md`)
- `docs/`：API 與手動測試說明
- `waveforms/`：歷史集中式波形放置目錄（未來轉為與音檔同資料夾策略；新策略已說明於需求）

---
## 🚀 快速開始 (Quick Start)
> 需求：Python 3.11+、Node.js (建議 18+)。

### 1. 取得原始碼
```bash
git clone <YOUR_FORK_OR_THIS_REPO_URL> audio-browser
cd audio-browser
```

### 2. 啟動 Backend
建立虛擬環境並安裝相依套件：
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

啟動服務 (預設 http://127.0.0.1:8000)：
```bash
uvicorn src.main:app --reload
```

健康檢查：
```bash
curl http://127.0.0.1:8000/health
```

### 3. 啟動 Frontend
在另一個終端：
```bash
cd frontend
npm install
npm run dev
```
> 目前 `dev` 僅啟動 TypeScript 編譯監聽；整合到實際靜態頁面伺服可依需求新增（例如使用簡易 `python -m http.server` 或任意靜態伺服工具）。

### 4. 開始掃描
呼叫掃描啟動：
```bash
curl -X POST http://127.0.0.1:8000/scan/start -H 'Content-Type: application/json' -d '{}'
```
查詢掃描狀態：
```bash
curl http://127.0.0.1:8000/scan/status
```

> 根資料夾的設定方式：目前程式碼尚未在 README 指定參數化方式；若預計支援環境變數或啟動參數，將於 Roadmap 中追蹤。暫時可在服務端程式碼中硬編路徑或後續 PR 改為設定檔 / .env。

### 5. 取得檔案樹 / 搜尋 範例
```bash
curl 'http://127.0.0.1:8000/files/tree?path='
curl 'http://127.0.0.1:8000/search?term=kick&minStars=3'
```

---
## 🔎 API 快速對照
精簡列表（詳見 `docs/api.md` 與 `specs/001-/contracts/audio-api.yaml`）：
- POST `/scan/start`：啟動或重新掃描
- GET `/scan/status`：掃描進度
- GET `/files/tree?path=...`：取得資料夾節點
- GET `/files/list?folder=...&minStars=&q=`：檔案列表 + 搜尋 / 星級過濾
- GET `/files/{id}/waveform`：回傳或觸發波形 PNG
- PUT `/files/{id}/rating`：設定星級
- PUT `/files/{id}/description`：設定描述
- GET `/search?term=...&minStars=`：全文搜尋 + 星級
- GET `/stats`：統計資訊

---
## 🗄️ 資料模型 (節錄)
`AudioFile`（詳見 `backend/src/models/audio_file.py`）：
- `id`：路徑雜湊
- `relative_path` / `display_name`
- `format` / `duration_seconds` / `file_size`
- `waveform_png_path`：同資料夾同檔名 `.png`
- `star_rating` (0–5) / `description`
- `scan_status`：`active|skipped|unsupported`

---
## 🧪 測試與品質 (品質)
專案包含多層級測試：
- `tests/contract`：API 契約行為
- `tests/integration`：跨服務流程（播放、樹狀 / 搜尋互動）
- `tests/performance`：初次載入、搜尋延遲、播放延遲
- `tests/unit`：細部服務與處理（例如 Tokenizer、Waveform Service）

執行方式：
```bash
cd backend
pytest -q
```
> 可再依需求加入 coverage / CI 工作流程。

---
## 📁 專案結構 (節錄)
```
backend/
  src/
    api/         # FastAPI 路由
    models/      # Pydantic 資料模型與索引/偏好實體
    services/    # 掃描、搜尋、播放、波形、統計等服務層
frontend/
  src/
    components/  # UI 元件 (PlayerBar, TreeView, SearchFilter, WaveformView)
    lib/         # API 呼叫 / 鍵盤事件工具
    state/       # 簡易全域狀態 store
specs/           # 功能需求與規格文件
docs/            # API 與手動測試文件
```

---
## 🛣️ Roadmap (簡述)
| 項目 | 狀態 |
|------|------|
| 排序 (名稱 / 星級) | SHOULD – 待實作 |
| 長音檔抽樣波形策略 | SHOULD – 低優先 |
| 展開狀態持久化 | SHOULD – 規劃中 |
| 錯誤回應統一格式 / JSON Schema | 進行中 |
| 環境化根資料夾設定 (.env / CLI 參數) | 規劃中 |
| 前端打包與部署腳本 | 規劃中 |
| CI (Lint + Test + Coverage Badge) | 規劃中 |

---
## 🤝 貢獻指南
1. 建立分支：`feature/<短描述>`
2. 撰寫或更新對應規格 / 測試
3. 確保 `pytest` 全數通過
4. 發出 Pull Request，描述動機與測試涵蓋

建議：新增功能前先於 `specs/` 撰寫或更新對應規格檔，避免落差。

---
## ⚖️ 授權 (MIT License)
本專案採用 MIT 授權。你可自由使用、複製、修改、合併、發布、散布、再授權與/或販售本軟體的複本，惟需保留下列著作權與授權聲明。

```
MIT License

Copyright (c) 2025 Audio Browser Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> 建議另外新增根目錄 `LICENSE` 檔（可直接複製上方內容）。

---
## 📬 聯絡 / 問題回報
- 建議以 Issue 回報 Bug / 需求
- 提供：重現步驟、期望行為、實際結果、環境資訊

---
**狀態**：早期開發階段，介面與資料結構可能仍會調整。
