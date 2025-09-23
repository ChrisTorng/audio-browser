# Data Model - 大量音頻瀏覽與標記搜尋功能

## Entities
### AudioFile
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| id | UUID | 主鍵 | path hash |
| relativePath | string | 相對於根目錄之路徑 | 顯示與搜尋索引鍵 |
| fileName | string | 檔名 | 英數字假設，不正規化 |
| format | enum | WAV/MP3/FLAC/OGG/AAC | 其他 → unsupported |
| duration | float | 秒數 | 首次解碼後回填 |
| size | int | 位元組大小 | 排序 / 閾值策略 |
| waveformPngPath | string | 對應波形 PNG 檔案路徑 | 掃描 MP3 無檔時預先生成 |
| starRating | int | 0-5 | 有值才寫入 SQLite |
| description | string | 使用者描述 | <=1024 chars (待最終確認) |
| createdAt | datetime | 檔案建立時間 | 排序可用 |
| lastModifiedAt | datetime | 檔案最後修改 | 快取失效判定 |
| scanStatus | enum | active/skipped/unsupported | 不支援格式記錄 |

### FolderNode
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | path hash |
| name | string | 資料夾名稱 |
| path | string | 相對 root 路徑 |
| childrenLoaded | bool | 是否已載入子節點 |
| expanded | bool | UI 展開狀態 (可延後持久化) |

### WaveformCache (DEFERRED / Optional)
若改用純 PNG 預先生成策略且檔案皆短，可暫不建立此實體。
| Field | Type | Description |
|-------|------|-------------|
| audioFileId | UUID | 對應 AudioFile |
| resolution | int | 採樣點數 | 需抽樣才建立 |
| segments | blob/json | 抽樣資料 | 長檔專用延後 |
| generatedAt | datetime | 生成時間 | 失效判定 |

### UserPreference
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | 單一使用者 (固定 'local') |
| lastExpandedPaths | json | 展開資料夾集合 (DEFERRED) |
| lastSelectedAudio | UUID | 上次選取音檔 |
| displayDensity | enum | compact/comfortable |

### SearchIndex
| Field | Type | Description |
|-------|------|-------------|
| term | string | token (lowercased) |
| audioFileIds | array | 對應音檔集合 |
| updatedAt | datetime | 更新時間 |

## Relationships
- FolderNode 1..* → (FolderNode | AudioFile)
- AudioFile 可選 → WaveformCache (長檔案策略時)
- UserPreference 1 → (多 UI 狀態欄位)
- SearchIndex 多對多 → AudioFile (倒排索引表示)

## State / Lifecycle
- MP3 掃描 → 若無波形 PNG → 生成 PNG → 設定 waveformPngPath
- 更新檔案 (mtime 變動) → 重新生成 PNG

## Validation Rules
- starRating ∈ [0,5]
- description 長度 ≤ 1024 (待確認)
- waveformPngPath 必須存在於檔案系統 (對 MP3)

## Deferred / Optional
- WaveformCache 抽樣資料（長音檔）
- 展開狀態持久化
- 其他排序欄位 (建立時間、大小)

## Indexing Strategy (Draft)
- Primary: id
- Secondary: relativePath (unique)
- Search: token 化 (lowercase, split by / 和 - _ .)

## Open Questions
- 是否需要 lazy 校驗 waveformPngPath 是否失效？
- 是否要提供重新生成全部波形的批次操作？
