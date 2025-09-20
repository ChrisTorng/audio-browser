# Data Model - 大量音頻瀏覽與標記搜尋功能

## Entities
### AudioFile
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| id | UUID | 主鍵 | 由掃描流程產生 (path hash) |
| relativePath | string | 相對於根目錄之路徑 | 用於顯示與搜尋 |
| fileName | string | 檔名 | 支援多語 |
| format | enum | WAV/MP3/FLAC/OGG/AAC | 其他標記 unsupported |
| duration | float | 秒數 | 由解碼後取得 |
| size | int | 位元組大小 | 用於排序/門檻策略 |
| waveformStatus | enum | pending/generating/ready/error | 快取狀態 |
| starRating | int | 0-5 | 只有有值時寫入 SQLite |
| description | string | 使用者描述 | 選填 |
| createdAt | datetime | 檔案建立時間 | 可能用於排序 |
| lastModifiedAt | datetime | 檔案最後修改 | 快取失效依據 |
| scanStatus | enum | active/skipped/unsupported | 不支援格式標記 |

### FolderNode
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | 主鍵 (path hash) |
| name | string | 資料夾名稱 |
| path | string | 絕對 or 相對路徑（相對 root 優先） |
| childrenLoaded | bool | 是否已載入子節點 |
| expanded | bool | UI 狀態（可持久化） |

### WaveformCache
| Field | Type | Description |
|-------|------|-------------|
| audioFileId | UUID | 對應 AudioFile |
| resolution | int | 採樣點數 | 依 UI 寬度動態 | 
| segments | blob/json | 壓縮後樣本資料 | 大檔案分段 |
| generatedAt | datetime | 生成時間 | 判斷是否重算 |

### UserPreference
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | 單使用者設定 (可固定 'local') |
| lastExpandedPaths | json | 最近展開的資料夾集合 |
| lastSelectedAudio | UUID | 上次選取音檔 |
| displayDensity | enum | compact/comfortable |

### SearchIndex
| Field | Type | Description |
|-------|------|-------------|
| term | string | 標準化後索引詞 |
| audioFileIds | array | 對應音檔集合 |
| updatedAt | datetime | 索引更新时间 |

## Relationships
- FolderNode 1..* → (FolderNode | AudioFile)
- AudioFile 1..1 → WaveformCache (可延遲)
- UserPreference 1 → 多組 UI 狀態欄位
- SearchIndex N..* → AudioFile 多對多關聯（實際以倒排索引結構儲存）

## State Transitions
### WaveformStatus
pending → generating → ready
pending → generating → error (可重試回到 pending)

## Derived / Computed Fields
- path hash (SHA1 or xxhash) 用於穩定 id
- duration 可能於第一播放 decode 後回填

## Validation Rules
- starRating ∈ [0,5]
- description 長度限制 (e.g. <= 1024 chars) [NEEDS CLARIFICATION: 上限?]
- waveform resolution ∈ {256,512,1024,2048} [NEEDS CLARIFICATION: 集合?]

## Indexing Strategy (Draft)
- Primary lookup: id
- Secondary: relativePath (unique)
- SearchIndex: tokenized (lowercased, diacritics stripped) terms referencing sets of audioFileIds

## Open Questions Impacting Model
- 是否儲存原始 metadata 摘要 (bitrate, sampleRate)?
- 是否需多使用者支援？
- 是否需標籤(tags) 擴充？
