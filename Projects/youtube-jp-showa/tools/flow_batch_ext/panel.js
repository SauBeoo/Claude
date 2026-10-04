// ═══════════════════════════════════════════════════════════════════════════════
// Flow Batch v2.1 — bơm (ẢNH + PROMPT) vào Google Flow qua chrome.debugger.
//
// 🟢 SELECTOR TRONG FILE NÀY LÀ **ĐO ĐƯỢC**, không phải đoán — dò trên tab thật
//    2026-09-09 (project `0652d7d2…`, Flow layout All media/Images/Videos/Characters/
//    Scenes/Uploads/Tools). Bảng chứng cứ: DESIGN_i2v_2026-09-09.md §0.7.
//
// ⭐ ĐƯỜNG ĐI ĐÚNG (đo được, khác hẳn giả thuyết ban đầu là upload file):
//    ẢNH ĐÃ NẰM TRONG PROJECT ⇒ không upload gì cả. Nút `+` trong thanh prompt
//    (`aria-label="Add ingredients to the prompt box"`) mở **bảng chọn asset** có ô
//    `input.search-input` (placeholder "Search assets") + danh sách asset CÓ TÊN CHỮ +
//    nút `Add to prompt`. Đo bằng bẫy: bấm `+` KHÔNG gọi `showOpenFilePicker` và KHÔNG
//    sinh `input[type=file]` ⇒ đường A/A2/A3 (upload/kéo-thả) **không cần** cho luồng chính.
//
// 🔴 BỐN THỨ ĐO ĐƯỢC LÀM ĐỔI THIẾT KẾ:
//  ① `.base-prompt-box` là hộp chứa ô prompt + slot ảnh + settings. **Mọi phép tìm nút
//     phải SCOPE vào hộp này.** Bản v2.0 tìm cả trang nên nhãn "add" trúng
//     `Add media menu` ở góc phải trên (SAI nút) trước khi trúng nút trong hộp.
//  ② Mode nằm trong `button[aria-label="Settings trigger"]` → popover là **lưới radio**
//     `Image|Video` × `Frames|Ingredient` × `16:9|9:16` × `x1..x4` + dropdown model
//     (`Veo 3.1 - Quality`). Khớp radio bằng TEXT.
//  ③ **PHẢI LÀ `Video` + `Frames`, KHÔNG PHẢI `Ingredient`.** Đo thật: cùng một ảnh, ở
//     mode `Ingredient` thì chip ra `chip-container chip-container-disabled` + icon `error`
//     (ảnh vẫn load, `naturalWidth` 1376 — tức bị TỪ CHỐI, không phải lỗi tải); đổi sang
//     `Frames` thì chip thành `chip-container`, `aria-label="Image ingredient"`, và thanh
//     prompt hiện **`Start ⇄ End`** = đúng slot frame đầu/cuối.
//  ④ **GIÁ CREDIT NẰM SẴN TRONG DOM**: chuỗi `Generating will use 100 credits`. Và khi hết
//     credit thì có `button[aria-label="Insufficient credits warning"]`. ⇒ Không cần gen
//     thử để biết giá, và tool TỰ CHẶN khi hết credit.
//
// 🔴 NGUYÊN TẮC GIỮ LẠI TỪ v1.1 (đừng "sửa cho gọn"):
//  · MỘT phép đo duy nhất (`JS_JOBSTATE`) cho mọi nhánh — placeholder của ProseMirror nằm
//    TRONG ô editable nên mọi phép "ô trống chưa" theo NGƯỠNG SỐ KÝ đều sai vĩnh viễn.
//  · Thất bại phải LOUD, không auto-retry cú gen (100 credits/clip).
//  · Sổ đã-gửi theo job id ⇒ bấm START lại không bao giờ gen trùng.
// ═══════════════════════════════════════════════════════════════════════════════

const $ = id => document.getElementById(id);
const HOSTS = ["flow.google.com", "labs.google"];
let running = false, LOG = [];

const sleep = ms => new Promise(r => setTimeout(r, ms));
const norm = s => (s || "").replace(/\s+/g, " ").trim().toLowerCase();

function say(msg, keep) {
  if (keep) LOG.push(msg); else LOG = [msg];
  if (LOG.length > 60) LOG = LOG.slice(-60);
  $("status").textContent = LOG.join("\n");
  $("status").scrollTop = $("status").scrollHeight;
}
const add = m => say(m, true);

const CFG = () => ({
  submit: $("cfgSubmit").value.split("|").map(norm).filter(Boolean),
  addimg: $("cfgAdd").value.split("|").map(norm).filter(Boolean),
  mode:   $("cfgMode").value.split("|").map(norm).filter(Boolean),
});

// ═══════════════════════════════════════════════════════════════════════════════
// TAB CHUYỂN CHẾ ĐỘ — v1 (bơm CHỮ, đúng luồng bản 1.1) · v2 (ẢNH → VIDEO)
// v1 KHÔNG phải "v2 bỏ bớt": nó có bộ mặc định riêng, vì luồng v1 là ~250 prompt/lượt.
// ═══════════════════════════════════════════════════════════════════════════════
const RM = () => $("runmode").value;
const LF = String.fromCharCode(10);

// Placeholder của ô prompt, đổi theo tab. Viết bằng template literal có XUỐNG DÒNG THẬT —
// 🔴 đừng sinh mấy chuỗi này bằng heredoc: `\n` bị unescape một tầng rồi thành newline thật
//    ⇒ vỡ chuỗi JS, y hệt bẫy đã ghi ở `render-background.md` §2.6 ⑥ (đã dính 2026-09-10).
const PH_V1 = `một prompt MỘT DÒNG, ví dụ:

photorealistic Japanese kitchen, morning light, a hand reaching for a cup
close-up of a green envelope on a wooden table, soft afternoon light`;

const PH_V2 = `{"id":"sb_04","mode":"frames","asset":"Woman walking down hallway","prompt":"Kazuko walks away …"}
{"id":"sb_06","mode":"frames","asset":"Man drawing circle on whiteboard","prompt":"Nakamura draws …"}

→ Không muốn tự viết JSON thì dùng mục 2b ngay dưới, hoặc nạp file jobs.jsonl.`;

function setMode(m, remember = true) {
  $("runmode").value = m;
  document.body.dataset.mode = m;
  $("tab-v1").setAttribute("aria-selected", m === "v1");
  $("tab-v2").setAttribute("aria-selected", m === "v2");
  if (m === "v1") {                    // luồng cũ: chạy thẳng, không trần, không dry-run
    $("dryrun").checked = false;
    $("maxjobs").value = 9999;
    $("delay").value = 18;             // nhịp đã kiểm của v1.1 cho gen ảnh
  } else {
    $("dryrun").checked = true;        // video tốn 100 credits/clip ⇒ dry-run trước
    if (+$("maxjobs").value > 200) $("maxjobs").value = 5;
    if (+$("delay").value < 20) $("delay").value = 20;
  }
  $("prompts").placeholder = m === "v1" ? PH_V1 : PH_V2;
  if (remember) chrome.storage.local.set({ runmode: m });
  say(m === "v1"
    ? "v1 · bơm CHỮ — mỗi dòng 1 prompt, bỏ qua ảnh/mode/hàng đợi. Trần job/lượt mở, DRY-RUN tắt."
    : "v2 · ẢNH → VIDEO — nạp jobs.jsonl. DRY-RUN đang BẬT (không tốn credit).");
}
$("tab-v1").onclick = () => setMode("v1");
$("tab-v2").onclick = () => setMode("v2");

