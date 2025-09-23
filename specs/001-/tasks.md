# Tasks: 大量音頻瀏覽與標記搜尋功能

**Input**: Design documents from `/specs/001-/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md

## Phase 3.1: Setup
- [x] T001 建立專案目錄結構 backend/ 與 frontend/（含 src/, tests/ 子目錄）
- [x] T002 初始化 backend Python 專案 (pyproject/requirements) 選定 FastAPI + uvicorn + pydantic
- [x] T003 初始化 frontend TypeScript 專案 (tsconfig, package.json)（原生 TS + minimal build 工具）
- [x] T004 [P] 設定共用程式碼格式與 Lint (black, isort, ruff, eslint, prettier)
- [x] T005 建立 SQLite 初始化腳本 (backend/src/models/db_init.py) 僅建立評價與描述相關表
- [x] T006 設定 .env.example (ROOT_AUDIO_DIR, DATABASE_URL)

## Phase 3.2: Tests First (TDD) ⚠️ MUST FAIL INITIALLY
**Contract / Schema / Integration / 性能基準骨架**
- [x] T007 產生測試資料夾 tests/contract/ + tests/integration/ + tests/performance/
- [x] T008 [P] Contract Test: POST /scan/start (tests/contract/test_scan_start.py)
- [x] T009 [P] Contract Test: GET /scan/status (tests/contract/test_scan_status.py)
- [x] T010 [P] Contract Test: GET /files/tree (tests/contract/test_files_tree.py)
- [x] T011 [P] Contract Test: GET /files/list (tests/contract/test_files_list.py)
- [x] T012 [P] Contract Test: GET /files/{id}/waveform (tests/contract/test_files_waveform.py)
- [x] T013 [P] Contract Test: PUT /files/{id}/rating (tests/contract/test_files_rating.py)
- [x] T014 [P] Contract Test: PUT /files/{id}/description (tests/contract/test_files_description.py)
- [x] T015 [P] Contract Test: GET /search (tests/contract/test_search.py)
- [x] T016 [P] Contract Test: GET /stats (tests/contract/test_stats.py)
- [x] T017 Integration Test: 樹狀展開與播放流程 (tests/integration/test_tree_and_play.py)
- [x] T018 Integration Test: 搜尋 + 星級篩選 (tests/integration/test_search_filter.py)
- [x] T019 Integration Test: 星級與描述持久化 (tests/integration/test_persistence.py)
- [x] T020 Integration Test: 波形預先生成與占位符 (tests/integration/test_waveform_generation.py)
- [x] T021 Integration Test: 快速切換播放無重疊 (tests/integration/test_concurrent_switch.py)
- [x] T022 Performance Baseline Test: 初次載入 <2s (tests/performance/test_initial_load.py)
- [x] T023 Performance Baseline Test: 播放啟動 <100ms (tests/performance/test_play_latency.py)
- [x] T024 Performance Baseline Test: 搜尋回應 <300ms (tests/performance/test_search_latency.py)

## Phase 3.3: Core Models & Index (ONLY after 3.2 written & failing)
- [x] T025 [P] Model: 建立 AudioFile 資料結構 (backend/src/models/audio_file.py)
- [x] T026 [P] Model: 建立 FolderNode 結構 (backend/src/models/folder_node.py)
- [x] T027 [P] Model: 建立 UserPreference 結構 (backend/src/models/user_preference.py)
- [x] T028 [P] Model: 建立 SearchIndex 結構 (backend/src/models/search_index.py)
- [x] T029 建立 DB schema (backend/src/models/schema.py)（含星級/描述表 + 索引基底）
- [x] T030 實作索引 tokenization 函式 (backend/src/lib/tokenizer.py)

## Phase 3.4: Services Layer
- [x] T031 掃描服務：遞迴取得 MP3/其他支援格式 (backend/src/services/scan_service.py)
- [x] T032 波形服務：MP3 無 PNG 時生成並快取 (backend/src/services/waveform_service.py)
 - [x] T032A 波形服務調整：改為於音檔相同資料夾生成同檔名 .png（取代集中 waveforms/ 目錄），更新 FR-004 與實作（需調整 `waveform_service.py` 與 API 回傳路徑）。
- [x] T033 檔案樹服務：惰性載入節點 (backend/src/services/tree_service.py)
- [x] T034 播放/Metadata 服務：取得檔案路徑與基本屬性 (backend/src/services/playback_service.py)
 - [x] T035 標記服務：星級與描述讀寫 (backend/src/services/annotation_service.py)
 - [x] T036 搜尋服務：依 token + 星級過濾 (backend/src/services/search_service.py)
 - [x] T037 統計服務：產生格式/星級統計 (backend/src/services/stats_service.py)

## Phase 3.5: API Endpoints (align with contracts)
 - [x] T038 Router: /scan/start (backend/src/api/scan.py)
 - [x] T039 Router: /scan/status (backend/src/api/scan.py)
 - [x] T040 Router: /files/tree (backend/src/api/files.py)
 - [x] T041 Router: /files/list (backend/src/api/files.py)
 - [x] T042 Router: /files/{id}/waveform (backend/src/api/files.py)
 - [x] T043 Router: /files/{id}/rating (backend/src/api/files.py)
 - [x] T044 Router: /files/{id}/description (backend/src/api/files.py)
 - [x] T045 Router: /search (backend/src/api/search.py)
 - [x] T046 Router: /stats (backend/src/api/stats.py)

## Phase 3.6: Frontend Core UI
- [ ] T047 建立初始專案入口 (frontend/src/pages/index.ts)
- [ ] T048 [P] Component: 樹狀瀏覽 (frontend/src/components/TreeView.ts)
- [ ] T049 [P] Component: 播放控制列 (frontend/src/components/PlayerBar.ts)
- [ ] T050 [P] Component: 搜尋 + 星級篩選 (frontend/src/components/SearchFilter.ts)
- [ ] T051 [P] Component: 波形顯示 (frontend/src/components/WaveformView.ts)
- [ ] T052 狀態管理：全域選取/播放/星級 store (frontend/src/state/store.ts)
- [ ] T053 鍵盤快捷處理 (frontend/src/lib/keyboard.ts)

## Phase 3.7: Frontend Integration
- [ ] T054 API 客戶端封裝 (frontend/src/lib/api.ts)
- [ ] T055 整合播放流程（選取 → 播放 → 高亮）(frontend/src/integration/play_flow.ts)
- [ ] T056 整合搜尋與篩選 (frontend/src/integration/search_flow.ts)
- [ ] T057 整合標記與持久化回填 (frontend/src/integration/annotation_flow.ts)
- [ ] T058 整合波形 PNG 載入占位符 (frontend/src/integration/waveform_flow.ts)

## Phase 3.8: Integration & Performance Tests Execution
- [ ] T059 執行全部 contract + integration 測試並確保最初失敗案例趨向綠燈
- [ ] T060 調整服務/索引確保 performance baseline 達標

## Phase 3.9: Polish
- [ ] T061 [P] 新增單元測試：tokenizer (backend/tests/unit/test_tokenizer.py)
- [ ] T062 [P] 新增單元測試：search service (backend/tests/unit/test_search_service.py)
- [ ] T063 [P] 新增單元測試：waveform service (backend/tests/unit/test_waveform_service.py)
- [ ] T064 覆蓋率報告整合 (pytest + 前端測試) (reports/coverage/)
- [ ] T065 重構：拆分超過複雜度上限函式
- [ ] T066 補充文件：更新 quickstart + API 說明 (docs/api.md)
- [ ] T067 手動測試腳本/說明 (docs/manual-test.md)
- [ ] T068 性能結果紀錄 (docs/performance.md)

## Dependencies
- Setup (T001–T006) → 所有後續
- Contract/Integration/Performance Tests (T007–T024) → Models (T025–T030)
- Models → Services (T031–T037)
- Services → API Routers (T038–T046)
- API → Frontend Core (T047–T053) → Frontend Integration (T054–T058)
- 前端與後端功能完成 → 測試執行與調整 (T059–T060) → Polish (T061–T068)

## Parallel Execution Examples
```
# 並行建立合約測試 (Phase 3.2 初期)
T008 T009 T010 T011 T012 T013 T014 T015 T016

