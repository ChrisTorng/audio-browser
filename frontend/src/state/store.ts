/**
 * Global Store (T052)
 * - 管理：目前選取檔案、播放狀態、搜尋條件、星級篩選。
 * - 簡易 pub/sub：listener 註冊與事件發送。
 */
export interface StoreState {
  selectedFileId: string | null;
  playing: boolean;
  searchTerm: string;
  minStars: number;
}

export type StoreListener = (state: StoreState) => void;

class Store {
  private state: StoreState = {
    selectedFileId: null,
    playing: false,
    searchTerm: '',
    minStars: 0,
  };
  private listeners = new Set<StoreListener>();

  subscribe(fn: StoreListener) { this.listeners.add(fn); fn(this.state); return () => this.listeners.delete(fn); }
  private emit() { for (const l of this.listeners) l(this.state); }

  selectFile(id: string | null) { this.state = { ...this.state, selectedFileId: id }; this.emit(); }
  setPlaying(playing: boolean) { this.state = { ...this.state, playing }; this.emit(); }
  setSearch(term: string, minStars: number) { this.state = { ...this.state, searchTerm: term, minStars }; this.emit(); }
}

export const store = new Store();