// ── tab Flow ──────────────────────────────────────────────────────────────────
// 🔴 "QUÉT KHÔNG ĐƯỢC" — nguyên nhân số 1 là **extension nằm ở Chrome PROFILE KHÁC**
//    với tab Flow: `chrome.tabs.query` chỉ thấy tab CÙNG profile với extension. Bản cũ
//    chỉ in "không thấy tab Flow nào" nên không phân biệt được 3 ca hoàn toàn khác nhau:
//      ⓐ sai profile  ⓑ chưa mở tab Flow  ⓒ filter host sai (Flow đổi domain lần 3).
//    ⇒ Nay LUÔN in ra extension thấy được BAO NHIÊU tab và HOST nào, và cho chọn tay
//       mọi tab khi không khớp host — tự chẩn đoán thay vì bắt người dùng đoán.
async function listTabs() {
  const sel = $("tabsel"); sel.innerHTML = "";
  let tabs = [];
  try { tabs = await chrome.tabs.query({}); }
  catch (e) { say("🔴 Không gọi được chrome.tabs.query: " + e.message); return; }

  const host = u => { try { return new URL(u).host; } catch (e) { return u ? u.split("/")[0] : "?"; } };
  const flow = tabs.filter(t => t.url && HOSTS.some(h => t.url.includes(h)));
  const src = flow.length ? flow : tabs.filter(t => t.url && /^https?:/.test(t.url));

  for (const t of src) {
    const o = document.createElement("option");
    o.value = t.id;
    const isFlow = t.url && HOSTS.some(h => t.url.includes(h));
    const inProject = t.url.includes("/project/") || t.url.includes("/tools/flow");
    o.textContent = `[${t.id}] ${isFlow ? (inProject ? "" : "⚠ chưa mở project — ")
                                        : "⛔ KHÔNG phải Flow — "}${host(t.url)} · ${(t.title || "").slice(0, 44)}`;
    sel.appendChild(o);
  }

  if (flow.length) return;

  if (!src.length) {
    const o = document.createElement("option");
    o.value = ""; o.textContent = "— extension không thấy tab http(s) nào —";
    sel.appendChild(o);
  }
  const hosts = [...new Set(tabs.map(t => host(t.url || "")))].filter(h => h && h !== "?").slice(0, 12);
  say([
    "🔴 KHÔNG thấy tab Flow nào.",
    `Extension thấy ${tabs.length} tab trong CÙNG Chrome profile với nó — host: ${hosts.join(", ") || "(không có)"}`,
    "",
    "Ba nguyên nhân, phân biệt bằng danh sách host ở trên:",
    "  ⓐ Danh sách này KHÔNG có tab nào của bạn đang mở  → extension nạp ở PROFILE KHÁC.",
    "     Chrome extension chỉ thấy tab cùng profile. Nạp lại `Load unpacked` ở ĐÚNG",
    "     profile đang đăng nhập account Flow (account có credit), rồi bấm ↻ quét.",
    "  ⓑ Danh sách đúng profile nhưng thiếu Flow  → chưa mở tab Flow. Mở",
    "     flow.google.com/project/<id> rồi bấm ↻.",
    "  ⓒ Có tab Flow trong danh sách mà vẫn bị lọc  → Flow đổi domain lần nữa.",
    "     Chọn tay tab đó trong dropdown (nó vẫn hiện, có dấu ⛔) rồi bấm 🔍 DÒ UI;",
    "     gửi Claude host mới để thêm vào HOSTS.",
  ].join("\n"));
}
$("refresh").onclick = listTabs;
listTabs();

// ── CDP ───────────────────────────────────────────────────────────────────────
let lastDetachReason = "";
chrome.debugger.onDetach.addListener((s, r) => { lastDetachReason = r; });
let fileChooser = null;   // chỉ dùng cho nhánh UPLOAD (đường lui)
chrome.debugger.onEvent.addListener((src, method, params) => {
  if (method === "Page.fileChooserOpened") fileChooser = { tabId: src.tabId, ...params };
});

function attach(tabId) {
  return new Promise((res, rej) => chrome.debugger.attach({ tabId }, "1.3", () => {
    const e = chrome.runtime.lastError;
    if (e && !/Another debugger|already attached/i.test(e.message)) rej(new Error(e.message));
    else res();
  }));
}
function cdp(tabId, method, params) {
  return new Promise((resolve, reject) => {
    chrome.debugger.sendCommand({ tabId }, method, params || {}, res => {
      if (chrome.runtime.lastError) reject(new Error(chrome.runtime.lastError.message));
      else resolve(res);
    });
  });
}
const cdpSoft = async (t, m, p) => { try { return await cdp(t, m, p); } catch (e) { return null; } };
async function evalIn(tabId, expression) {
  const r = await cdp(tabId, "Runtime.evaluate", { expression, returnByValue: true });
  if (r.exceptionDetails) throw new Error("JS lỗi trong tab Flow: " + (r.exceptionDetails.text || ""));
  return r.result.value;
}