# 並行建立資料模型 (Phase 3.3)
T025 T026 T027 T028

# 並行前端元件 (Phase 3.6)
T048 T049 T050 T051

# 並行後期單元測試 (Phase 3.9)
T061 T062 T063
```

## Validation Checklist
- [ ] 所有 contracts 皆有對應測試 (T008–T016)
- [ ] 每個實體皆有 Model 任務 (AudioFile/FolderNode/UserPreference/SearchIndex) (T025–T028)
- [ ] 測試任務皆於實作之前列出 (Phase 3.2 > 3.3+)  
- [ ] [P] 任務無同檔衝突  
- [ ] 整合與性能測試在 Core 完成後執行  
- [ ] Polish 前具備綠燈基礎

## Pending Refactor Notes
- R001: 實作 T032A 需：
	1. 於 `waveform_service.py` 由 file_id 尋找對應 AudioFile.relative_path，組合實際音檔絕對路徑，再以相同資料夾/檔名 `.png` 作為 target。
	2. 移除集中 `WAVEFORM_DIR` 常數（或保留為 fallback）。
	3. 更新掃描流程（可選）在掃描時若發現現有 `.png` 即寫入 AudioFile.waveform_png_path。
	4. API `/files/{id}/waveform` 回傳相對路徑（或絕對）需與新策略一致。
	5. 後續更新或新增單元測試覆蓋此行為。

