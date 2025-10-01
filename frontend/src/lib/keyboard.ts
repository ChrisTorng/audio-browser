/**
 * Keyboard Shortcuts (T053)
 * - ↑ ↓: 暫存 (未實作用於列表聚焦)
 * - 數字 0-5: 設定星級 (暫以 console.log 示意，之後呼叫 API 並更新 store)
 * - /: 聚焦搜尋 (若存在 ab-search input)
 * - Space/Enter: 切換播放
 */
import { store } from '../state/store.js';

function onKey(e: KeyboardEvent) {
  // 聚焦於可輸入元素時忽略大部分快捷
  const tag = (e.target as HTMLElement)?.tagName;
  const isTyping = tag === 'INPUT' || tag === 'TEXTAREA' || (e.target as HTMLElement)?.isContentEditable;
  if (isTyping && e.key !== 'Escape') return;

  if (e.key === '/') {
    const search = document.querySelector('ab-search input') as HTMLInputElement | null;
    if (search) { e.preventDefault(); search.focus(); }
    return;
  }

  if (e.key === ' ' || e.key === 'Enter') {
    e.preventDefault();
    store.setPlaying(!getState().playing);
    return;
  }

  if (/^[0-5]$/.test(e.key)) {
    e.preventDefault();
    const stars = parseInt(e.key, 10);
    console.log('Set stars (TODO implement API):', stars, 'for file', getState().selectedFileId);
    return;
  }
}

function getState() { let s: any; store.subscribe(st=> s=st)(); return s; }

export function enableKeyboardShortcuts() { window.addEventListener('keydown', onKey); }
export function disableKeyboardShortcuts() { window.removeEventListener('keydown', onKey); }

if (typeof window !== 'undefined') enableKeyboardShortcuts();