// ═══════════════════════════════════════════════════════════════════════════════
// MỘT PHÉP ĐO DUY NHẤT. Đừng viết lại biểu thức này ở chỗ khác.
// ═══════════════════════════════════════════════════════════════════════════════
const JS_JOBSTATE = `(() => {
  const vis = el => el.offsetParent !== null || el.getClientRects().length > 0;
  const T = el => (el && el.textContent || '').replace(/\\s+/g,' ').trim();
  const mid = el => { const r = el.getBoundingClientRect();
                      return { x: r.x + r.width/2, y: r.y + r.height/2 }; };

  // ① hộp prompt — selector ĐO ĐƯỢC
  const box = document.querySelector('.base-prompt-box');
  const ed  = (box && box.querySelector('div[contenteditable="true"]'))
           || document.querySelector('div.ProseMirror[contenteditable="true"]')
           || document.querySelector('div[contenteditable="true"]');

  let text='', ph='', len=0;
  if (ed) {
    ph = [...ed.querySelectorAll('.prosemirror-placeholder,[class*="placeholder"]')].map(n=>T(n)).join(' ');
    const c = ed.cloneNode(true);
    c.querySelectorAll('.prosemirror-placeholder,[class*="placeholder"],.ProseMirror-widget,.ProseMirror-separator,br')
     .forEach(n=>n.remove());
    text = (c.textContent||'').replace(/\\u00a0/g,' ').trim(); len = text.length;
  }

  const dsc = el => ({ al: el.getAttribute('aria-label')||'', tx: T(el).slice(0,46),
                       dis: !!el.disabled || /disabled/.test(String(el.className)),
                       role: el.getAttribute('role')||el.tagName.toLowerCase(), ...mid(el) });

  const inBox = sel => box ? [...box.querySelectorAll(sel)].filter(vis) : [];
  const boxBtns = inBox('button,[role=button],[role=radio],[role=combobox]').map(dsc);

  // ③ chip ảnh: disabled = class chứa 'chip-container-disabled' (mode sai)
  const chips = inBox('[class*="chip-container"]').map(c => ({
    cls: String(c.className), al: c.getAttribute('aria-label')||'',
    disabled: /chip-container-disabled/.test(String(c.className)), ...mid(c) }));

  // slot Start / End của mode Frames.
  // 🔴 CHỈ khớp TEXT đúng bằng "Start"/"End". Bản trước còn khớp aria-label chứa "start|end"
  //    ⇒ nút GỬI (aria-label "Start generation") bị tính là SLOT. Khi slot đã có ảnh thì nó
  //    mất chữ "Start" (thành chip có nhãn cancel), pick("start") rơi vào nút gửi ⇒ bấm mờ ⇒
  //    "bảng chọn asset không mở". Dính thật 2026-09-10.
  const slots = boxBtns.filter(b => /^(start|end)$/i.test(b.tx));

  // ④ credit
  const creditTxt = [...document.querySelectorAll('*')]
      .filter(e => e.children.length === 0 && vis(e) && /credit/i.test(T(e)))
      .map(e => T(e))[0] || '';
  const insufficient = [...document.querySelectorAll('button')]
      .some(b => /insufficient/i.test(b.getAttribute('aria-label')||''));

  // ── bảng chọn asset «Select a frame image» (khi đang mở) ────────────────────
  // 🔴 BUG ĐÃ SỬA (demo 2026-09-10): 'input.search-input' khớp **HAI** ô —
  //    ô search ở HEADER TRANG (y≈25) và ô trong hộp thoại (y≈177). Bản trước lấy [0]
  //    ⇒ gõ caption vào ô header, hộp thoại không lọc gì, rồi bốc hàng đầu = **đính SAI ẢNH**
  //    mà prompt vẫn đúng ⇒ clip ra sai người, 100 credits, không dấu hiệu lỗi.
  //    ⇒ Nay BẮT BUỘC scope vào dialog.
  const dlg = document.querySelector('[role=dialog],mat-dialog-container,.cdk-overlay-pane');
  const search = dlg ? ([...dlg.querySelectorAll('input.search-input,input[placeholder*="Search assets" i]')]
                          .filter(vis)[0] || null) : null;

  // 🔴 BUG ĐÃ SỬA: hàng asset thật là button.asset-item[role=option]
  //    (component flow-add-menu-asset-item, thumbnail img.asset-thumbnail-image).
  //    Bản trước lọc theo hậu tố "Image"/"Video" ở cuối text — hậu tố đó CHỈ có ở bảng picker
  //    kiểu cũ; trong hộp thoại «Select a frame image» thì KHÔNG có ⇒ trả 0 hàng, job dừng oan.
  //    textContent của hàng là TÊN ĐẦY ĐỦ (chỗ "…" chỉ là CSS cắt), nên so tên vẫn đúng.
  //    ⛔ KHÔNG dùng dấu backtick trong khối comment này — nó nằm TRONG template literal.
  const rowEls = dlg ? [...dlg.querySelectorAll('button.asset-item,[role=option]')].filter(vis)
                     : [];
  // 🔴 KHONG DE-DUP O DAY. Ban truoc gop cac hang TRUNG TEN lai lam mot ⇒ nhom "3 anh cung
  //    ten" bi dem thanh 1 ⇒ so ung vien bang 1 ⇒ tool dinh HANG DAU ma khong hoi gi, va
  //    field pick thanh vo dung. De-dup chi duoc lam o cho LIET KE (nut 📋), khong o phep do.
  //    ⛔ Khong dung dau backtick trong khoi comment nay — no nam TRONG template literal.
  const assetRows = rowEls.map(e => ({ t: T(e), active: /asset-item-active/.test(String(e.className)),
                                       ...mid(e) }))
      .filter(o => o.t && o.t.length < 120);
  // 🔴 Nút xác nhận trong hộp thoại. Bản trước đòi ĐÚNG chuỗi "Add to prompt" và tìm trên
  //    CẢ TRANG ⇒ hộp thoại đổi nhãn (hoặc tự đóng sau khi chọn hàng) là job chết oan, dù
  //    ảnh có thể đã đính xong. Nay: ưu tiên đúng nhãn, rồi nới sang nút xác nhận khác
  //    TRONG hộp thoại, và luôn trả về danh sách nút của hộp thoại để chẩn đoán.
  const dlgBtns = dlg ? [...dlg.querySelectorAll('button')].filter(vis).map(dsc) : [];
  const addToPrompt =
        dlgBtns.find(b => /^add to prompt$/i.test(b.tx))
     || dlgBtns.find(b => /add to prompt|add to|use (this|image)|insert/i.test(b.tx + ' ' + b.al))
     || dlgBtns.find(b => /^(add|use|select|chọn|thêm|done|ok)$/i.test(b.tx) && !b.dis)
     || null;

  // ── chế độ AGENT ──────────────────────────────────────────────────────────
  // 🔴 ĐO ĐƯỢC 2026-09-10: thanh prompt có HAI chế độ. Bật Agent thì chip
  //    «Settings trigger» (Video · 360p · 8s) và slot Start/End **BIẾN MẤT**, thay bằng
  //    «Agent instructions» + «Settings»(tune) → mở panel *Agent settings* (Confirm before
  //    generating / model mặc định). Tức ở Agent mode thì KHÔNG làm được luồng Frames.
  //    ⇒ Phải phát hiện và TẮT Agent trước khi chạy.
  const agentBtn = boxBtns.find(b => /^agent$/i.test(b.tx));
  const agentOn = !!boxBtns.find(b => /agent instructions/i.test(b.al))
                  || (!boxBtns.some(b => /settings trigger/i.test(b.al)) && !!agentBtn);

  // tín hiệu đang chạy — BỎ hộp prompt ra khỏi phép đếm, nếu không placeholder
  // "What do you want to create?" tự làm busy=1 vĩnh viễn.
  const busyTxt = [...document.querySelectorAll('*')].filter(e =>
      e.children.length === 0 && vis(e) && !(box && box.contains(e))
      && /generating|rendering|đang tạo|作成中|生成中/i.test(T(e))).length;

  return JSON.stringify({
    boxFound: !!box, found: !!ed, text, len, ph,
    editorCls: ed ? String(ed.className).slice(0,40) : null,
    chips, nChips: chips.length, nChipsBad: chips.filter(c=>c.disabled).length,
    slots, boxBtns,
    creditTxt, insufficient,
    agentOn, agentBtn: agentBtn || null, dlgOpen: !!dlg, dlgBtns,
    searchOpen: !!search, searchRect: search ? mid(search) : null,
    assetRows: assetRows.slice(0,40), nAssetRows: assetRows.length,
    addToPrompt,
    edRect: ed ? mid(ed) : null,
    nFileInputs: document.querySelectorAll('input[type=file]').length,
    busyTxt, bars: document.querySelectorAll('[role=progressbar],[aria-busy="true"]').length,
    vids: document.querySelectorAll('video').length
  });
})()`;
const jobstate = tabId => evalIn(tabId, JS_JOBSTATE).then(JSON.parse);

// ① khớp nhãn CHỈ TRONG hộp prompt (bản v2.0 tìm cả trang ⇒ trúng "Add media menu" sai nút)
function pick(list, labels, { needEnabled = false } = {}) {
  for (const lb of labels) {
    const hit = list.find(b => (norm(b.al).includes(lb) || norm(b.tx).includes(lb))
                               && (!needEnabled || !b.dis));
    if (hit) return hit;
  }
  return null;
}

// ── input trusted ─────────────────────────────────────────────────────────────
async function key(tabId, o) {
  await cdp(tabId, "Input.dispatchKeyEvent", { type: "keyDown", ...o });
  await cdp(tabId, "Input.dispatchKeyEvent", { type: "keyUp", ...o });
}
const pressEnter = t => key(t, { windowsVirtualKeyCode:13, nativeVirtualKeyCode:13, key:"Enter", code:"Enter", text:"\r", unmodifiedText:"\r" });
const pressEsc   = t => key(t, { windowsVirtualKeyCode:27, nativeVirtualKeyCode:27, key:"Escape", code:"Escape" });
const selectAll  = t => key(t, { windowsVirtualKeyCode:65, nativeVirtualKeyCode:65, key:"a", code:"KeyA", modifiers:2 });
const backspace  = t => key(t, { windowsVirtualKeyCode:8,  nativeVirtualKeyCode:8,  key:"Backspace", code:"Backspace" });

async function click(tabId, pt) {
  await cdp(tabId, "Input.dispatchMouseEvent", { type:"mouseMoved",   x:pt.x, y:pt.y });
  await cdp(tabId, "Input.dispatchMouseEvent", { type:"mousePressed", x:pt.x, y:pt.y, button:"left", clickCount:1 });
  await cdp(tabId, "Input.dispatchMouseEvent", { type:"mouseReleased",x:pt.x, y:pt.y, button:"left", clickCount:1 });
  await sleep(120);
}

// ═══════════════════════════════════════════════════════════════════════════════
// ② SETTINGS — Video + Frames + 16:9 + x1. Làm MỘT LẦN/lô, settings của Flow bám project.
// ═══════════════════════════════════════════════════════════════════════════════
// Tắt chế độ Agent nếu đang bật — điều kiện SỐNG CÒN để có slot Start/End (xem JS_JOBSTATE).
async function ensureClassicBar(tabId) {
  let st = await jobstate(tabId);
  if (!st.agentOn) return { changed: false, st };
  if (!st.agentBtn) throw new Error("Thanh prompt đang ở chế độ AGENT mà không thấy chip «Agent» "
                                  + "để tắt. Tắt tay rồi chạy lại.");
  await click(tabId, st.agentBtn);
  await sleep(1200);
  st = await jobstate(tabId);
  if (st.agentOn) throw new Error("Bấm chip «Agent» rồi mà vẫn ở chế độ Agent. Tắt tay rồi chạy lại.");
  return { changed: true, st };
}

