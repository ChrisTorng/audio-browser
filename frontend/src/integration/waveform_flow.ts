/**
 * Waveform Flow Integration (T058)
 * - 監聽 store.selectedFileId 變化 → 呼叫 /files/{id}/waveform → 更新 ab-waveform 元件。
 */
import { store } from '../state/store.js';
import { getWaveform } from '../lib/api.js';

let currentId: string | null = null;

export function bindWaveformFlow(root: Document | HTMLElement = document) {
  store.subscribe(async (st) => {
    if (st.selectedFileId && st.selectedFileId !== currentId) {
      currentId = st.selectedFileId;
      try {
        const wf = await getWaveform(st.selectedFileId);
        const el = root.querySelector('ab-waveform') as any;
        if (el) el.src = wf.waveform_png_path;
      } catch (e) {
        console.error('Waveform load error', e);
      }
    }
  });
}

if (typeof window !== 'undefined') bindWaveformFlow();
