/**
 * API Client (T054)
 * - 提供統一 fetch wrapper 與端點函式。
 */
export interface ApiOptions { baseUrl?: string }
const DEFAULT_BASE = '';

async function request<T>(path: string, init?: RequestInit, opts?: ApiOptions): Promise<T> {
  const base = opts?.baseUrl ?? DEFAULT_BASE;
  const res = await fetch(base + path, { ...init, headers: { 'Content-Type': 'application/json', ...(init?.headers||{}) } });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  if (res.status === 204) return undefined as unknown as T;
  return res.json() as Promise<T>;
}

// Scan
export const startScan = (opts?: ApiOptions) => request<{accepted: boolean}>('/scan/start', { method: 'POST' }, opts);
export const getScanStatus = (opts?: ApiOptions) => request<any>('/scan/status', undefined, opts);

// Files
export interface FileListItem { id: string; name: string; format: string }
export const listFiles = (opts?: ApiOptions) => request<FileListItem[]>('/files/list', undefined, opts);
export const getTree = (path?: string, opts?: ApiOptions) => request<any>(`/files/tree${path?`?path=${encodeURIComponent(path)}`:''}`, undefined, opts);
export const getWaveform = (id: string, opts?: ApiOptions) => request<{file_id: string; waveform_png_path: string}>(`/files/${id}/waveform`, undefined, opts);
export const setRating = (id: string, stars: number, opts?: ApiOptions) => request(`/files/${id}/rating`, { method: 'PUT', body: JSON.stringify({ stars }) }, opts);
export const setDescription = (id: string, description: string, opts?: ApiOptions) => request(`/files/${id}/description`, { method: 'PUT', body: JSON.stringify({ description }) }, opts);

// Search
export const search = (q: string, minStars?: number, opts?: ApiOptions) => {
  const params = new URLSearchParams();
  if (q) params.set('q', q); if (minStars!=null) params.set('minStars', String(minStars));
  return request<{query: string; results: any[]}>(`/search${params.toString()?`?${params}`:''}`, undefined, opts);
};

// Stats
export const getStats = (opts?: ApiOptions) => request<any>('/stats', undefined, opts);