async function openSettings(tabId) {
  await ensureClassicBar(tabId);
  const st = await jobstate(tabId);
  const trg = pick(st.boxBtns, ["settings trigger", "settings"]);
  if (!trg) throw new Error("Không thấy «Settings trigger» trong thanh prompt.");
  await click(tabId, trg); await sleep(700);
  return jobstate(tabId);
}
async function clickRadio(tabId, want) {
  const st = await evalIn(tabId, `(() => {
    const vis = el => el.offsetParent !== null || el.getClientRects().length > 0;
    return JSON.stringify([...document.querySelectorAll('[role=radio]')].filter(vis).map(r => {
      const b = r.getBoundingClientRect();
      return { t: (r.textContent||'').replace(/\\s+/g,' ').trim(),
               x: b.x + b.width/2, y: b.y + b.height/2 };
    }));
  })()`).then(JSON.parse);
  // text của radio là "videocamVideo" (ligature + nhãn) ⇒ so bằng "chứa"
  const hit = st.find(r => norm(r.t).includes(norm(want)));
  if (!hit) return false;
  await click(tabId, hit); await sleep(450);
  return true;
}
async function setupSettings(tabId) {
  const out = [];
  await openSettings(tabId);
  for (const w of ["Video", "Frames", "16:9", "x1"])
    out.push(`${w}:${await clickRadio(tabId, w) ? "✓" : "—"}`);
  await pressEsc(tabId); await sleep(500);
  const st = await jobstate(tabId);
  return { line: out.join(" · "), credit: st.creditTxt, insufficient: st.insufficient, st };
}

// ═══════════════════════════════════════════════════════════════════════════════
// ⭐ ĐÍNH ẢNH TỪ THƯ VIỆN PROJECT (luồng chính — không upload gì)
//    slot Start → picker → gõ caption → chọn hàng → Add to prompt → kiểm chip
// ═══════════════════════════════════════════════════════════════════════════════
// 🔴 DỌN THANH PROMPT TRƯỚC MỖI JOB — điều kiện để job N+1 chạy được sau khi job N gãy.
//    Job gãy giữa đường hay để lại ẢNH TRONG SLOT + chữ trong ô. Slot đã có ảnh thì mất
//    chữ "Start" ⇒ không mở lại được bảng chọn. Nút «Clear prompt» xoá CẢ chữ LẪN chip
//    (đo tay 2026-09-10: prompt 0 ký · 0 chip · Start/End trống).
async function resetBar(tabId) {
  let st = await jobstate(tabId);
  if (!st.nChips && !st.len) return st;
  const clr = pick(st.boxBtns, ["clear prompt"]);
  if (clr) { await click(tabId, clr); await sleep(700); st = await jobstate(tabId); }
  if (st.nChips || st.len) {                       // đường lui: gỡ từng chip + xoá chữ
    for (const c of st.chips) { await click(tabId, c); await sleep(400); }
    await clearPrompt(tabId);
    st = await jobstate(tabId);
  }
  if (st.nChips) throw new Error(`Còn ${st.nChips} ảnh trong thanh prompt mà không gỡ được — `
                               + "gỡ tay (bấm ✕ trên chip) rồi START lại.");
  add("đã dọn thanh prompt (ảnh + chữ của lượt trước)");
  return st;
}

async function openAssetPicker(tabId) {
  let st = await jobstate(tabId);
  if (st.searchOpen) return st;
  if (st.agentOn) { const r = await ensureClassicBar(tabId); st = r.st; add("đã TẮT chế độ Agent"); }
  st = await resetBar(tabId);

  // 🔴 BA THỨ ĐÃ SỬA sau khi job 48 chết ở đây (2026-09-10):
  //  ① CHỜ 900ms rồi kết luận là quá ngắn — hộp thoại có lúc mở chậm hơn. Nay POLL tới 6s.
  //  ② ĐO LẠI toạ độ NGAY TRƯỚC khi bấm — resetBar vừa gỡ chip nên thanh prompt xê dịch,
  //     toạ độ đo trước đó có thể đã cũ.
  //  ③ Trượt lần đầu thì THỬ NÚT KIA (slot Start ↔ nút thêm ảnh) trước khi bỏ cuộc.
  let clickedWhat = "";
  for (let attempt = 0; attempt < 2; attempt++) {
    st = await jobstate(tabId);                                  // ②
    const a = pick(st.slots, ["start"]), b = pick(st.boxBtns, CFG().addimg);
    const target = attempt === 0 ? (a || b) : (b || a);
    if (!target || (attempt === 1 && target === (a || b))) continue;
    clickedWhat = target.tx || target.al || "?";
    await click(tabId, target);
    for (let i = 0; i < 12; i++) {                               // ①
      await sleep(500);
      st = await jobstate(tabId);
      if (st.searchOpen) return st;
    }
  }
  throw new Error("Bấm rồi mà bảng chọn asset không mở sau 6 giây."
    + LF + `  đã bấm: ${JSON.stringify(clickedWhat) || "(không thấy nút nào)"}`
    + LF + `  slot thấy được: ${(st.slots || []).map(s => s.tx || s.al).join(" / ") || "(không có)"}`
    + LF + `  chip ảnh còn lại: ${st.nChips}  ·  ô prompt: ${st.len} ký`
    + LF + "  → Bấm 🔍 DÒ UI, gửi Claude phần «nút trong .base-prompt-box».");
}

