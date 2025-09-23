/**
 * WaveformView Component (T051)
 * - 職責：顯示波形 PNG 或載入中占位符。
 * - API 回傳策略：/files/{id}/waveform 取得圖片路徑。
 */
export class WaveformView extends HTMLElement {
  private mounted = false;
  private img!: HTMLImageElement;
  set src(v: string) { if (this.img) this.img.src = v; }
  connectedCallback() {
    if (this.mounted) return; this.mounted = true;
    this.classList.add('waveform-view');
    this.img = document.createElement('img');
    this.img.alt = 'waveform';
    this.img.style.maxWidth = '100%';
    this.img.style.display = 'block';
    this.img.src = '';
    this.appendChild(this.img);
  }
}
customElements.define('ab-waveform', WaveformView);
