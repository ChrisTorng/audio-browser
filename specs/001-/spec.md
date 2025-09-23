# Feature Specification: 大量音頻瀏覽與標記搜尋功能

**Feature Branch**: `001-`  
**Created**: 2025-09-19  
**Status**: Draft  
**Input**: User description: "我要建立大量音頻的網頁瀏覽工具，它可以掃描指定資料夾含子資料夾下的所有音檔，在網頁內依資料夾名稱及音檔名稱之階層顯示所有音檔，並可自動生成波形圖。然後我要可以使用鍵盤方便瀏覽選擇所有音檔，即時播放，因此可以很方便得知每一個音檔的內容。我還要可以針對各別音檔標記「五星喜好」以及自訂描述。之後我可以搜尋名稱，包括資料夾及音檔名及描述，以及篩選星級，以快速找到想要的目標音檔。"

## 執行中已澄清事項 (2025-09-22)
- 音檔總量「不會太多」，單檔長度都「很短」：不實作最大層級限制與極端大檔優化。
- 掃描資料夾取得 mp3 時：若無對應波形 png，立即背景生成並快取；不需進度顯示。
- 檔名皆為簡單英數字：不需要額外正規化與轉碼策略。

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies  
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
一位使用者希望快速瀏覽本地巨大音檔資料庫，利用鍵盤快速跳轉、即時播放、查看波形、標記喜好與描述，並能透過搜尋與星級篩選迅速找到目標音檔。

### Acceptance Scenarios
1. **Given** 已設定根資料夾，系統已完成初始掃描，**When** 使用者展開某層資料夾並選擇一個音檔，**Then** 顯示該音檔波形並可即時播放。
2. **Given** 使用者已為多個音檔標記星級與描述，**When** 在搜尋列輸入關鍵字並設定星級>=4，**Then** 只顯示符合名稱或描述關鍵字且星級>=4的音檔清單。
3. **Given** 使用者聚焦在音檔列表，**When** 按下鍵盤方向鍵上下與 Enter，**Then** 可無滑鼠導航並即時切換播放焦點音檔。
4. **Given** 音檔尚未產生波形快取，**When** 首次點擊播放或點擊檢視，**Then** 系統於合理時間內顯示生成中的指示並最終呈現波形。
5. **Given** 使用者已設定星級與描述，**When** 重新載入頁面，**Then** 之前的標記仍存在。

### Edge Cases
- 掃描過程中遇到不支援或損毀檔案 → 標記並略過且記錄錯誤數量。
- 同名檔案存在於不同資料夾 → 顯示相對路徑區分。
- 使用者快速連續切換音檔播放 → 需避免播放重疊與記憶體洩漏。
- 搜尋輸入空字串 → 回復為目前資料夾上下文所有項目。
- 波形 png 尚未生成完成時 → 顯示暫用占位符圖示。

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: 系統 MUST 讓使用者指定根資料夾以進行遞迴掃描。
- **FR-002**: 系統 MUST 建立音檔樹狀結構依資料夾階層顯示。
- **FR-003**: 系統 MUST 支援的音檔格式至少含: WAV, MP3, FLAC, OGG, AAC。
- **FR-004**: 系統 MUST 對每個 MP3 檔檢查是否已有對應波形 png；若無則自動生成並儲存檔案（不需進度顯示）。
- **FR-005**: 系統 MUST 提供鍵盤導覽（上下、展開/收合、Enter 播放）。
- **FR-006**: 系統 MUST 即時播放目前選取音檔並顯示播放進度。
- **FR-007**: 系統 MUST 允許對每個音檔設定 0–5 星級評價。
- **FR-008**: 系統 MUST 允許對每個音檔新增與更新文字描述（支援多語字元）。
- **FR-009**: 系統 MUST 永續儲存星級與描述資料（本地 SQLite）。
- **FR-010**: 系統 MUST 支援依關鍵字搜尋檔名（含路徑片段）與描述。
- **FR-011**: 系統 MUST 支援依星級篩選（>= 指定值）。
- **FR-012**: 系統 MUST 在搜尋與篩選組合時僅顯示同時符合的結果。
- **FR-013**: 系統 MUST 顯示不支援或失敗載入的檔案計數並允許重新嘗試。
- **FR-014**: 系統 MUST 在潛在較多檔案情境下使用延遲載入避免 UI 卡頓（雖然目前預期檔案不多仍保留彈性）。
- **FR-015**: 系統 MUST 提供播放中檔案的視覺高亮。
- **FR-016**: 系統 MUST 防止重疊播放（切換時立即停止前一音檔）。
- **FR-017**: 系統 SHOULD 支援對極長音檔的抽樣波形策略（目前因短檔為主可延後）。
- **FR-018**: 系統 SHOULD 支援排序（至少：名稱、星級；建立時間可延後）。
- **FR-019**: 系統 SHOULD 在重新載入後保留上次瀏覽展開狀態（延後決策）。
- **FR-020**: 系統 DOES NOT 需要針對檔名做正規化（英數字假設成立）。

### Non-Functional / Performance (Derived from Constitution)
- **NFR-001**: 初次載入根資料夾完成首批可見節點顯示 < 2 秒。
- **NFR-002**: 單一音檔播放啟動延遲 < 100ms（快取後）。
- **NFR-003**: MP3 波形 png 生成（短檔案）通常於 2 秒內完成；若延遲則不阻塞播放。
- **NFR-004**: 記憶體使用：每活躍音檔緩衝 < 200MB（實際短檔遠低於此）。
- **NFR-005**: 搜尋與篩選回應時間 < 300ms。
- **NFR-006**: 鍵盤導航焦點移動回饋 < 50ms。
- **NFR-007**: 波形生成在背景執行不阻塞 UI。

### Key Entities
- **AudioFile**: id、relativePath、fileName、format、duration、size、waveformPngPath、starRating、description、createdAt、lastModifiedAt、scanStatus。
- **FolderNode**: id、name、path、children、expandedState、lazyLoaded。
- **WaveformCache**: audioFileId、generatedAt、resolution、status、partialSegments（MP3 png 生成後可選擇省略此實體簡化）。
- **UserPreference**: id、lastExpandedPaths、lastSelectedAudioId、displayDensity。
- **SearchIndex**: terms、audioFileRefs、lastUpdatedAt。

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain (僅保留 SHOULD 延後項目而非未決)*
- [ ] Requirements are testable and unambiguous  
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed

---