// ⭐ NHIỀU ẢNH CÙNG TÊN — Flow tự đặt caption nên 2–3 ảnh trùng tên là chuyện thường.
//    `pick` (1-based) chỉ đích danh ảnh thứ mấy trong nhóm cùng tên đó.
//    Không khai `pick` mà có >1 ứng viên ⇒ DỪNG + in danh sách kèm số để chọn.
//    ⚠️ Thứ tự đếm = thứ tự hàng trong bảng chọn (đang sắp theo `Recent`) ⇒ gen thêm ảnh
//       mới thì thứ tự ĐỔI. Chốt `pick` xong nên chạy luôn, đừng để cách hôm.
async function attachAsset(tabId, caption, pickN) {
  let st = await openAssetPicker(tabId);
  // gõ caption vào ô search
  await click(tabId, st.searchRect);
  await selectAll(tabId); await backspace(tabId);
  await cdp(tabId, "Input.insertText", { text: caption });
  await sleep(1400);
  st = await jobstate(tabId);
  const want = norm(caption);
  const rows = st.assetRows;
  if (!rows.length) throw new Error(`Search "${caption}" không ra asset nào. Bấm 📋 LIỆT KÊ ASSET `
                                  + `để lấy TÊN ĐÚNG rồi sửa jobs.jsonl.`);
  // 🔴 phải khớp DUY NHẤT. Nhiều kết quả mà chọn hàng đầu = rủi ro đính SAI ẢNH,
  //    prompt vẫn đúng ⇒ clip ra sai người, 100 credits, không dấu hiệu lỗi.
  const eq = rows.filter(r => norm(r.t) === want);
  const pre = rows.filter(r => norm(r.t).startsWith(want));
  const cand = eq.length ? eq : (pre.length ? pre : rows);
  let row;
  if (cand.length === 1) {
    row = cand[0];
  } else if (pickN && pickN >= 1 && pickN <= cand.length) {
    row = cand[pickN - 1];
    add(`   ⚠ ${cand.length} ảnh cùng tên — dùng pick:${pickN}`);
  } else {
    throw new Error(`"${caption}" khớp ${cand.length} ảnh — DỪNG để không đính sai ảnh.\n`
      + cand.map((r, k) => `   pick:${k + 1}  ${r.t}${r.active ? "  ← đang chọn" : ""}`).join("\n")
      + "\n➡️ Cách 1: mở Flow, bấm slot Start, gõ tên đó, xem preview từng hàng để biết ảnh mình"
      + ' cần là thứ mấy, rồi thêm  "pick":<số>  vào dòng job đó.'
      + "\n➡️ Cách 2 (nhanh): điền ô «pick mặc định khi TRÙNG TÊN» = 1 — tool tự lấy hàng đầu cho"
      + " MỌI job trùng tên. Bạn nhận rủi ro đính sai ảnh; hợp khi mấy ảnh trùng tên nhìn na ná nhau."
      + (pickN ? `\n   (job đang khai pick:${pickN} — ngoài khoảng 1..${cand.length})` : ""));
  }
  const chips0 = st.nChips;
  await click(tabId, row);

  // 🔴 BA KẾT CỤC KHÁC NHAU sau khi bấm hàng — đừng chỉ chờ đúng một cái:
  //    ⓐ hộp thoại còn mở, có nút xác nhận  → bấm nút
  //    ⓑ hộp thoại TỰ ĐÓNG và ảnh ĐÃ ĐÍNH   → xong rồi, đừng báo lỗi (ca dính 2026-09-10)
  //    ⓒ không ra gì                        → mới là lỗi, và in ra ĐỦ nút của hộp thoại
  let clicked = false;
  for (let i = 0; i < 10; i++) {
    await sleep(500);
    st = await jobstate(tabId);
    if (st.nChips > chips0) { clicked = true; break; }        // ⓑ tự đính xong
    if (st.addToPrompt) {                                     // ⓐ
      await click(tabId, st.addToPrompt);
      clicked = true;
      break;
    }
    if (!st.dlgOpen) break;                                   // hộp thoại đóng mà chưa có chip
  }
  if (!clicked && !st.dlgOpen && st.nChips <= chips0)
    throw new Error("Bấm hàng asset xong thì hộp thoại ĐÓNG mà ảnh KHÔNG được đính.\n"
                  + "  → Bấm 🔍 DÒ UI rồi gửi Claude phần «nút trong .base-prompt-box».");
  if (!clicked)
    throw new Error("Không tìm được nút xác nhận trong hộp thoại. Nút hộp thoại đang có:\n  "
                  + (st.dlgBtns || []).map(b => JSON.stringify(b.tx || b.al)).join(" · ")
                  + "\n  → gửi dòng này cho Claude để thêm nhãn.");

  // xác nhận cuối: chip phải TĂNG và KHÔNG disabled
  for (let i = 0; i < 16 && st.nChips <= chips0; i++) { await sleep(500); st = await jobstate(tabId); }
  if (st.nChips <= chips0)
    throw new Error("Đã bấm xác nhận mà chip ảnh không xuất hiện trong thanh prompt.");
  if (st.nChipsBad)
    throw new Error("Chip ảnh ở trạng thái DISABLED (class `chip-container-disabled`) — "
                  + "SAI MODE. Ảnh frame chỉ hợp với mode «Frames», mode «Ingredient» sẽ từ chối nó. "
                  + "Bấm ⚙ CHỐT SETTINGS rồi chạy lại.");
  return { row: row.t, nChips: st.nChips };
}

// ── đường lui: UPLOAD file từ đĩa (chỉ dùng khi job khai `first` là đường dẫn) ──
async function attachUpload(tabId, path) {
  await cdpSoft(tabId, "Page.enable"); await cdpSoft(tabId, "DOM.enable");
  fileChooser = null;
  const interc = await cdpSoft(tabId, "Page.setInterceptFileChooserDialog", { enabled: true });
  let st = await openAssetPicker(tabId);
  const up = pick(st.boxBtns.concat(st.assetRows.map(r => ({ al:"", tx:r.t, x:r.x, y:r.y }))),
                  ["upload media", "upload", "tải lên"]);
  if (up) { await click(tabId, up); await sleep(800); }
  let route = null;
  for (let i = 0; i < 20 && !(fileChooser && fileChooser.tabId === tabId); i++) await sleep(200);
  if (fileChooser && fileChooser.tabId === tabId) {
    await cdp(tabId, "DOM.setFileInputFiles", { files:[path], backendNodeId:fileChooser.backendNodeId });
    route = "upload qua file-chooser";
  } else {
    const doc = await cdpSoft(tabId, "DOM.getDocument", { depth: 1 });
    const q = doc && await cdpSoft(tabId, "DOM.querySelector",
                                   { nodeId: doc.root.nodeId, selector: 'input[type=file]' });
    if (q && q.nodeId && await cdpSoft(tabId, "DOM.setFileInputFiles", { files:[path], nodeId:q.nodeId }) !== null)
      route = "upload qua input[type=file]";
  }
  await cdpSoft(tabId, "Page.setInterceptFileChooserDialog", { enabled: false });
  if (!route) throw new Error(`Không upload được (intercept: ${interc ? "ok" : "KHÔNG hỗ trợ"}). `
                            + "Dùng field \"asset\" (tên asset đã có trong project) thay cho \"first\".");
  return route;
}

// ── prompt ────────────────────────────────────────────────────────────────────
async function focusEditor(tabId) {
  await evalIn(tabId, `((document.querySelector('.base-prompt-box div[contenteditable="true"]')
                      || document.querySelector('div[contenteditable="true"]'))||{focus(){}}).focus()`);
  await sleep(120);
}
async function typePrompt(tabId, text) {
  await focusEditor(tabId);
  await selectAll(tabId);
  await cdp(tabId, "Input.insertText", { text });
  await sleep(550);
  let st = await jobstate(tabId);
  if (st.len > text.length * 1.3) {            // chống nối chuỗi prompt
    await selectAll(tabId); await backspace(tabId); await sleep(180);
    await cdp(tabId, "Input.insertText", { text }); await sleep(550);
    st = await jobstate(tabId);
  }
  if (st.len < Math.min(24, text.length * 0.6))
    throw new Error(`insertText không vào editor (${st.len}/${text.length} ký) — tab đang bị `
                  + "debugger khác giữ (F12 / Claude-in-Chrome)? Mở tab Flow MỚI.");
  return st;
}
const clearPrompt = async tabId => { await focusEditor(tabId); await selectAll(tabId); await backspace(tabId); await sleep(150); };

// ── gửi ───────────────────────────────────────────────────────────────────────
async function submit(tabId, promptText) {
  const head = norm(promptText).slice(0, 24);
  const b4 = await jobstate(tabId);
  await pressEnter(tabId); await sleep(1200);
  let st = await jobstate(tabId);
  if (norm(st.text).includes(head)) {
    const go = pick(st.boxBtns, CFG().submit, { needEnabled: true });
    if (go) { await click(tabId, go); await sleep(1200); st = await jobstate(tabId); }
  }
  const cleared = !norm(st.text).includes(head);
  const started = st.busyTxt > b4.busyTxt || st.bars > b4.bars || st.vids > b4.vids
                  || st.nChips < b4.nChips;
  return { cleared, started, st };
}
async function waitSlot(tabId, maxPend, capSec) {
  const t0 = Date.now();
  while (running && (Date.now() - t0) / 1000 < capSec) {
    const st = await jobstate(tabId);
    if (Math.max(st.busyTxt, st.bars) < maxPend) return { ok: true };
    await sleep(3000);
  }
  return { ok: false };
}

// ── sổ đã-gửi ────────────────────────────────────────────────────────────────
// ⚡ SỔ ĐÃ-GỬI — MỖI JOB MỘT KHOÁ RIÊNG, không phải một object chung.
// 🔴 Bản trước là `sent: {…}`: ghi = đọc-sửa-ghi cả object. Chạy ĐA LUỒNG thì hai panel
//    đọc cùng một bản, mỗi bên thêm job của mình rồi ghi đè nhau ⇒ MẤT entry ⇒ lần chạy sau
//    gen lại job đã gửi = mất credit. Một-khoá-một-job thì mỗi lượt ghi độc lập, không đè.
const SENT = "s_";
const ledgerGet = () => chrome.storage.local.get(null).then(all => {
  const out = {};
  for (const k in all) if (k.startsWith(SENT)) out[k.slice(SENT.length)] = all[k];
  return out;
});
const ledgerAdd = id => chrome.storage.local.set({ [SENT + id]: new Date().toISOString() });
const ledgerClear = async () => {
  const all = await chrome.storage.local.get(null);
  const keys = Object.keys(all).filter(k => k.startsWith(SENT)).concat(["sent"]);
  await chrome.storage.local.remove(keys);
  return keys.length - 1;
};

