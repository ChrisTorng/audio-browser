/**
 * Annotation Flow Integration (T057)
 * - 目前僅示意：提供 setStars / setDescription 函式，後續可綁定 UI。
 */
import { setRating, setDescription } from '../lib/api.js';
import { store } from '../state/store.js';

export async function updateStars(stars: number) {
  const id = getState().selectedFileId; if (!id) return;
  await setRating(id, stars);
  console.log('Updated stars', stars);
}

export async function updateDescription(description: string) {
  const id = getState().selectedFileId; if (!id) return;
  await setDescription(id, description);
  console.log('Updated description');
}

function getState() { let s: any; store.subscribe(st=> s=st)(); return s; }
