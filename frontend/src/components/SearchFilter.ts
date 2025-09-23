/**
 * SearchFilter Component (T050)
 * - 職責：搜尋輸入 + 星級篩選。
 * - 事件：'search:change' ({ term, minStars })
 */
export class SearchFilter extends HTMLElement {
  private mounted = false;
  private input!: HTMLInputElement;
  private select!: HTMLSelectElement;
  connectedCallback() {
    if (this.mounted) return; this.mounted = true;
    this.classList.add('search-filter');
    this.innerHTML = '';
    this.input = document.createElement('input');
    this.input.type = 'text';
    this.input.placeholder = 'Search...';
    this.select = document.createElement('select');
    ['0','1','2','3','4','5'].forEach(s => {
      const opt = document.createElement('option'); opt.value = s; opt.textContent = `>= ${s}★`; this.select.appendChild(opt);
    });
    const emit = () => this.dispatchEvent(new CustomEvent('search:change', { bubbles: true, detail: { term: this.input.value, minStars: parseInt(this.select.value, 10) } }));
    this.input.addEventListener('input', emit);
    this.select.addEventListener('change', emit);
    this.append(this.input, this.select);
  }
}
customElements.define('ab-search', SearchFilter);