// ── nạp job ──────────────────────────────────────────────────────────────────
function parseJobs(raw) {
  const out = [];
  raw.split("\n").forEach((line, i) => {
    const s = line.trim();
    if (!s || s.startsWith("#")) return;
    if (s.startsWith("{")) {
      try {
        const j = JSON.parse(s);
        out.push({ id: j.id || `line-${i+1}`, mode: j.mode || "frames",
                   asset: j.asset || null, image: j.first || j.image || null,
                   pick: j.pick || null,
                   prompt: j.prompt || "", duration: j.duration || null });
        return;
      } catch (e) {}
    }
    // 🔴 BUG v2.0 ĐÃ SỬA: id cũ là `line-N` ⇒ sổ đã-gửi khoá theo SỐ DÒNG. Nạp một file
    //    prompt KHÁC thì `line-1` đã nằm trong sổ ⇒ prompt mới bị **BỎ QUA oan**, im lặng.
    //    Nay khoá theo NỘI DUNG: cùng prompt = cùng khoá (resume đúng), prompt khác = khoá
    //    khác (không đụng nhau). Đây là điều kiện để luồng v1 dùng được sổ.
    out.push({ id: "t:" + hash(s), mode: "text", asset: null, image: null,
               prompt: s, duration: null, line: i + 1 });
  });
  return out;
}
// djb2 — đủ để phân biệt prompt, không cần chống đụng độ kiểu mật mã
function hash(s) {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
  return (h >>> 0).toString(36);
}

// ═══════════════════════════════════════════════════════════════════════════════
// 🔍 DÒ UI
// ═══════════════════════════════════════════════════════════════════════════════
$("diag").onclick = async () => {
  const tabId = parseInt($("tabsel").value);
  if (!tabId) return say("Chọn tab Flow trước đã.");
  say("Đang dò UI…");
  try {
    await attach(tabId);
    const st = await jobstate(tabId);
    const c = CFG();
    const go = pick(st.boxBtns, c.submit), ai = pick(st.boxBtns, c.addimg);
    const trg = pick(st.boxBtns, ["settings"]);
    say([
      `.base-prompt-box: ${st.boxFound ? "✓" : "🔴 KHÔNG THẤY — đã mở project chưa?"}`,
      `Ô prompt: ${st.found ? "✓ " + st.editorCls : "🔴 KHÔNG THẤY"}  placeholder=${JSON.stringify(st.ph)}`,
      `  đang chứa: ${st.len} ký${st.len ? " → " + JSON.stringify(st.text.slice(0,44)) : " (trống)"}`,
      `Slot frame: ${st.slots.length ? st.slots.map(s=>s.tx||s.al).join(" / ") : "— (chưa ở mode Frames?)"}`,
      `Chip ảnh: ${st.nChips} (disabled: ${st.nChipsBad})`,
      `Nút GỬI: ${go ? `✓ «${go.al||go.tx}»${go.dis?" ·mờ":" ·sáng"}` : "🔴 không khớp nhãn"}`,
      `Nút THÊM ẢNH: ${ai ? `✓ «${ai.al||ai.tx}»` : "🔴 không khớp nhãn"}`,
      `Settings trigger: ${trg ? `✓ «${trg.tx||trg.al}»` : "🔴 không thấy"}`,
      `💰 CREDIT: ${st.creditTxt || "(không đọc được)"}${st.insufficient ? "   🔴 HẾT CREDIT" : ""}`,
      `Bảng chọn asset đang mở: ${st.searchOpen ? "✓" : "không"} · asset thấy được: ${st.nAssetRows}`,
      `Tín hiệu đang chạy: busy=${st.busyTxt} progressbar=${st.bars} video=${st.vids}`,
      "",
      `— nút trong .base-prompt-box —`,
      ...st.boxBtns.map(b => `  [${b.role}] ${JSON.stringify(b.al||b.tx)}${b.dis?" ·mờ":""}`),
      "",
      st.boxFound && st.found ? "✅ Đủ để chạy ⚙ CHỐT SETTINGS rồi DRY-RUN." : "🔴 Sửa mục 🔴 rồi dò lại.",
    ].join("\n"));
  } catch (e) { say("🔴 Không dò được: " + e.message); }
  finally { try { chrome.debugger.detach({ tabId }); } catch (e) {} }
};

// ═══════════════════════════════════════════════════════════════════════════════
// ⚙ CHỐT SETTINGS  ·  📋 LIỆT KÊ ASSET
// ═══════════════════════════════════════════════════════════════════════════════
$("setup").onclick = async () => {
  const tabId = parseInt($("tabsel").value);
  if (!tabId) return say("Chọn tab Flow trước đã.");
  say("Đang chốt settings Video + Frames + 16:9 + x1…");
  try {
    await attach(tabId);
    const r = await setupSettings(tabId);
    say([`Radio đã bấm: ${r.line}`,
         `💰 ${r.credit || "(không đọc được giá)"}${r.insufficient ? "   🔴 HẾT CREDIT — chạy thật sẽ không gửi được" : ""}`,
         `Slot frame: ${r.st.slots.map(s=>s.tx||s.al).join(" / ") || "— (chưa thấy Start/End)"}`,
         "", r.st.slots.length ? "✅ Đúng mode Frames." : "⚠ Chưa thấy Start/End — mở ⚙ bằng tay kiểm lại."].join("\n"));
  } catch (e) { say("🔴 " + e.message); }
  finally { try { chrome.debugger.detach({ tabId }); } catch (e) {} }
};

$("listassets").onclick = async () => {
  const tabId = parseInt($("tabsel").value);
  if (!tabId) return say("Chọn tab Flow trước đã.");
  say("Đang mở bảng chọn asset và liệt kê…");
  try {
    await attach(tabId);
    let st = await openAssetPicker(tabId);

    // 🔴 BA LOI CUA BAN TRUOC — bat duoc khi user thay project 102 asset ma no chi liet ke 15:
    //  ① O SEARCH CON CHU cua job truoc ⇒ danh sach bi LOC ⇒ cang bam cang it. Phai XOA.
    //  ② CUON SAI CHO: cuon o `searchRect.y + 200` — diem do roi vao O PREVIEW ben PHAI,
    //     khong phai danh sach ben TRAI ⇒ danh sach khong cuon ⇒ chi lay duoc trang dau.
    //     Nay cuon NGAY TREN mot hang asset that.
    //  ③ Tab loc co the dang o Videos/Characters thay vi All.
    if (st.searchRect) {                                   // ①
      await click(tabId, st.searchRect);
      await selectAll(tabId); await backspace(tabId);
      await sleep(900);
    }
    st = await jobstate(tabId);
    const allTab = (st.dlgBtns || []).find(b => /^all$/i.test(b.tx));   // ③
    if (allTab) { await click(tabId, allTab); await sleep(800); }

    const seen = new Map();
    let stall = 0;
    for (let i = 0; i < 60 && stall < 5; i++) {
      st = await jobstate(tabId);
      const before = seen.size;
      st.assetRows.forEach(r => seen.set(r.t, (seen.get(r.t) || 0) + 1));
      const anchor = st.assetRows[Math.floor(st.assetRows.length / 2)] || st.searchRect;  // ②
      if (anchor)
        await cdp(tabId, "Input.dispatchMouseEvent",
                  { type: "mouseWheel", x: anchor.x, y: anchor.y, deltaX: 0, deltaY: 500 });
      await sleep(450);
      stall = seen.size > before ? 0 : stall + 1;
      if (i % 8 === 7) add(`   … đã gom ${seen.size} tên`);
    }
    await pressEsc(tabId);
    const list = [...seen.keys()].map(t => t.replace(/(Image|Video)$/, "").trim());
    const dup = [...seen.entries()].filter(([, n]) => n > 1);
    say([`📋 ${list.length} TÊN asset trong project:`,
         ...list.map((t, i) => `  ${String(i + 1).padStart(3)}  ${t}`),
         "",
         dup.length ? `⚠ ${dup.length} tên thấy nhiều lần trong danh sách — job dùng tên đó cần "pick"`
                    : "✓ không thấy tên nào lặp trong danh sách",
         "ⓘ Cuộn tới khi 5 lượt liền không ra tên mới thì dừng. Vẫn thiếu so với số asset thật thì",
         "  danh sách bị Flow ảo hoá sâu — gửi Claude con số này để nới vòng cuộn.",
        ].join("\n"));
  } catch (e) { say("🔴 " + e.message); }
  finally { try { chrome.debugger.detach({ tabId }); } catch (e) {} }
};

