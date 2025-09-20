# Implementation Plan: 大量音頻瀏覽與標記搜尋功能

**Branch**: `001-` | **Date**: 2025-09-20 | **Spec**: /home/christorng/audio-browser/specs/001-/spec.md
**Input**: Feature specification from `/specs/001-/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
大量音頻檔案之本地資料夾遞迴掃描、樹狀瀏覽、即時播放、波形自動生成、鍵盤導覽、星級與描述標記、搜尋與星級篩選。目標：高效能（<2s 初始顯示、<100ms 播放啟動）、高一致性使用者體驗、持久化最小集（僅星級與描述）以降低儲存負擔，並遵循憲法之程式碼品質與測試標準。技術方向：Python 後端 (檔案掃描/波形預處理/SQLite 存取 API) + 前端 TypeScript (緊湊 UI + 虛擬清單 + 鍵盤互動)。

## Technical Context
**Language/Version**: Python 3.x (後端), TypeScript (前端)  
**Primary Dependencies**: [NEEDS CLARIFICATION: Python Web Framework? FastAPI / Flask?]; 波形生成 [NEEDS CLARIFICATION: 使用何種演算法或函式庫?]; 前端狀態管理 [NEEDS CLARIFICATION: 是否需使用框架? 原始 TS + Web Components?]  
**Storage**: SQLite (僅儲存有星級或描述之 AudioFile metadata 與使用者偏好)  
**Testing**: pytest (後端), 前端可用 Jest/Playwright [NEEDS CLARIFICATION: 前端測試工具選擇?]  
**Target Platform**: 桌面瀏覽器 (Chrome/Firefox/Safari 最新版)  
**Project Type**: web (frontend + backend)  
**Performance Goals**: 初次顯示 <2s；播放啟動 <100ms；搜尋結果 <300ms；波形 <50MB 於 2s 內生成或回饋進度；60fps 波形視覺更新  
**Constraints**: 單活躍音檔緩衝 <200MB；大量檔案 (>10k) 需懶載與索引；不可阻塞主執行緒（前端使用 Web Worker for 波形/搜尋）  
**Scale/Scope**: 目標支援 100k 音檔（深層資料夾結構）；同時顯示視窗中 ~50–100 列（虛擬化）  

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Code Quality Gates
- [ ] Type safety implementation planned for all audio processing functions (後端型別註解 + 前端 TS)
- [ ] Maximum 10 cyclomatic complexity for all audio processing functions (標記高風險：波形處理流程需分段)
- [ ] Single responsibility principle verified for all audio components (掃描、索引、波形、播放、標記模組化)
- [ ] Comprehensive documentation planned for audio domain concepts (AudioFile / WaveformCache / SearchIndex 說明)

### Testing Standards Gates  
- [ ] TDD approach confirmed: tests written before implementation (contract + integration 樂觀測試計畫)
- [ ] Audio-specific test cases planned (sample audio files, format compatibility)  
- [ ] Integration tests for audio format compatibility planned (多格式載入 + 播放 API)  
- [ ] 90% test coverage target for critical audio processing paths (波形、索引、篩選核心覆蓋)

### User Experience Consistency Gates
- [ ] Standardized audio player control patterns defined (播放/暫停/跳轉鍵盤映射草案)  
- [ ] Consistent error handling and loading states for all audio operations (統一 Loading/Error 元件)  
- [ ] Keyboard shortcuts and accessibility features planned (上下/左右/Enter/Space/星級快捷)  
- [ ] Responsive design for audio interface components (緊湊格線 + 自適應側欄)

### Performance Requirements Gates
- [ ] Audio file loading <2s for files <50MB verified feasible (預抓 metadata + 延後波形)  
- [ ] Playback latency <100ms requirement confirmed achievable (預先建立 AudioContext + lazy decode)  
- [ ] Memory usage limits for audio buffers (<200MB per track) planned (釋放非焦點 audio buffer)  
- [ ] Web Workers implementation for non-blocking audio processing (波形/全文索引 worker 提案)

### Audio Format Standards Gates
- [ ] Support for standard audio formats (MP3, FLAC, WAV, OGG, AAC) confirmed (後端 format 掃描清單)  
- [ ] Metadata extraction consistency planned across formats (統一抽象介面)  
- [ ] Waveform generation capability confirmed (抽樣策略待研究)  
- [ ] File integrity preservation during processing verified (唯讀掃描，不修改原檔)

## Project Structure

### Documentation (this feature)
```
specs/001-/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
backend/
├── src/
│   ├── api/
│   ├── services/
│   ├── models/
│   └── workers/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── state/
│   └── workers/
└── tests/
```

**Structure Decision**: Web application (frontend + backend)

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - Unknowns: Python Web Framework, 波形算法, 前端框架/無框架策略, 前端測試工具, 抽樣密度, 排序欄位, 展開狀態持久化, 非 UTF-8 編碼處理, 儲存策略(本地 vs server-only)  
   - For each NEEDS CLARIFICATION → research task  
2. **Generate and dispatch research agents** (擬定研究任務清單)  
3. **Consolidate findings** in `research.md` (Decision / Rationale / Alternatives)

**Output**: research.md with all NEEDS CLARIFICATION resolved (否則不前進 Phase 1)

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*
1. 資料實體 → data-model.md (包含索引策略/波形快取欄位)  
2. API contracts: 掃描啟動 / 狀態查詢 / 音檔列表分頁 / 波形請求 / 星級更新 / 描述更新 / 搜尋 / 統計  
3. Contract tests: 每個 API schema 驗證 (初始失敗)  
4. 整合測試情境：使用者故事對應播放/搜尋/標記流程  
5. quickstart.md：安裝、建立資料夾、啟動後端、開啟前端、基本鍵盤操作  
6. 更新 agent context (若腳本存在)

**Output**: data-model.md, contracts/*.yaml(or .json), tests/contract/*, quickstart.md

## Phase 2: Task Planning Approach
*描述 /tasks 將如何生成 tasks.md（不於此階段建立）*

**Task Generation Strategy**:
- 從 contracts 產生：每個 endpoint → Contract Test 任務 (tests/contract)
- 從 data-model 產生：每個實體 → Model 定義任務
- 從使用者故事：每個 Acceptance Scenario → Integration Test 任務
- 從 NFR 產生：Performance Baseline 測試任務（播放延遲、搜尋延遲、波形生成時間）
- 從 Edge Cases：異常/大檔/不支援格式 → 測試或保護性任務

**Ordering Strategy**:
1. Setup（專案目錄、依賴、格式檢查）
2. Contract Tests（失敗）
3. Models & Index & Waveform Cache 結構
4. Services（掃描、索引、波形、標記）
5. API 層（符合合約）
6. 前端虛擬樹 + 播放控制 + 波形載入
7. 前端標記與搜尋互動
8. 整合測試（使用者故事）
9. 效能與壓力測試
10. Polish（文件、重構、覆蓋率驗證）

**Parallelization ([P])**:
- Model 定義可並行
- 不同 API endpoint contract tests 可並行
- 前端獨立元件（播放器、樹、搜尋）可並行（在 API 穩定後）

**Estimated Output**: ~30 任務（T001–T030）

**Readiness**: 完成此描述後可進入 /tasks 指令生成實際 tasks.md

## Phase 3+: Future Implementation
(略)

## Complexity Tracking
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 分離 frontend/backend 結構 | 清晰邊界 + 部署靈活 | 單一專案將增加前端構建複雜度與測試混雜 |

## Progress Tracking
**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`*
