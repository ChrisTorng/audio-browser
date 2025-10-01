/**
 * PlayerBar Component (T049)
 * - 職責：播放/暫停/進度顯示。
 * - 事件：'player:play', 'player:pause'
 */
export class PlayerBar extends HTMLElement {
  private mounted = false;
  private button!: HTMLButtonElement;
  connectedCallback() {
    if (this.mounted) return; this.mounted = true;
    this.classList.add('player-bar');
    this.button = document.createElement('button');
    this.button.textContent = 'Play';
    this.button.addEventListener('click', () => {
      const playing = this.button.dataset.state === 'playing';
      if (playing) {
        this.button.dataset.state = 'paused';
        this.button.textContent = 'Play';
        this.dispatchEvent(new CustomEvent('player:pause', { bubbles: true }));
      } else {
        this.button.dataset.state = 'playing';
        this.button.textContent = 'Pause';
        this.dispatchEvent(new CustomEvent('player:play', { bubbles: true }));
      }
    });
    this.appendChild(this.button);
  }
}
customElements.define('ab-player', PlayerBar);
