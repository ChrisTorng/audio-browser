/**
 * Play Flow Integration (T055)
 * - 監聽 TreeView 選取與 PlayerBar 播放事件。
 * - 簡化：尚未實作實際 AudioContext，僅 console.log 示意。
 */
import { store } from '../state/store.js';

function onTreeSelect(e: Event) {
  const detail = (e as CustomEvent).detail; // { path } or file id (待後端樹 API 定義)
  if (detail?.id) {
    store.selectFile(detail.id);
  }
}

function onPlayerPlay() { store.setPlaying(true); console.log('PLAY', store); }
function onPlayerPause() { store.setPlaying(false); console.log('PAUSE'); }

export function bindPlayFlow(root: HTMLElement | Document = document) {
  root.addEventListener('tree:select', onTreeSelect as any);
  root.addEventListener('player:play', onPlayerPlay as any);
  root.addEventListener('player:pause', onPlayerPause as any);
}

if (typeof window !== 'undefined') bindPlayFlow();
