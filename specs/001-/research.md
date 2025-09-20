# Research - 大量音頻瀏覽與標記搜尋功能

## Unknowns & Research Tasks
| Topic | Question | Status | Notes |
|-------|----------|--------|-------|
| Python Web Framework | FastAPI vs Flask 對於 async I/O 與型別提示 | OPEN | FastAPI 可能較佳 (內建 OpenAPI) |
| 波形生成策略 | 取樣密度、是否預先或延後計算 | OPEN | 需平衡初次載入時間 |
| 前端框架選擇 | 原生 TS + Web Components vs React/Vue | OPEN | 無需大型狀態時可輕量化 |
| 前端測試工具 | Jest + Playwright or Vitest? | OPEN | 需支援鍵盤互動測試 |
| 抽樣密度標準 | 長音檔 > 2hr 如何抽樣 | OPEN | 可能依秒數等距取樣 |
| 排序欄位 | 除名稱、星級外是否需時間/大小排序 | OPEN | 影響索引結構 |
| 展開狀態持久化 | 是否需保留使用者展開樹狀 | OPEN | 影響 UserPreference schema |
| 非 UTF-8 編碼 | 轉碼/顯示策略 | OPEN | 需決定 fallback 行為 |
| 星級/描述儲存 | 僅 SQLite 本地 or 可同步? | OPEN | 初期可本地，後期擴充同步 |
| 波形快取格式 | 二進位 blob or JSON array | OPEN | 影響前端載入速度 |

## Preliminary Decisions (Draft)
- (尚未確定，待研究完成後更新)

## Methodology
完成各研究後以 Decision / Rationale / Alternatives 格式追加於此。

## Pending
所有 OPEN 項目需在 Phase 0 結束前轉為 DECIDED 或標示延期策略。