// ═══════════════════════════════════════════════════════════════════════════════
// ▶ START
// ═══════════════════════════════════════════════════════════════════════════════
$("start").onclick = async () => {
  if (running) return;
  const tabId = parseInt($("tabsel").value);
  if (!tabId) return say("Chọn tab Flow trước đã.");
  const jobs = parseJobs($("prompts").value);
  if (!jobs.length) return say("Chưa có job nào.");
  const dry = $("dryrun").checked;
  const delay = Math.max(5, parseInt($("delay").value) || 20);
  const maxJobs = Math.max(1, parseInt($("maxjobs").value) || 5);
  const maxPend = Math.max(1, parseInt($("maxpend").value) || 2);
  const from = Math.max(1, parseInt($("startidx").value) || 1);
  // ⚡ ĐA LUỒNG: mỗi panel nhận một KHOẢNG dòng. Trống = tới hết danh sách.
  const to = Math.min(jobs.length, parseInt($("endidx").value) || jobs.length);
  let i = from - 1;
  if (to < from) return say(`🔴 «ĐẾN dòng» (${to}) nhỏ hơn «Bắt đầu từ dòng» (${from}).`);

  // 🔴 idx phải NAMESPACE theo khoảng — chạy 3 luồng mà dùng chung một khoá `idx` thì
  //    luồng nào ghi sau sẽ đè tiến độ của luồng khác.
  const IDXK = `idx_${from}_${to}`;
  chrome.storage.local.set({ prompts: $("prompts").value, delay });
  const ledger = await ledgerGet();

  try { await attach(tabId); await evalIn(tabId, "1"); }
  catch (e) {
    return say(/Another debugger|already attached|not attached/i.test(String(e.message))
      ? "🔴 Tab này đang bị công cụ khác debug (Claude-in-Chrome, hoặc F12 đang mở).\n"
        + "Đóng F12 / mở 1 TAB FLOW MỚI, bấm ↻, chọn tab mới rồi Start."
      : "Không attach được debugger: " + e.message);
  }

  // ④ CHẶN CREDIT trước khi làm gì
  const st0 = await jobstate(tabId);
  // 🔴 PHẢI NÓI THẲNG NGAY TỪ ĐẦU: dry-run KHÔNG tạo clip nào. Bản trước chỉ ghi
  //    "không tốn credit" rồi kết thúc bằng "✅ XONG cả danh sách" ⇒ người dùng chạy xong,
  //    vào Flow không thấy gì, tưởng tool hỏng. Lỗi giao tiếp, không phải lỗi cơ chế.
  say(dry ? "🧪 CHẠY KHÔ (DRY-RUN)\n"
          + "   Tool sẽ đính ảnh + gõ prompt + kiểm nút gửi, rồi XOÁ đi.\n"
          + "   ⛔ SẼ KHÔNG CÓ CLIP NÀO ĐƯỢC TẠO — đó là ĐÚNG. Chỉ để kiểm luồng, 0 credit.\n"
          + "   Muốn gen thật: BỎ TICK «DRY-RUN» rồi bấm START lại."
          : "🔴 CHẠY THẬT — mỗi job sẽ trừ credit.");
  // ⓘ Chuỗi "Generating will use N credits" CHỈ có bên trong popover Settings ⇒ popover đóng
  //    thì không đọc được, và đó là BÌNH THƯỜNG — đừng để nó trông như lỗi.
  add(st0.creditTxt ? `💰 ${st0.creditTxt}`
                    : "ⓘ giá credit chỉ hiện trong popover ⚙ Settings — bấm ⚙ CHỐT SETTINGS để xem");
  if (st0.insufficient && !dry) {
    return add("🔴 Flow báo HẾT CREDIT (`Insufficient credits warning`) — DỪNG, không bấm gì.\n"
             + "   Đổi sang account có credit, hoặc chạy DRY-RUN để nghiệm thu luồng.");
  }

  // kiem nhanh danh sach TRUOC khi cham vao Flow — lech la thay ngay o dong dau
  const nAsset = jobs.filter(j => j.asset).length;
  const nameUse = {};
  jobs.forEach(j => { if (j.asset) nameUse[j.asset] = (nameUse[j.asset] || 0) + 1; });
  const needPick = jobs.filter(j => j.asset && nameUse[j.asset] > 1 && !j.pick);
  const nDup = needPick.length;
  add(`danh sách: ${jobs.length} job · có asset ${nAsset}/${jobs.length}`
      + (nDup ? ` · ${nDup} job trùng tên CHƯA khai pick` : ""));
  if (nAsset < jobs.length && jobs.some(j => j.mode === "frames"))
    add(`⚠ ${jobs.length - nAsset} job thiếu "asset" — rất có thể danh sách là BẢN CŨ, nạp lại file.`);
  if (nDup) {
    const names = [...new Set(needPick.map(j => j.asset))];
    add(`🔴 ${nDup} job dùng CHUNG ${names.length} tên asset mà chưa khai "pick":`);
    names.forEach(nm => add(`     ${nameUse[nm]} job × ${JSON.stringify(nm)}`
                          + `  → khai pick 1..${nameUse[nm]} cho từng job`));
    add(`   ⛔ Ô «pick mặc định» KHÔNG áp cho mấy job này — lấy hàng đầu cho cả nhóm thì`
      + ` ${nameUse[names[0]]} clip ra GIỐNG HỆT nhau. Tool sẽ dừng ở job đầu của nhóm.`);
  }

  add(`khoảng chạy: dòng ${from} → ${to}  (${to - from + 1} job)`);
  running = true; $("bar").max = Math.min(to - from + 1, maxJobs);
  let done = 0, fails = 0;

  const v1 = RM() === "v1";
  while (running && i < to && done < maxJobs) {
    // v1: mọi dòng chạy như prompt CHỮ, bỏ hẳn ảnh/mode/hàng đợi (đúng luồng bản 1.1)
    const j = v1 ? { ...jobs[i], mode: "text", asset: null, image: null } : jobs[i];
    add(`\n── ${i+1}/${jobs.length} · ${j.id} · mode=${j.mode} ──`);
    if (ledger[j.id] && !dry) {
      add(`⏭ BỎ QUA — sổ ghi đã gửi lúc ${ledger[j.id]}.`);
      i++; $("bar").value = ++done; continue;
    }
    try {
      if (!dry && j.mode !== "text") {
        const w = await waitSlot(tabId, maxPend, 360);
        if (!w.ok) { add("🔴 Chờ 6 phút queue vẫn đầy — DỪNG. Không tự bấm lại (100 credits/clip)."); running = false; break; }
      }

      if (j.asset) {
        // 🔴 pick MAC DINH chi duoc ap khi ten asset do CHI CO MOT JOB dung.
        //    Neu 2–3 job dung cung ten (nhom "3 anh cung ten", moi job can MOT anh khac),
        //    lay hang dau cho ca nhom = 3 clip GIONG HET NHAU, im lang. Luc do phai DUNG
        //    va bat khai pick tung job.
        const dp = (nameUse[j.asset] === 1) ? (parseInt($("defpick").value) || 0) : 0;
        add("ảnh: " + JSON.stringify((await attachAsset(tabId, j.asset, j.pick || dp)).row));
      }
      // 🔴 mode frames MA THIEU `asset` = danh sach trong panel LA BAN CU.
      //    Panel tu khoi phuc o prompt tu chrome.storage, nen file sua tren dia KHONG tu vao
      //    panel. Bản trước âm thầm rơi vào nhánh UPLOAD (đường chưa kiểm) rồi báo lỗi upload
      //    — chẩn đoán chạy theo triệu chứng sai. Nay dừng đúng chỗ, nói đúng việc phải làm.
      else if (j.mode === "frames")
        throw new Error([
          `Job "${j.id}" không có field "asset" ⇒ danh sách trong panel là BẢN CŨ.`,
          "  → Bấm lại nút chọn file, nạp lại jobs.jsonl (bản mới có \"asset\"), rồi START.",
          "  → Muốn upload ảnh từ đĩa thật thì đổi dòng job sang \"mode\":\"upload\".",
        ].join(LF));
      else if (j.image) add("ảnh: " + await attachUpload(tabId, j.image));
      else if (j.mode !== "text") add("⚠ job không khai `asset` lẫn `first` — chạy như text");

      const st = await typePrompt(tabId, j.prompt);
      add(`prompt: ${st.len}/${j.prompt.length} ký đã vào ô`);

      if (dry) {
        const go = pick(st.boxBtns, CFG().submit);
        add(`🧪 nút gửi: ${go ? (go.dis ? "🔴 ĐANG MỜ" : "✓ sáng") : "🔴 không thấy"} → KHÔNG bấm`);
        add(`🧪 chip ảnh: ${st.nChips} (disabled ${st.nChipsBad})`);
        await clearPrompt(tabId);
      } else {
        const r = await submit(tabId, j.prompt);
        add(`gửi: ô prompt ${r.cleared ? "sạch ✓" : "🔴 CÒN CHỮ"} · bắt đầu chạy: ${r.started ? "✓" : "🔴 không thấy"}`);
        if (r.cleared || r.started) { await ledgerAdd(j.id); fails = 0; }
        else if (++fails >= 2) {
          add("🔴 2 job liền không xác nhận được — DỪNG. Bấm 🔍 DÒ UI xem Flow đổi gì. "
            + "⛔ Đừng bấm START lại trước khi biết lý do.");
          running = false; break;
        }
      }
    } catch (e) {
      if (/not attached/i.test(String(e.message))) {
        add(`⚠ debugger đứt (${lastDetachReason || "?"}) — nối lại sau 3s…`);
        await sleep(3000);
        try { await attach(tabId); continue; } catch (e2) { add("🔴 nối lại thất bại: " + e2.message); running = false; break; }
      }
      add("🔴 " + e.message); running = false; break;
    }
    chrome.storage.local.set({ [IDXK]: i + 1 });
    i++; $("startidx").value = i + 1; $("bar").value = ++done;
    if (running && done < maxJobs && i < to)
      for (let s = 0; s < delay * 2 && running; s++) await sleep(500);
  }

  try { chrome.debugger.detach({ tabId }); } catch (e) {}
  // ⚡ DÒNG KẾT THÚC — chạy đa luồng thì đây là thứ phải đọc: luồng này dừng ở dòng nào,
  //    luồng kế tiếp bắt đầu từ đâu.
  add(`\n── khoảng ${from}→${to} · đã xử lý ${done} job · DỪNG SAU DÒNG ${i} `
    + `· dòng kế tiếp: ${i + 1 <= to ? i + 1 : "(hết khoảng)"} ──`);
  add(done >= maxJobs && i < to
      ? `⏹ Hết trần ${maxJobs} job/lượt. START để chạy tiếp từ dòng ${i + 1} (vẫn trong khoảng ${from}→${to}).`
      : (i >= to
          ? (dry ? `\n🧪 CHẠY KHÔ XONG — kiểm ${done} job, luồng ${done ? "SẠCH" : "chưa chạy được"}.\n`
                 + "⛔ KHÔNG có clip nào được tạo, và đó là ĐÚNG: dry-run không bấm nút gửi.\n"
                 + "➡️ Vào Flow sẽ KHÔNG thấy gì mới. Muốn có clip thật:\n"
                 + "   ① BỎ TICK «DRY-RUN»  ② Trần job/lượt = 1  ③ bấm START\n"
                 + "   (mỗi clip trừ credit — xem số ở dòng 💰 phía trên)"
                 : "\n✅ XONG — đã GỬI cả danh sách. Vào tab Flow chờ render rồi tải clip về.")
          : "\n⏹ Dừng."));
  running = false;
};

