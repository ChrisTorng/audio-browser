/**
 * TreeView Component (T048)
 * - 職責：顯示資料夾樹與懶載入節點。
 * - 事件：dispatch CustomEvent('tree:select', { detail: { path } })
 */
export class TreeView extends HTMLElement {
  private mounted = false;
  connectedCallback() {
    if (this.mounted) return; this.mounted = true;
    this.classList.add('tree-view');
    this.textContent = 'TreeView (loading...)';
    // TODO: 之後以 API 資料取代
  }
}
customElements.define('ab-tree', TreeView);
