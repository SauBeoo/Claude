/* ─────────────────────────────────────────────────────────────────────────────
   PROBE_flow_ui.js — đo giao diện Flow để chốt selector cho Flow Video Batch v2
   Dùng: mở tab Flow ĐANG Ở TRONG PROJECT → F12 → Console → dán PHẦN 1 → Enter
         → copy output dán lại cho Claude. Rồi làm PHẦN 2.
   ⚠️ Đọc thôi, KHÔNG bấm gen, KHÔNG tốn credit.
   ⚠️ Xong thì ĐÓNG F12 và mở TAB FLOW MỚI trước khi chạy extension —
      tab có devtools/debugger thì extension attach chồng lên là chết im.
   ───────────────────────────────────────────────────────────────────────────── */

/* ══════════════ PHẦN 1 — đo tĩnh (dán cả khối này) ══════════════ */
(() => {
  const vis = el => el.offsetParent !== null || el.getClientRects().length > 0;
  const txt = el => (el.textContent || '').replace(/\s+/g, ' ').trim();

  // ô prompt
  const ed = document.querySelector('div.ProseMirror[contenteditable="true"]')
          || document.querySelector('div[contenteditable="true"]');

  // mọi thứ bấm được, kèm aria-label + text + disabled  → trả lời P1 và P3
  const clickable = [...document.querySelectorAll('button,[role="button"],[role="tab"],[role="menuitem"],[role="combobox"]')]
    .filter(vis)
    .map(b => ({ al: b.getAttribute('aria-label') || '', tx: txt(b).slice(0, 44), dis: !!b.disabled }))
    .filter(o => o.al || o.tx);

  // ô tile ảnh: leo 5 tầng từ <img> để tìm cái gì ĐỊNH DANH được nó → quyết đường (B)
  const imgs = [...document.querySelectorAll('img')].filter(vis)
    .filter(i => i.naturalWidth > 120);           // bỏ avatar/icon
  const chain = (el) => { const out = []; let n = el;
    for (let i = 0; i < 5 && n; i++) {
      out.push({ tag: n.tagName,
                 cls: String(n.className || '').slice(0, 60),
                 id: n.id || undefined,
                 keys: [...n.attributes].map(a => a.name)
                        .filter(x => x.startsWith('data-') || ['aria-label','alt','title','href'].includes(x)),
                 al: n.getAttribute && (n.getAttribute('aria-label') || n.getAttribute('alt')) || undefined });
      n = n.parentElement; }
    return out; };

  const out = {
    url: location.origin + location.pathname,
    editor: ed ? { cls: String(ed.className).slice(0, 60),
                   ph: txt(ed.querySelector('[class*=placeholder]') || {}) || null } : '🔴 KHONG THAY',
    nFileInputs: document.querySelectorAll('input[type=file]').length,
    hasSearch: !!document.querySelector('input[type=search],input[placeholder*="earch" i]'),
    nTiles: imgs.length,
    tileSrc: imgs.slice(0, 3).map(i => ({ src: String(i.src).slice(0, 90), alt: i.alt || '' })),
    tileChain: imgs[0] ? chain(imgs[0]) : null,
    clickable,
  };
  console.log('%c=== FLOW PROBE PHAN 1 ===', 'font-weight:bold');
  console.log(JSON.stringify(out, null, 1));
  return out;
})();

/* ══════════════ PHẦN 2 — đo cách Flow NHẬN FILE (câu đắt nhất, P2) ══════════════
   ① dán khối này → Enter   (nó gài bẫy theo dõi, chưa làm gì cả)
   ② TỰ TAY bấm nút thêm ảnh ( "+" cạnh ô prompt ) rồi bấm mục Upload / Tải lên.
      Hộp thoại chọn file bật lên thì BẤM CANCEL — không cần chọn file thật.
   ③ dán   __flowProbe.report()   → Enter → copy output
   ───────────────────────────────────────────────────────────────────────────── */
(() => {
  const P = { picker: false, inputsCreated: [], menusSeen: [], clicks: [] };

  // bẫy 1: Flow có dùng File System Access API không?
  if (window.showOpenFilePicker && !window.showOpenFilePicker.__spied) {
    const orig = window.showOpenFilePicker.bind(window);
    const spy = function (...a) { P.picker = true; console.log('🔎 showOpenFilePicker ĐƯỢC GỌI', a); return orig(...a); };
    spy.__spied = true;
    window.showOpenFilePicker = spy;
  }

  // bẫy 2: có <input type=file> nào được TẠO RA lúc bấm không?
  new MutationObserver(ms => {
    for (const m of ms) for (const n of m.addedNodes) {
      if (n.nodeType !== 1) continue;
      const ins = n.matches && n.matches('input[type=file]') ? [n]
                : n.querySelectorAll ? [...n.querySelectorAll('input[type=file]')] : [];
      for (const i of ins) P.inputsCreated.push({ accept: i.accept, multiple: i.multiple, hidden: !i.offsetParent });
      // bẫy 3: menu vừa mở ra có những mục gì
      const mi = n.querySelectorAll ? [...n.querySelectorAll('[role=menuitem],[role=option],li,button')] : [];
      const labels = mi.map(x => (x.textContent || '').replace(/\s+/g, ' ').trim()).filter(s => s && s.length < 40);
      if (labels.length) P.menusSeen.push(labels.slice(0, 12));
    }
  }).observe(document.documentElement, { childList: true, subtree: true });

  // bẫy 4: mình đã bấm vào cái gì (để biết selector của nút thêm ảnh)
  document.addEventListener('click', e => {
    const b = e.target.closest('button,[role=button],[role=menuitem]');
    if (b) P.clicks.push({ al: b.getAttribute('aria-label') || '',
                           tx: (b.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40) });
  }, true);

  window.__flowProbe = { _: P, report() {
    const r = { showOpenFilePickerCalled: P.picker,
                fileInputsCreated: P.inputsCreated,
                fileInputsNow: document.querySelectorAll('input[type=file]').length,
                menusSeen: P.menusSeen,
                clicked: P.clicks,
                KET_LUAN: P.picker ? 'showOpenFilePicker → đi đường A3 (dispatchDragEvent)'
                        : (P.inputsCreated.length || document.querySelectorAll('input[type=file]').length)
                          ? 'có input[type=file] → đi đường A hoặc A2 (setFileInputFiles) ✅'
                          : 'chưa xác định — đã bấm tới mục Upload chưa?' };
    console.log('%c=== FLOW PROBE PHAN 2 ===', 'font-weight:bold');
    console.log(JSON.stringify(r, null, 1));
    return r; } };

  console.log('%c✅ Bẫy đã gài. Giờ TỰ BẤM nút thêm ảnh → Upload → Cancel, rồi chạy: __flowProbe.report()',
              'color:#0a0;font-weight:bold');
})();
