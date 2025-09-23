/**
 * Search Flow Integration (T056)
 * - 監聽 SearchFilter 事件並呼叫後端 /search 或 /files/list。
 */
import { store } from '../state/store.js';
import { search as apiSearch, listFiles } from '../lib/api.js';

let currentAbort: AbortController | null = null;

async function performSearch(term: string, minStars: number) {
  if (currentAbort) currentAbort.abort();
  currentAbort = new AbortController();
  try {
    const data = term ? await apiSearch(term, minStars) : await listFiles();
    console.log('SEARCH RESULTS', data);
  } catch (e) {
    if ((e as any).name === 'AbortError') return;
    console.error('Search error', e);
  }
}

function onSearchChange(e: Event) {
  const { term, minStars } = (e as CustomEvent).detail;
  store.setSearch(term, minStars);
  performSearch(term, minStars);
}

export function bindSearchFlow(root: HTMLElement | Document = document) {
  root.addEventListener('search:change', onSearchChange as any);
}

if (typeof window !== 'undefined') bindSearchFlow();
