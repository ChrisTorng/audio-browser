# Research - 大量音頻瀏覽與標記搜尋功能

## Unknowns & Research Tasks
| Topic | Question | Status | Notes |
|-------|----------|--------|-------|
| Python Web Framework | FastAPI vs Flask 對於 async I/O 與型別提示 | OPEN | FastAPI 可能較佳 (內建 OpenAPI) |
| 波形生成策略 | 取樣密度、是否預先或延後計算 | PARTIAL | MP3 短檔：掃描時若無 png 直接生成；長檔抽樣延後 (目前不急) |
| 前端框架選擇 | 原生 TS + Web Components vs React/Vue | OPEN | 偏向原生 + 輕量 store |
| 前端測試工具 | Jest + Playwright or Vitest? | OPEN | End-to-end 需 Playwright |
| 抽樣密度標準 | 長音檔 > 2hr 如何抽樣 | DEFERRED | 短檔為主，延後定義 |
| 排序欄位 | 除名稱、星級外是否需時間/大小排序 | OPEN | 目前名稱/星級優先 |
| 展開狀態持久化 | 是否需保留使用者展開樹狀 | DEFERRED | 可由 UserPreference 延後實作 |
| 非 UTF-8 編碼 | 轉碼/顯示策略 | DECIDED | 不處理，假設英數字 |
| 星級/描述儲存 | 僅 SQLite 本地 or 可同步? | DECIDED | SQLite 本地，未來可擴充同步 |
| 波形快取格式 | 二進位 blob or JSON array | PARTIAL | 先產出 PNG 檔案，必要時再加抽樣資料 |
| 最大層級限制 | 是否需要限制深度 | DECIDED | 不需要，檔案量小 |
| 波形進度顯示 | 是否需要進度條 | DECIDED | 不需要，短檔快速完成 |

## Decisions
### 波形 PNG 預先生成 (MP3)
Decision: 掃描 MP3 缺少 png 時立即生成。
Rationale: 短檔案生成快速，改善首次瀏覽體驗。
Alternatives: 延遲至首次點擊 (放棄：會增加首播延遲)。

### 不實作進度顯示
Decision: 不顯示進度條。
Rationale: 短檔生成可忽略延遲。
Alternatives: 動態進度 UI (過度設計)。

### 不處理複雜檔名正規化
Decision: 英數字假設成立，不做轉碼。
Rationale: 減少不必要處理成本。
Alternatives: 全面轉碼/正規化 (無立即需求)。

### SQLite 儲存星級與描述
Decision: 僅本地 SQLite。
Rationale: 簡化初版，資料量小。
Alternatives: 雲同步 (延後，待需求確認)。

## Deferred Items
- 長音檔抽樣密度策略
- 展開狀態持久化細節
- 排序欄位擴充（建立時間/大小）
- 波形內部抽樣資料格式（若 PNG 不足）

## Methodology
完成各研究後以 Decision / Rationale / Alternatives 格式追加於此。

## Pending
只剩 OPEN/DEFERRED 項需於後續研究或下一里程碑釐清。
