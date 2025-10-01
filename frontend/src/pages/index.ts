/**
 * 初始入口頁面 (T047)
 * 簡易掛載函式：負責將核心 UI 元件 (之後實作) 插入 DOM。
 * 採無框架策略：使用原生自訂元素 (Web Components) 與全域 store。
 */

// 待後續元件實作後再導入：TreeView, PlayerBar, SearchFilter, WaveformView
// import '../components/TreeView';
// import '../components/PlayerBar';
// import '../components/SearchFilter';
// import '../components/WaveformView';

interface BootstrapOptions {
  target?: HTMLElement;
}

export function bootstrap(options: BootstrapOptions = {}): void {
  const root = options.target ?? document.getElementById('app') ?? createRoot();
  root.classList.add('audio-browser-root');

  // 基本結構容器 (之後以自訂元素填入)
  if (!root.querySelector('.layout')) {
    const layout = document.createElement('div');
    layout.className = 'layout';
    layout.innerHTML = `
      <div class="sidebar">
        <div class="tree-container" data-mount="tree"></div>
      </div>
      <div class="main">
        <div class="topbar">
          <div data-mount="search"></div>
          <div data-mount="player"></div>
        </div>
        <div class="waveform" data-mount="waveform"></div>
        <div class="list" data-mount="list"></div>
      </div>`;
    root.appendChild(layout);
  }
}

function createRoot(): HTMLElement {
  const div = document.createElement('div');
  div.id = 'app';
  document.body.appendChild(div);
  return div;
}

// 若直接以 <script type="module" src=".../index.js"> 載入時自動啟動
if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => bootstrap());
  } else {
    bootstrap();
  }
}