// ── mục 2b: thêm job không cần viết JSON ─────────────────────────────────────
const TAIL_KEEP = "Keep the framing, composition, characters, clothing, props and colours of the "
  + "given image exactly as they are; the camera stays locked off and does not move, no zoom, no pan, "
  + "no cut to another shot. Only what is described above moves, once, slowly, and it holds still for "
  + "the rest of the shot. Any printing on paper or screens stays exactly as in the image; no new text "
  + "appears, no captions, no watermark, no logo.";

$("qTail").onclick = () => {
  const t = $("qPrompt").value.trim().replace(/\.$/, "");
  if (!t) return say("Gõ prompt trước đã.");
  if (t.includes("Keep the framing")) return say("Đuôi đã có rồi.");
  $("qPrompt").value = t + ". " + TAIL_KEEP;
};

$("qAdd").onclick = () => {
  const asset = $("qAsset").value.trim();
  const prompt = $("qPrompt").value.trim();
  if (!prompt) return say("🔴 Thiếu prompt.");
  if (!asset) return say("🔴 Thiếu tên asset. Bấm 📋 LIỆT KÊ ASSET để lấy tên đúng — "
                       + "đoán tên thì search ra 0 kết quả và job sẽ dừng.");
  const n = parseJobs($("prompts").value).length + 1;
  const line = JSON.stringify({ id: "j" + String(n).padStart(2, "0"), mode: "frames", asset, prompt });
  const cur = $("prompts").value.replace(/\s*$/, "");
  $("prompts").value = (cur ? cur + LF : "") + line + LF;
  chrome.storage.local.set({ prompts: $("prompts").value });
  $("qPrompt").value = "";
  say(`✅ Đã thêm job j${String(n).padStart(2, "0")} — tổng `
    + `${parseJobs($("prompts").value).length} job.${LF}asset: ${JSON.stringify(asset)}`);
};

$("pause").onclick = () => { running = false; add("Đang dừng sau job hiện tại…"); };
$("reset").onclick = () => { chrome.storage.local.remove(["idx"]); $("startidx").value = 1;
                             say("Đã reset tiến độ về dòng 1. (Sổ đã-gửi KHÔNG bị xoá.)"); };
$("clearledger").onclick = async () => {
  const n = await ledgerClear();
  say(`🗑 Đã xoá sổ đã-gửi (${n} job). Những job đó CÓ THỂ bị gen lại — 100 credits/clip.`);
};
$("loadfile").onchange = async e => {
  const f = e.target.files[0]; if (!f) return;
  $("prompts").value = await f.text();
  say(`Đã nạp ${f.name} — ${parseJobs($("prompts").value).length} job.`);
};
chrome.storage.local.get(["prompts", "idx", "delay", "runmode"]).then(s => {
  setMode(s.runmode === "v1" ? "v1" : "v2", false);   // khôi phục tab đã chọn lần trước
  if (s.prompts) $("prompts").value = s.prompts;
  if (s.delay) $("delay").value = s.delay;
  // ⚡ KHONG khoi phuc startidx nua: chay da luong thi moi panel co khoang rieng,
  //    do lai mot con so `idx` chung se dat sai khoang cho luong khac.
  listTabs();   // quét lại SAU khi khôi phục state (lần gọi ở trên chạy trước khi DOM sẵn state)
});
