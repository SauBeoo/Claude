/* YT Dashboard — frontend thuần, không build step */
let CURRENT = null; // {channel, slug} đang mở panel

const $ = (q) => document.querySelector(q);
const api = async (url, body) => {
  const r = await fetch(url, body ? {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  } : undefined);
  return r.json();
};

function toast(msg, ok = true, sticky = false) {
  const t = $("#toast");
  t.textContent = msg + (sticky ? "\n(bấm vào đây để đóng)" : "");
  t.className = ok ? "" : "err";
  t.onclick = () => t.classList.add("hidden");
  clearTimeout(t._h);
  if (!sticky) t._h = setTimeout(() => t.classList.add("hidden"), 6000);
}

function badgeClass(stage) {
  if (stage.startsWith("GÓI SẴN")) return "b-goi";
  if (stage.startsWith("RENDER ✓")) return "b-render";
  if (stage.startsWith("RENDER…")) return "b-do";
  if (stage.startsWith("ĐÃ ĐĂNG")) return "b-dadang";
  return "b-script";
}

// Màu nhận diện từng kênh (chấm tròn trong lịch để quét nhanh)
const CH_COLORS = {
  chouhen: "#b07cf7", shokutaku: "#2ecc71", health: "#4f8cff",
  "co-dai": "#e67e22", "kr-romfan": "#e74c5b", nenkin: "#1abc9c", stickman: "#8b96ad",
  "suimin-rekishi": "#9b7cf7", akiya: "#39c07a", chimei: "#e69138",
  yoyang: "#e85d8a", kaigo: "#5ac8d8",
};
const chColor = (k) => CH_COLORS[k] || "#8b96ad";

function videoActions(ch, v) {
  const b = [];
  if (v.stage.startsWith("GÓI SẴN")) {
    b.push(`<button onclick="openPanel('${ch}','${v.slug}')">📋 Upload</button>`);
    b.push(`<button onclick="openFolder('${ch}','${v.slug}','pack')">📂</button>`);
    b.push(`<button class="danger" onclick="markDone('${ch}','${v.slug}')">✓ Đã đăng</button>`);
    b.push(`<button onclick="pack('${ch}','${v.slug}')" title="đóng gói lại">📦</button>`);
  } else if (v.stage.startsWith("RENDER ✓")) {
    b.push(`<button onclick="pack('${ch}','${v.slug}')">📦 Đóng gói</button>`);
  } else if (v.stage.startsWith("ĐÃ ĐĂNG")) {
    b.push(`<button class="danger" onclick="markDone('${ch}','${v.slug}')">✓ Chuyển kho</button>`);
  }
  return b.join("");
}

async function setActive(channel, on) {
  await api("/api/channel_active", { channel, active: on });
  toast(on ? `▶ Đã bật lại kênh ${channel}` : `💤 Đã tắt kênh ${channel} — ẩn khỏi danh sách + lịch đăng`);
  loadStatus();
}

async function loadStatus() {
  const data = await api("/api/status");
  const active = data.filter((c) => c.active);
  const off = data.filter((c) => !c.active);
  const _chBox = $("#channels");  // tab Tổng quan đã bỏ — chỉ render nếu còn element
  if (_chBox) _chBox.innerHTML = active.map((c) => `
    <div class="channel">
      <div class="ch-head">
        <b>${c.name}</b>
        <span class="dim">[${c.key}] · đã đăng: ${c.uploaded}</span>
        ${c.has_token ? '<span class="token">● API</span>' : ""}
        <button class="ch-off-btn" title="Tắt kênh (ngưng hoạt động): ẩn khỏi danh sách, lịch đăng, job — data giữ nguyên, bật lại lúc nào cũng được"
          onclick="setActive('${c.key}', false)">💤</button>
      </div>
      ${c.rows.map((v) => `
        <div class="video">
          <span class="slug">${v.slug}</span>
          <span class="badge ${badgeClass(v.stage)}">${v.stage}</span>
          <span class="actions">${videoActions(c.key, v)}</span>
        </div>`).join("") || '<div class="video dim">kho trống</div>'}
      <div class="suggest">
        ${c.slots.length ? "Slot: " + c.slots.join(" · ") : ""}
        ${c.suggest.length
          ? "<br>Đề xuất: " + c.suggest.map((s) => `${s.slot} ← <b>${s.slug}</b>`).join(" · ")
          : (c.slots.length ? '<br><span class="warn">⚠️ Slot sắp tới nhưng KHÔNG có video sẵn</span>' : "")}
      </div>
    </div>`).join("") +
    (off.length ? `
    <div class="channel ch-sleeping">
      <div class="ch-head"><b>💤 Kênh đang tắt</b>
        <span class="dim">không hiện trong lịch đăng / analytics / job — bấm ▶ để bật lại</span>
      </div>
      ${off.map((c) => `
        <div class="video">
          <span class="slug dim">${c.name} [${c.key}]</span>
          <span class="actions"><button onclick="setActive('${c.key}', true)">▶ Bật lại</button></span>
        </div>`).join("")}
    </div>` : "");

  const sel = $("#ana-channel");
  const keep = sel.value;
  sel.innerHTML = active.map((c) =>
    `<option value="${c.key}" ${c.has_token ? "" : "disabled"}>${c.name}${c.has_token ? "" : " (chưa token)"}</option>`
  ).join("");
  if ([...sel.options].some((o) => o.value === keep)) sel.value = keep;
  const jsel = $("#job-channel");
  if (jsel) {
    const jkeep = jsel.value;
    jsel.innerHTML = active.map((c) => `<option value="${c.key}">${c.name}</option>`).join("");
    if ([...jsel.options].some((o) => o.value === jkeep)) jsel.value = jkeep;
  }
  const wsel = $("#wm-channel");
  if (wsel) {
    const wkeep = wsel.value;
    wsel.innerHTML = active.map((c) => `<option value="${c.key}">${c.name}</option>`).join("");
    if ([...wsel.options].some((o) => o.value === wkeep)) wsel.value = wkeep;
  }
}

async function pack(channel, slug, slot) {
  toast(`📦 Đang đóng gói ${slug}…`);
  const r = await api("/api/pack", { channel, slug, slot: slot || null });
  toast(r.log.split("\n").slice(0, 8).join("\n"), r.ok);
  loadStatus();
}

async function markDone(channel, slug) {
  if (!confirm(`Xác nhận: ${slug} ĐÃ upload lên kênh?\n→ Ghi sổ + chuyển kho + AI cắt clip TikTok + dọn mp4.\nChạy nền ~2-5 phút — log hiện ở góc màn hình + tab 🏭 Sản xuất.`)) return;
  const r = await api("/api/done", { channel, slug });
  if (r.error) { toast(r.error, false, true); return; }
  $("#panel").classList.add("hidden");
  loadStatus();
  const t0 = Date.now();
  toast(`⏳ ${slug}: job ${r.id} bắt đầu chạy nền…`, true, true);
  const poll = setInterval(async () => {
    let s;
    try {
      s = await (await fetch("/api/job_log?id=" + r.id)).json();
    } catch (e) { return; } // mạng/server chớp — giữ poll
    const secs = Math.round((Date.now() - t0) / 1000);
    const tail = (s.log || "").split("\n").filter(Boolean);
    if (s.status === "running") {
      toast(`⏳ ${slug} — ${Math.floor(secs / 60)}m${String(secs % 60).padStart(2, "0")}s\n` +
        (tail.slice(-4).join("\n") || "(đang khởi động…)"), true, true);
    } else {
      clearInterval(poll);
      toast(`${s.status === "done" ? "✅ XONG" : "❌ " + (s.status || "LỖI").toUpperCase()} — ${slug} (${Math.floor(secs / 60)}m${String(secs % 60).padStart(2, "0")}s)\n` +
        tail.slice(-8).join("\n"), s.status === "done", true);
      loadStatus();
    }
  }, 3000);
}

async function openFolder(channel, slug, what) {
  const r = await api("/api/open", { channel, slug, what });
  toast(r.log, r.ok);
}

function noteEl(text, warn) {
  const el = document.createElement("div");
  el.className = "field f-note" + (warn ? " f-warn" : "");
  el.textContent = text;
  return el;
}

function fieldEl(label, value, oneline = false) {
  if (!value) return null;
  const wrap = document.createElement("div");
  wrap.className = "field";
  const head = document.createElement("div");
  head.className = "f-head";
  const lab = document.createElement("label");
  lab.textContent = label;
  const btn = document.createElement("button");
  btn.className = "copy";
  btn.textContent = "Copy";
  btn.onclick = async () => {
    await navigator.clipboard.writeText(value);
    btn.textContent = "✓ Đã copy";
    setTimeout(() => (btn.textContent = "Copy"), 1500);
  };
  const val = document.createElement("div");
  val.className = "val" + (oneline ? " oneline" : "");
  val.textContent = value;
  head.append(lab, btn);
  wrap.append(head, val);
  return wrap;
}

async function openPanel(channel, slug, kho = false) {
  const q = `channel=${channel}&slug=${encodeURIComponent(slug)}${kho ? "&kho=1" : ""}`;
  const r = await fetch(`/api/metadata?${q}`);
  if (!r.ok) { toast((await r.json()).error, false); return; }
  const m = await r.json();
  CURRENT = { channel, slug, kho };
  $("#panel-title").textContent = `${kho ? "🗄️" : "📋"} ${slug} [${channel}]${kho ? " — trong kho" : ""}`;
  const sc = $("#panel-sched");
  sc.textContent = m.schedule ? "⏰ " + m.schedule : "";
  sc.classList.toggle("sched-past", !!m.schedule_past);
  const warns = m.warnings.slice();
  if (m.schedule_past) {
    warns.unshift("⏰ GIỜ HẸN ĐÃ QUA (tính lúc đóng gói) — bấm 📦 Gói lại để lấy giờ hẹn mới, hoặc 📦⏰ chọn slot trên tab Lịch đăng");
  }
  const w = $("#panel-warn");
  if (warns.length) { w.textContent = warns.join("\n"); w.classList.remove("hidden"); }
  else w.classList.add("hidden");
  const box = $("#panel-fields");
  box.innerHTML = "";
  [fieldEl("① File video (kéo thả)", m.file, true),
   fieldEl("② Title", m.title, true),
   fieldEl("③ Description (概要欄)", m.description),
   fieldEl("④ Tags", m.tags),
  ].forEach((el) => el && box.append(el));
  // ②b bộ title A/B — đổi TUẦN TỰ (YouTube không A/B được title)
  if (m.ab_titles && m.ab_titles.length > 1) {
    const tb = noteEl(`②b ${m.ab_titles.length} TITLE A/B — đổi TUẦN TỰ, mỗi bản ≥7 ngày:`, false);
    m.ab_titles.forEach((it, i) => {
      const row = document.createElement("div");
      row.className = "ab-title-row";
      const btn = document.createElement("button");
      btn.className = "mini";
      btn.textContent = "copy";
      btn.onclick = () => navigator.clipboard.writeText(it.title);
      const lab = document.createElement("code");
      lab.textContent = `[${it.tag}] ${it.title}` + (i === 0 ? "   ← DÙNG KHI ĐĂNG" : "");
      row.append(btn, lab);
      tb.append(row);
    });
    box.append(tb);
  }
  // ⑤ phụ đề srt — bắt buộc upload thủ công (rule youtube-upload-seo.md 1.2)
  box.append(noteEl(m.srt
    ? "⑤ Phụ đề: upload subs.srt trong folder (Subtitles → Add → Upload file) — KHÔNG dùng auto-caption"
    : "⑤ ⚠️ THIẾU subs.srt trong gói — kiểm tra render/đóng gói lại!", !m.srt));
  // ⑥ thumbnail preview
  if (m.thumb) {
    const list = (m.thumbs && m.thumbs.length) ? m.thumbs : ["thumbnail.png"];
    const isAB = list.length > 1;
    const t = noteEl(isAB
      ? `⑥ Thumbnail — BỘ A/B ${list.length} bản (Studio → Thumbnail → "Test & compare", nạp cả ${list.length})`
      : "⑥ Thumbnail (thumbnail.png trong folder):", false);
    const row = document.createElement("div");
    if (isAB) row.className = "thumb-ab";
    list.forEach((name, i) => {
      const cell = document.createElement("div");
      cell.className = "thumb-ab-cell";
      const img = document.createElement("img");
      img.src = `/api/thumb?${q}&v=${encodeURIComponent(name)}&t=${Date.now()}`;
      img.className = "thumb-prev";
      img.title = name;
      cell.append(img);
      if (isAB) {
        const cap = document.createElement("div");
        cap.className = "thumb-ab-cap";
        cap.textContent = `T${i + 1} · ${name}`;
        cell.append(cap);
      }
      row.append(cell);
    });
    t.append(row);
    box.append(t);
    if (isAB) box.append(noteEl(
      "⚠️ Test & compare chỉ A/B được THUMBNAIL. GIỮ NGUYÊN TITLE suốt thời gian test (≥7 ngày) — "
      + "đổi title giữa lúc test là lẫn 2 biến, kết quả thumbnail thành vô nghĩa.", true));
  } else {
    box.append(noteEl("⑥ ⚠️ THIẾU thumbnail.png trong gói — làm thumbnail rồi đóng gói lại (--thumb)!", true));
  }
  const pin = fieldEl("⑨ Pinned comment (sau khi công khai)", m.pinned);
  if (pin) box.append(pin);
  // Soi thiếu gì → hiện nút AI bổ sung
  const missing = [];
  if (!m.file) missing.push("tên file video SEO");
  if (!m.title) missing.push("title");
  if (!m.description) missing.push("description 概要欄");
  if (!m.tags) missing.push("tags");
  if (!m.pinned) missing.push("pinned comment (nếu format kênh có)");
  if (!m.thumb) missing.push("thumbnail.png");
  if (!m.srt) missing.push("subs.srt (cần job Render — AI chỉ báo lại)");
  const fixBtn = $("#panel-ai-fix");
  CURRENT.missing = missing;
  if (missing.length) {
    fixBtn.textContent = `🤖 AI bổ sung thiếu (${missing.length})`;
    fixBtn.title = "Thiếu: " + missing.join(", ") +
      "\n→ phóng 1 Claude agent trong repo kênh: viết phần thiếu vào script theo format chuẩn + gói lại";
    fixBtn.classList.remove("hidden");
  } else {
    fixBtn.classList.add("hidden");
  }
  $("#panel-checklist").innerHTML = "<label style='color:var(--fg)'>Checklist:</label>" +
    m.checklist.map((c) => `<label><input type="checkbox"> <span>${c}</span></label>`).join("");
  // Kho = chỉ tra cứu/copy: ẩn nút workflow (đăng/gói lại/mở folder gói/bổ sung), giữ ▶ Studio để update
  const wf = !kho;
  $("#panel-done").style.display = wf ? "" : "none";
  $("#panel-repack").style.display = wf ? "" : "none";
  const packBtn = document.querySelector('#panel-actions [data-open="pack"]');
  if (packBtn) packBtn.style.display = wf ? "" : "none";
  $("#panel-checklist").style.display = kho ? "none" : "";
  if (kho) $("#panel-ai-fix").classList.add("hidden");
  $("#panel").classList.remove("hidden");
}

/* ---- Tab Kho (07_UPLOADED) — lưới card có thumbnail ---- */
const esc = (s) => (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

let KHO_DATA = null;      // cache toàn bộ kho (JSON nhẹ, không kèm ảnh)
let khoShown = {};        // key kênh -> số card đang hiện (phân trang)
const KHO_PAGE = 12;      // số card mỗi lần hiện / "Xem thêm"

async function loadKho(force) {
  if (!KHO_DATA || force) {
    KHO_DATA = await (await fetch("/api/kho")).json();
    khoShown = {};
    const sel = $("#kho-ch"), keep = sel.value;
    sel.innerHTML = '<option value="">Tất cả kênh</option>' +
      KHO_DATA.filter((c) => c.items.length)
        .map((c) => `<option value="${c.key}">${esc(c.name)} (${c.items.length})</option>`).join("");
    if ([...sel.options].some((o) => o.value === keep)) sel.value = keep;
  }
  renderKho();
}

function khoCard(key, v) {
  const thumb = v.has_thumb
    ? `<img class="kho-thumb" loading="lazy" src="/api/thumb?channel=${key}&slug=${encodeURIComponent(v.slug)}&kho=1">`
    : `<div class="kho-thumb ph">🖼️</div>`;
  const chips = [
    v.uploaded ? `<span class="kho-chip kho-date">📅 ${esc(v.uploaded)}</span>` : "",
    v.has_srt ? '<span class="kho-chip">💬 subs</span>' : "",
    v.scripts.length ? `<span class="kho-chip">📄 ${v.scripts.length}</span>` : "",
  ].join("");
  return `
    <div class="kho-card">
      ${thumb}
      <div class="kho-body">
        <div class="kho-title" title="${esc(v.title || v.slug)}">${esc(v.title || v.slug)}</div>
        <div class="kho-slug">${esc(v.slug)}</div>
        <div class="kho-chips">${chips}</div>
        <div class="kho-actions">
          <button onclick="openPanel('${key}','${v.slug}',true)">📋 Xem/Copy</button>
          <button onclick="openProfile('${key}')" title="Mở YouTube Studio đúng profile kênh để sửa video này">▶ Studio</button>
        </div>
      </div>
    </div>`;
}

function khoMore(key) { khoShown[key] = (khoShown[key] || KHO_PAGE) + KHO_PAGE; renderKho(); }

function renderKho() {
  const box = $("#kho-list");
  if (!KHO_DATA) { box.textContent = "Đang tải…"; return; }
  const q = ($("#kho-search").value || "").trim().toLowerCase();
  const chFilter = $("#kho-ch").value;
  let sections = KHO_DATA.filter((c) => c.items.length);
  if (chFilter) sections = sections.filter((c) => c.key === chFilter);
  sections = sections.map((c) => ({
    ...c,
    _items: c.items.filter((v) => !q ||
      (v.title || "").toLowerCase().includes(q) || v.slug.toLowerCase().includes(q)),
  })).filter((c) => c._items.length);
  if (!sections.length) {
    box.innerHTML = `<div class="suggest">${q || chFilter ? "Không có video nào khớp bộ lọc." : "Kho chưa có video nào có metadata."}</div>`;
    return;
  }
  box.innerHTML = sections.map((c) => {
    const limit = q ? c._items.length : (khoShown[c.key] || KHO_PAGE); // đang tìm → hiện hết kết quả
    const vis = c._items.slice(0, limit);
    const more = c._items.length - vis.length;
    return `
    <div class="kho-chsec">
      <div class="ch-head"><b>${esc(c.name)}</b>
        <span class="dim">[${c.key}] · ${c._items.length} video${q ? " khớp" : ""}${more > 0 ? ` · hiện ${vis.length}` : ""}</span></div>
      <div class="kho-grid">${vis.map((v) => khoCard(c.key, v)).join("")}</div>
      ${more > 0 ? `<div style="margin-top:10px"><button onclick="khoMore('${c.key}')">Xem thêm ${Math.min(more, KHO_PAGE)} / còn ${more} ▾</button></div>` : ""}
    </div>`;
  }).join("");
}

/* ---- Tab Chuẩn bị đăng: chọn project → mở script + slide chưa upload ---- */
let PEND_DATA = null;
let PEND_ACTIVE = null; // key project đang chọn

async function loadPending(force) {
  if (!PEND_DATA || force) {
    PEND_DATA = await (await fetch("/api/pending")).json();
  }
  // giữ project đang chọn nếu còn hợp lệ, không thì chọn project đầu tiên CÓ bài
  const keys = PEND_DATA.map((c) => c.key);
  if (!PEND_ACTIVE || !keys.includes(PEND_ACTIVE)) {
    PEND_ACTIVE = (PEND_DATA.find((c) => c.count) || PEND_DATA[0] || {}).key || null;
  }
  renderPendTabs();
  renderPending();
}

function renderPendTabs() {
  const box = $("#pend-projtabs");
  if (!PEND_DATA || !PEND_DATA.length) { box.textContent = "chưa có project nào."; return; }
  box.innerHTML = PEND_DATA.map((c) => `
    <button class="proj-tab${c.key === PEND_ACTIVE ? " active" : ""}${c.count ? "" : " empty"}"
            onclick="selectPendProj('${c.key}')" title="${esc(c.name)}">
      <span class="pt-dot" style="background:${chColor(c.key)}"></span>
      ${esc(c.name)} <span class="pt-count">${c.count}</span>
    </button>`).join("");
}

function selectPendProj(key) {
  PEND_ACTIVE = key;
  renderPendTabs();
  renderPending();
}

function pendCard(key, v) {
  const chips = [
    v.has_video ? '<span class="kho-chip">🎬 render</span>' : "",
    v.has_tts ? '<span class="kho-chip">🎞️ TTS</span>' : "",
    v.n_slides ? `<span class="kho-chip">🖼️ ${v.n_slides}</span>` : "",
  ].join("");
  return `
    <div class="kho-card pend-card">
      <div class="kho-body">
        <div class="kho-title" title="${esc(v.title || v.slug)}">${esc(v.title || v.slug)}</div>
        <div class="kho-slug">${esc(v.slug)}</div>
        <div class="kho-chips">${chips || '<span class="dim">chưa có slide/TTS/video</span>'}</div>
        <div class="kho-actions">
          <button onclick="openPending('${key}','${esc(v.slug)}')">📄 Xem kịch bản + ảnh</button>
          <button onclick="openFolder('${key}','${esc(v.slug)}','video')" title="Mở folder video trong Explorer (xem/sửa ảnh nguồn trước khi render)">📂</button>
          <button onclick="openProfile('${key}')" title="Mở Studio đúng profile kênh">▶ Studio</button>
        </div>
      </div>
    </div>`;
}

function renderPending() {
  const box = $("#pend-list");
  if (!PEND_DATA) { box.textContent = "Đang tải…"; return; }
  const c = PEND_DATA.find((x) => x.key === PEND_ACTIVE);
  if (!c) { box.innerHTML = '<div class="suggest">Chọn một project ở trên.</div>'; return; }
  const q = ($("#pend-search").value || "").trim().toLowerCase();
  const items = c.items.filter((v) => !q ||
    (v.title || "").toLowerCase().includes(q) || v.slug.toLowerCase().includes(q));
  if (!items.length) {
    box.innerHTML = `<div class="suggest">${q
      ? "Không có bài nào khớp trong project này."
      : `<b>${esc(c.name)}</b> không có bài nào đang chờ đăng — mọi script đã chuyển kho.`}</div>`;
    return;
  }
  box.innerHTML = `
    <div class="kho-chsec">
      <div class="ch-head"><b>${esc(c.name)}</b>
        <span class="dim">[${c.key}] · ${items.length} bài${q ? " khớp" : ""}</span>
        <button style="margin-left:auto" onclick="openProfile('${c.key}')" title="Mở Studio đúng profile kênh">▶ Studio</button></div>
      <div class="kho-grid">${items.map((v) => pendCard(c.key, v)).join("")}</div>
    </div>`;
}

async function openPending(channel, slug) {
  $("#ppanel").classList.remove("hidden");
  const head = $("#ppanel-title");
  head.innerHTML = `📝 ${esc(slug)} <span class="dim">[${esc(channel)}]</span> `;
  const fbtn = document.createElement("button");
  fbtn.textContent = "📂 Mở folder";
  fbtn.title = "Mở folder video trong Explorer để xem/sửa ảnh nguồn trước render";
  fbtn.style.fontSize = "12px";
  fbtn.onclick = () => openFolder(channel, slug, "video");
  head.append(fbtn);
  $("#ppanel-tabs").innerHTML = "";
  $("#ppanel-body").textContent = "Đang tải…";
  const d = await api(`/api/pending_detail?channel=${channel}&slug=${encodeURIComponent(slug)}`);
  if (d.error) { $("#ppanel-body").textContent = "⚠️ " + d.error; return; }
  const views = [];
  const nImg = (d.preview_imgs || []).length;
  views.push({ name: `🖼️ Duyệt ảnh${nImg ? ` (${nImg})` : ""}`,
               render: () => pendPreviewView(channel, slug, d) });
  views.push({ name: `📜 Kịch bản`, render: () => pendScriptView(d.script_file, d.script) });
  if (d.tts) views.push({ name: `🎞️ TTS`, render: () => pendScriptView(d.tts_file, d.tts) });
  $("#ppanel-tabs").innerHTML = views
    .map((v, i) => `<button class="pp-tab${i === 0 ? " active" : ""}" data-i="${i}">${v.name}</button>`).join("");
  const show = (i) => {
    $("#ppanel-tabs").querySelectorAll(".pp-tab").forEach((b) => b.classList.toggle("active", +b.dataset.i === i));
    $("#ppanel-body").innerHTML = "";
    $("#ppanel-body").append(views[i].render());
  };
  $("#ppanel-tabs").querySelectorAll(".pp-tab").forEach((b) => b.onclick = () => show(+b.dataset.i));
  show(0);
}

function copyBtnFor(getText) {
  const btn = document.createElement("button");
  btn.className = "copy";
  btn.textContent = "Copy";
  btn.onclick = async () => {
    await navigator.clipboard.writeText(getText());
    btn.textContent = "✓ Đã copy";
    setTimeout(() => (btn.textContent = "Copy"), 1500);
  };
  return btn;
}

function pendScriptView(file, text) {
  const wrap = document.createElement("div");
  const head = document.createElement("div");
  head.className = "f-head";
  const lab = document.createElement("label");
  lab.textContent = `${file} · ${text.length.toLocaleString()} ký tự`;
  head.append(lab, copyBtnFor(() => text));
  const pre = document.createElement("pre");
  pre.className = "pend-script";
  pre.textContent = text;
  wrap.append(head, pre);
  return wrap;
}

function pendPreviewView(channel, slug, d) {
  const imgs = d.preview_imgs || [];
  const wrap = document.createElement("div");
  if (!imgs.length) {
    const p = document.createElement("div");
    p.className = "suggest";
    p.innerHTML = `Chưa có ảnh nguồn để duyệt${d.n_spec ? ` (spec có ${d.n_spec} slide)` : ""}. `
      + "Ảnh chỉ có sau khi <b>fetch ảnh</b> (bước trước render). "
      + 'Bấm <b>📂 Mở folder</b> ở trên để kiểm tra, hoặc chạy fetch/render ở tab 🏭 Sản xuất.';
    wrap.append(p);
    return wrap;
  }
  const head = document.createElement("div");
  head.className = "f-head";
  const lab = document.createElement("label");
  lab.textContent = `${imgs.length} ảnh nguồn sẽ ghép vào video — duyệt TRƯỚC render (bấm ảnh xem to; 📂 Mở folder để thay ảnh lệch)`;
  head.append(lab);
  wrap.append(head);
  const grid = document.createElement("div");
  grid.className = "pend-slide-grid";
  imgs.forEach((it, i) => {
    const cell = document.createElement("figure");
    cell.className = "pend-slide-cell";
    const img = document.createElement("img");
    img.loading = "lazy";
    img.src = `/api/pending_img?channel=${channel}&slug=${encodeURIComponent(slug)}&file=${encodeURIComponent(it.file)}`;
    img.onclick = () => window.open(img.src, "_blank");
    const cap = document.createElement("figcaption");
    cap.textContent = `#${i + 1}${it.match ? " · " + it.match : ""}`;
    cap.title = it.q ? "query: " + it.q : "";
    cell.append(img, cap);
    grid.append(cell);
  });
  wrap.append(grid);
  return wrap;
}

/* ---- Tab Lịch đăng ---- */
async function loadSchedule() {
  const box = $("#schedule");
  const r = await (await fetch("/api/schedule")).json();
  const profs = await getProfiles(); // profile Chrome từng kênh — hiện ngay tại slot cho tiện đăng
  const csel = $("#slot-add-channel");
  const ckeep = csel.value;
  csel.innerHTML = Object.entries(r.channels)
    .map(([k, n]) => `<option value="${k}">${n}</option>`).join("");
  if ([...csel.options].some((o) => o.value === ckeep)) csel.value = ckeep;
  if (!$("#slot-add-date").value && r.days.length) $("#slot-add-date").value = r.days[0].date;
  box.innerHTML = "";
  r.days.forEach((d) => {
    const card = document.createElement("div");
    card.className = "day" + (d.today ? " today" : "") + (d.slots.length ? "" : " empty");
    const head = document.createElement("div");
    head.className = "day-head";
    head.innerHTML = `<b>${d.label}</b>` + (d.today ? ' <span class="today-badge">HÔM NAY</span>' : "")
      + (d.slots.length ? `<span class="day-count">${d.slots.length} slot</span>` : "");
    card.append(head);
    if (!d.slots.length) {
      const none = document.createElement("div");
      none.className = "dim slot-none";
      none.textContent = "— không có lịch đăng —";
      card.append(none);
    }
    d.slots.forEach((s) => {
      const row = document.createElement("div");
      row.className = "slot" + (s.past ? " past" : "");
      const time = document.createElement("span");
      time.className = "slot-time";
      time.textContent = s.vn;
      const local = document.createElement("span");
      local.className = "dim slot-local";
      local.textContent = s.local ? `(${s.local})` : "";
      const name = document.createElement("span");
      name.className = "slot-ch";
      name.innerHTML = `<span class="ch-dot" style="background:${chColor(s.key)}"></span>`
        + (s.extra ? "➕ " : "") + esc(s.name);
      if (s.extra) name.title = "Slot thêm tay (không thuộc lịch cố định)";
      // Profile Chrome của kênh + nút mở Studio đúng profile để đăng luôn
      const prof = document.createElement("span");
      prof.className = "dim slot-prof";
      const pf = profs[s.key];
      if (pf) {
        prof.textContent = `🌐 ${pf.profile_dir}`;
        prof.title = `Chrome profile của kênh · ${pf.gmail_live || pf.gmail || "chưa login"}`;
        const go = document.createElement("button");
        go.textContent = "▶ Studio";
        go.title = `Mở YouTube Studio bằng profile 「${pf.profile_dir}」 (${pf.gmail_live || pf.gmail || ""}) để đăng`;
        go.onclick = () => openProfile(s.key);
        prof.append(" ", go);
      } else {
        prof.innerHTML = '<span class="warn" title="Kênh chưa có Chrome profile — thêm ở tab 🌐 Profiles">🌐 chưa có profile</span>';
      }
      // Kênh mới (ngoài CHANNELS) đặt lịch trước — khung dự kiến, chưa có video/queue
      if (s.plan) {
        const pv = document.createElement("span");
        pv.className = "slot-video";
        pv.innerHTML = '<span class="slot-plan" title="Kênh mới đang rebrand — đã đặt lịch trước ở tab Dự án, chưa có video">🆕 dự kiến</span>';
        row.append(time, local, name, prof, pv);
        card.append(row);
        return;
      }
      const vid = document.createElement("span");
      vid.className = "slot-video";
      const pin = s.pinned ? "📌 " : "";
      if (s.video) {
        vid.innerHTML = pin + `← <span class="badge ${badgeClass(s.stage || "")}">${s.video}</span>` +
          (!s.stage ? ' <span class="warn">(không còn trong kho?)</span>'
            : (s.stage.startsWith("RENDER ✓") ? ' <span class="warn">(chưa gói!)</span>' : ""));
      } else {
        vid.innerHTML = s.pinned ? `${pin}<span class="dim">để trống (ghim)</span>`
          : '<span class="warn">⚠️ chưa có video sẵn</span>';
      }
      // Dropdown ghim: đổi video vào slot này / để trống / trả về tự động
      const sel = document.createElement("select");
      sel.className = "slot-sel";
      sel.title = "Đổi video ghép vào slot này (ghim tay — các slot khác tự dồn lại)";
      const opts = [["__auto__", "⚙ tự động"], ["", "∅ để trống"]]
        .concat((r.queues[s.key] || []).map((q) => [q.slug, q.slug]));
      if (s.pinned && s.video && !opts.some(([v]) => v === s.video)) opts.push([s.video, s.video]);
      opts.forEach(([v, t]) => {
        const o = document.createElement("option");
        o.value = v; o.textContent = t;
        sel.append(o);
      });
      sel.value = s.pinned ? (s.video || "") : "__auto__";
      sel.onchange = async () => {
        const body = { date: d.date, channel: s.key, time: s.sort };
        if (sel.value === "__auto__") body.clear = true; else body.slug = sel.value;
        await api("/api/slot_pin", body);
        loadSchedule();
      };
      vid.append(sel);
      // Lấy thông tin upload ngay từ lịch (video đã GÓI SẴN)
      if (s.video && s.stage && s.stage.startsWith("GÓI SẴN")) {
        const info = document.createElement("button");
        info.textContent = "📋";
        info.title = "Mở panel Upload: title/mô tả/tags copy từng ô + checklist + cảnh báo thiếu gì";
        info.onclick = () => openPanel(s.key, s.video);
        vid.append(info);
      }
      // Chốt giờ hẹn thật: gói lại với --slot = slot này (ghi vào METADATA)
      if (s.video) {
        const pk = document.createElement("button");
        pk.textContent = "📦⏰";
        pk.title = `Đóng gói ${s.video} với giờ hẹn = slot này (ghi vào METADATA.txt)`;
        pk.onclick = async () => {
          if (!confirm(`Gói ${s.video} với giờ hẹn ${s.vn} VN ${s.local ? "(" + s.local + ")" : ""} ngày ${d.label}?`)) return;
          await pack(s.key, s.video, s.slot_arg);
          loadSchedule();
        };
        vid.append(pk);
      }
      if (s.extra) {
        const del = document.createElement("button");
        del.className = "danger";
        del.textContent = "✕";
        del.title = "Xóa slot thêm tay này (ghim gắn vào cũng bị dọn)";
        del.onclick = async () => {
          await api("/api/slot_del", { channel: s.key, date: d.date, time: s.sort });
          loadSchedule();
        };
        vid.append(del);
      }
      row.append(time, local, name, prof, vid);
      card.append(row);
    });
    box.append(card);
  });
  const note = document.createElement("div");
  note.className = "dim";
  note.style.marginTop = "10px";
  note.textContent = `Cập nhật lúc ${r.now} (giờ VN). Video ghép theo queue: GÓI SẴN trước, RENDER ✓ sau.`;
  box.append(note);
}

/* ---- Analytics tab ---- */
async function anaRun(kind) {
  const channel = $("#ana-channel").value;
  if (!channel) return;
  $("#ana-out").textContent = "Đang chạy…";
  if (kind === "load") {
    const r = await (await fetch(`/api/analytics?channel=${channel}`)).json();
    $("#ana-out").textContent = r.log || "(không có output)";
    loadChannelVideos(channel);
    return;
  }
  const r = await api("/api/sync", { channel, apply: kind === "sync" });
  $("#ana-out").textContent = r.log || "(không có output)";
}

function videoRow(channel, v, fresh) {
  const row = document.createElement("div");
  row.className = "video";
  const meta = document.createElement("span");
  meta.className = "slug";
  meta.textContent = `${fresh ? "🔥 " : ""}${v.published || "hẹn giờ"} · ${v.views} views`;
  const title = document.createElement("span");
  title.style.flex = "1";
  title.textContent = v.title.slice(0, 62);
  const act = document.createElement("span");
  act.className = "actions";
  const btn = document.createElement("button");
  btn.textContent = "🔬 Số liệu";
  btn.onclick = async () => {
    btn.disabled = true;
    $("#ana-out").textContent = `🔬 Đang mổ「${v.title.slice(0, 30)}…」 (10–20 giây)…`;
    const r = await (await fetch(`/api/video_report?channel=${channel}&video=${v.id}`)).json();
    $("#ana-out").textContent = r.log || "(không có output)";
    btn.disabled = false;
    $("#ana-out").scrollIntoView({ behavior: "smooth" });
  };
  const aiBtn = document.createElement("button");
  aiBtn.textContent = "🤖 AI";
  aiBtn.title = "AI đọc số liệu video này và trả về chẩn đoán + việc cần làm";
  aiBtn.onclick = () => aiAnalyze(channel, v.id, v.title, aiBtn);
  act.append(btn, aiBtn);
  row.append(meta, title, act);
  return row;
}

async function loadChannelVideos(channel) {
  const box = $("#ana-videos");
  const freshBox = $("#ana-fresh");
  freshBox.innerHTML = "";
  box.textContent = "Đang tải danh sách video trên kênh…";
  const resp = await fetch(`/api/channel_videos?channel=${channel}`);
  if (!resp.ok) { box.textContent = ""; return; }
  const vids = (await resp.json()).filter((v) => v.privacy === "public" || v.publishAt);
  box.innerHTML = "";
  // Watchlist <72h — bước ⑤ vòng đời (upload-schedule.md 1.5): theo dõi 72h đầu sau đăng
  const isFresh = (v) => v.published &&
    (Date.now() - new Date(v.published).getTime()) < 72 * 3600 * 1000;
  const fresh = vids.filter(isFresh);
  if (fresh.length) {
    const head = document.createElement("div");
    head.className = "ch-head";
    head.innerHTML = "<b>🔥 Video mới (&lt;72h) — theo dõi cú đẩy đầu</b>";
    freshBox.append(head);
    fresh.forEach((v) => freshBox.append(videoRow(channel, v, true)));
  }
  vids.filter((v) => !isFresh(v)).forEach((v) => box.append(videoRow(channel, v, false)));
}

async function aiAnalyze(channel, videoId, title, btn) {
  if (btn) btn.disabled = true;
  $("#ana-out").textContent = videoId
    ? `🤖 AI đang phân tích「${(title || videoId).slice(0, 30)}…」— kéo số liệu + suy nghĩ, ~30–90 giây, chờ chút…`
    : `🤖 AI đang phân tích toàn kênh — kéo số liệu + suy nghĩ, ~30–90 giây, chờ chút…`;
  try {
    const r = await api("/api/ai_analyze", { channel, video: videoId || null });
    $("#ana-out").textContent = r.log || "(không có output)";
  } catch (e) {
    $("#ana-out").textContent = "Lỗi gọi AI: " + e;
  }
  if (btn) btn.disabled = false;
  $("#ana-out").scrollIntoView({ behavior: "smooth" });
}

/* ---- model AI cho từng tính năng ---- */
async function loadAiModels() {
  const d = await api("/api/ai_models");
  const label = (m) => (m === "" ? "mặc định" : m);
  $("#ai-models").innerHTML = d.purposes.map((p) => `
    <label style="display:inline-flex;align-items:center;gap:7px;font-size:13.5px">
      ${p.label}
      <select data-purpose="${p.key}">
        ${d.options.map((o) => `<option value="${o}" ${o === p.model ? "selected" : ""}>${label(o)}</option>`).join("")}
      </select>
    </label>`).join("");
  document.querySelectorAll("#ai-models select").forEach((s) => s.onchange = async () => {
    const r = await api("/api/ai_models", { purpose: s.dataset.purpose, model: s.value });
    toast(r.ok ? `🧠 「${s.closest("label").textContent.trim().split("\n")[0]}」 → ${label(s.value)}` : (r.error || "Lỗi lưu model"), !!r.ok);
  });
}

/* ---- browser profiles: mỗi kênh 1 Chrome profile riêng ---- */
let PROFILES_CACHE = null; // key -> {profile_dir, gmail, gmail_live, ...}

async function getProfiles() {
  if (!PROFILES_CACHE) {
    const d = await api("/api/profiles");
    PROFILES_CACHE = {};
    (d.rows || []).forEach((p) => (PROFILES_CACHE[p.key] = p));
  }
  return PROFILES_CACHE;
}

async function loadProfiles() {
  const d = await api("/api/profiles");
  PROFILES_CACHE = {};
  (d.rows || []).forEach((p) => (PROFILES_CACHE[p.key] = p));
  $("#prof-list").innerHTML = (d.rows || []).map((p) => {
    const mismatch = p.gmail && p.gmail_live && p.gmail !== p.gmail_live;
    const k = esc(p.key);
    return `
    <div class="video" id="prof-row-${k}">
      <span class="slug"><b>${esc(p.channel_name)}</b> <span class="dim">[${k}]</span></span>
      <span class="dim">${esc(p.profile_dir)}${p.exists ? "" : " ❌ (chưa tồn tại)"}</span>
      <span class="${mismatch ? "warn" : "dim"}">${esc(p.gmail_live || p.gmail || "(chưa login)")}${mismatch ? ` ⚠️ mapping ghi ${esc(p.gmail)}` : ""}</span>
      <span class="actions">
        <button onclick="openProfile('${k}')">▶ Mở Studio</button>
        <button onclick="openProfile('${k}','https://www.youtube.com')" title="mở YouTube thường">YT</button>
        <button onclick="editProfile('${k}')" title="Sửa tên kênh + gmail">✏️</button>
        <button class="danger" onclick="delProfile('${k}')" title="Gỡ khỏi mapping (giữ folder + shortcut)">🗑️</button>
      </span>
      <div class="prof-edit hidden" id="prof-edit-${k}">
        <input class="pe-name" type="text" placeholder="tên kênh" value="${esc(p.channel_name)}" style="flex:1;min-width:200px">
        <input class="pe-gmail" type="text" placeholder="gmail kênh" value="${esc(p.gmail)}" style="width:240px">
        <button onclick="saveProfile('${k}')">💾 Lưu</button>
        <button onclick="$('#prof-edit-${k}').classList.add('hidden')">Hủy</button>
        <span class="dim">profile_dir 「${esc(p.profile_dir)}」 giữ nguyên</span>
      </div>
    </div>`;
  }).join("") || '<div class="video dim">chưa có mapping nào — thêm ở form dưới</div>';
  if (!d.chrome) toast("⚠️ Không tìm thấy chrome.exe — sửa chrome_exe trong browser_profiles.json", false);
}

function editProfile(key) {
  const box = $("#prof-edit-" + key);
  if (box) box.classList.toggle("hidden");
}

async function saveProfile(key) {
  const box = $("#prof-edit-" + key);
  const r = await api("/api/profile_edit", {
    key,
    channel_name: box.querySelector(".pe-name").value.trim(),
    gmail: box.querySelector(".pe-gmail").value.trim(),
  });
  toast(r.log, r.ok);
  if (r.ok) { PROFILES_CACHE = null; loadProfiles(); }
}

async function delProfile(key) {
  if (!confirm(`Gỡ profile 「${key}」 khỏi mapping?\nFolder Chrome + shortcut desktop VẪN GIỮ — chỉ xóa entry trong browser_profiles.json.`)) return;
  const r = await api("/api/profile_del", { key });
  toast(r.log, r.ok);
  if (r.ok) { PROFILES_CACHE = null; loadProfiles(); }
}

async function openProfile(key, url) {
  const r = await api("/api/profile_open", { key, url: url || null });
  toast(r.log, r.ok);
}

/* ---- Tab Dự án (quản lý danh mục kênh, giai đoạn pivot) ---- */
const PROJ_STATUS = {
  active:     { dot: "🟢", label: "Hoạt động",    cls: "st-active" },
  rebranding: { dot: "🟡", label: "Đang rebrand",  cls: "st-rebrand" },
  planning:   { dot: "⚪", label: "Lên kế hoạch",  cls: "st-plan" },
  paused:     { dot: "⏸",  label: "Tạm dừng",      cls: "st-paused" },
};

async function loadProjects() {
  const box = $("#proj-list");
  let data;
  try { data = await (await fetch("/api/projects")).json(); }
  catch (e) { box.textContent = "Lỗi tải: " + e; return; }
  const n = { active: 0, rebranding: 0, planning: 0, paused: 0 };
  data.forEach((p) => (n[p.status] = (n[p.status] || 0) + 1));
  $("#proj-summary").textContent =
    `🟢 ${n.active} hoạt động · 🟡 ${n.rebranding} rebrand · ⚪ ${n.planning} kế hoạch · ⏸ ${n.paused} tạm dừng`;
  box.innerHTML = "";
  box.className = "proj-grid";
  data.forEach((p) => box.append(projCard(p)));
}

function sigChips(s, p) {
  const chips = [];
  // Profile Chrome (dò tự động)
  if (p.profile_dir) {
    const ok = s.profile_exists;
    chips.push(`<span class="chip ${ok ? "c-ok" : "c-bad"}" title="${ok ? "Profile Chrome tồn tại" : "Profile CHƯA tồn tại trong Chrome"}">🌐 ${esc(p.profile_dir)}${ok ? "" : " ✗"}</span>`);
    if (p.gmail_mismatch) chips.push(`<span class="chip c-bad" title="Gmail login thật (${esc(s.gmail_live)}) khác mapping (${esc(p.gmail)})">⚠️ gmail lệch</span>`);
  } else {
    chips.push(`<span class="chip c-dim">🌐 chưa gán profile</span>`);
  }
  chips.push(s.has_token
    ? `<span class="chip c-ok" title="Có token API — upload full-auto được">🔑 API</span>`
    : `<span class="chip c-dim" title="Chưa có token API">🔑 chưa</span>`);
  chips.push(`<span class="chip" title="Số script trong 0N_SCRIPTS">📄 ${s.scripts} script</span>`);
  chips.push(`<span class="chip" title="Số video trong 0N_VIDEO">🎬 ${s.videos} video</span>`);
  chips.push(`<span class="chip ${s.uploaded ? "c-ok" : ""}" title="Số video đã chuyển kho 07_UPLOADED">📤 ${s.uploaded} đã đăng</span>`);
  return chips.join("");
}

const WD_VN = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];  // index = weekday 0=Mon..6=Sun
const p2 = (n) => String(n).padStart(2, "0");
const hh = (h, m = 0) => p2(h) + ":" + p2(m);

function fmtSlots(sched) {
  if (!sched.slots.length) return "chưa đặt lịch";
  const hour = sched.slots[0][1], min = sched.slots[0][2] || 0;  // slot = [wd, giờ] hoặc [wd, giờ, phút]
  const wds = sched.slots.map((s) => WD_VN[s[0]]).join("·");
  const vnh = (((hour - (sched.tz - 7)) % 24) + 24) % 24;
  return `${wds} · ${hh(hour, min)} ${sched.tz_name}` + (sched.tz !== 7 ? ` (${hh(vnh, min)} VN)` : "");
}

function projSchedule(p) {
  const box = document.createElement("div");
  box.className = "proj-sched";
  const sched = p.sched;
  const srcLabel = { rule: "theo rule", override: "sửa tay (đè rule)", project: "đặt tay" }[sched.source] || "";
  const cur = document.createElement("div");
  cur.className = "proj-sched-cur";
  cur.innerHTML = `📅 <b>${fmtSlots(sched)}</b>` + (srcLabel ? ` <span class="proj-sched-src">${srcLabel}</span>` : "");
  box.append(cur);

  const ed = document.createElement("div");
  ed.className = "proj-sched-ed";
  const picked = new Set(sched.slots.map((s) => s[0]));
  const days = document.createElement("div");
  days.className = "wd-row";
  WD_VN.forEach((lb, wd) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "wd-btn" + (picked.has(wd) ? " on" : "");
    b.textContent = lb;
    b.onclick = () => { picked.has(wd) ? picked.delete(wd) : picked.add(wd); b.classList.toggle("on"); };
    days.append(b);
  });
  const time = document.createElement("input");
  time.type = "time";
  time.className = "wd-time";
  time.value = sched.slots.length ? hh(sched.slots[0][1], sched.slots[0][2] || 0) : "09:00";
  const save = document.createElement("button");
  save.textContent = "💾 Lưu";
  save.onclick = async () => {
    const wds = [...picked].sort((a, b) => a - b);
    if (!wds.length) { toast("Chọn ít nhất 1 thứ trong tuần", false); return; }
    const [th, tm] = time.value.split(":");
    const r = await api("/api/project_schedule", {
      key: p.key, weekdays: wds,
      hour: parseInt(th, 10), minute: parseInt(tm || "0", 10),  // hỗ trợ giờ lẻ phút (17:30)
    });
    if (r.ok) { toast(`📅 Đã lưu lịch 「${p.name_new}」 — xem tab Lịch đăng`); loadProjects(); }
    else toast(r.error || "Lỗi lưu lịch", false);
  };
  ed.append(days, time, save);
  if (sched.source === "override") {  // kênh CHANNELS đang bị đè → cho về mặc định rule
    const rst = document.createElement("button");
    rst.textContent = "↺ Về rule";
    rst.title = "Xóa lịch sửa tay, quay về lịch mặc định trong rule upload-schedule.md";
    rst.onclick = async () => {
      if (!confirm(`Bỏ lịch sửa tay của 「${p.name_new}」, quay về lịch rule?`)) return;
      const r = await api("/api/project_schedule", { key: p.key, weekdays: [] });
      if (r.ok) { toast(`↺ 「${p.name_new}」 về lịch rule`); loadProjects(); } else toast(r.error || "Lỗi", false);
    };
    ed.append(rst);
  }
  box.append(ed);
  const hint = document.createElement("div");
  hint.className = "proj-sched-note";
  hint.textContent = p.in_channels
    ? `Sửa ở đây = ĐÈ lịch rule cho kênh này (giờ ${sched.tz_name}); ↺ để về mặc định. Mỗi kênh 1 giờ cố định.`
    : `Chọn thứ + 1 giờ (giờ ${sched.tz_name} thị trường) → hiện khung "dự kiến" ở Lịch đăng.`;
  box.append(hint);
  return box;
}

function projCard(p) {
  const card = document.createElement("div");
  const st = PROJ_STATUS[p.status] || PROJ_STATUS.planning;
  card.className = "proj-card " + st.cls;
  const [done, total] = p.progress;
  const pct = total ? Math.round((100 * done) / total) : 0;

  // Header: status select + market + wave
  const head = document.createElement("div");
  head.className = "proj-head";
  const sel = document.createElement("select");
  sel.className = "proj-status " + st.cls;
  sel.title = "Đổi trạng thái hoạt động (bán tự động — lưu ngay)";
  Object.entries(PROJ_STATUS).forEach(([k, v]) => {
    const o = document.createElement("option");
    o.value = k; o.textContent = `${v.dot} ${v.label}`;
    if (k === p.status) o.selected = true;
    sel.append(o);
  });
  sel.onchange = async () => {
    const r = await api("/api/project_set", { key: p.key, status: sel.value });
    if (r.ok) { toast(`「${p.name_new}」 → ${PROJ_STATUS[sel.value].label}`); loadProjects(); }
    else toast(r.error || "Lỗi", false);
  };
  const tags = document.createElement("span");
  tags.className = "proj-tags";
  tags.innerHTML = `<span class="chip c-mkt">${esc(p.market)}</span>` +
    (p.wave >= 1 && p.wave <= 3 ? `<span class="chip">Đợt ${p.wave}</span>` : "");
  head.append(sel, tags);

  // Title + niche + old name
  const title = document.createElement("div");
  title.className = "proj-title";
  title.textContent = p.name_new;
  const niche = document.createElement("div");
  niche.className = "proj-niche";
  niche.textContent = p.niche_vn || "";
  card.append(head, title, niche);
  if (p.old_name) {
    const old = document.createElement("div");
    old.className = "proj-old";
    old.innerHTML = `↩ rebrand từ <span class="strike">${esc(p.old_name)}</span>`;
    card.append(old);
  }

  // Signal chips (dò tự động)
  const chips = document.createElement("div");
  chips.className = "proj-chips";
  chips.innerHTML = sigChips(p.signals, p);
  card.append(chips);

  if (p.note) {
    const note = document.createElement("div");
    note.className = "proj-note";
    note.textContent = p.note;
    card.append(note);
  }

  // Checklist chuẩn bị
  if (p.checklist.length) {
    const prog = document.createElement("div");
    prog.className = "proj-prog";
    prog.innerHTML = `<span>Chuẩn bị ${done}/${total}</span><div class="proj-bar"><i style="width:${pct}%"></i></div>`;
    card.append(prog);
    const list = document.createElement("div");
    list.className = "proj-checks";
    p.checklist.forEach((it) => {
      const row = document.createElement("label");
      row.className = "proj-check" + (it.done ? " done" : "") + (it.auto ? " auto" : "");
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = it.done;
      if (it.auto) {
        cb.disabled = true;
        cb.title = it.auto_done ? "Tự tick: hệ thống đã phát hiện" : "Sẽ tự tick khi hệ thống phát hiện";
      } else {
        cb.onchange = async () => {
          await api("/api/project_set", { key: p.key, tick: it.id, on: cb.checked });
          loadProjects();
        };
      }
      const span = document.createElement("span");
      span.innerHTML = (it.auto ? "⚙ " : "") + esc(it.label);
      row.append(cb, span);
      list.append(row);
    });
    card.append(list);
  }

  card.append(projSchedule(p));

  // Actions
  const act = document.createElement("div");
  act.className = "proj-actions";
  if (p.signals.repo_exists) {
    const b = document.createElement("button");
    b.textContent = "📂 Repo";
    b.onclick = async () => toast((await api("/api/proj_open", { key: p.key, what: "repo" })).log);
    act.append(b);
  }
  if (p.profile_dir) {
    const b = document.createElement("button");
    b.textContent = "▶ Studio";
    b.title = "Mở YouTube Studio bằng Chrome profile của kênh này";
    b.onclick = async () => toast((await api("/api/proj_open", { key: p.key, what: "studio" })).log);
    act.append(b);
  }
  const del = document.createElement("button");
  del.className = "danger proj-del";
  del.textContent = "🗑";
  del.title = "Gỡ khỏi bảng quản lý (không đụng repo/file thật)";
  del.onclick = async () => {
    if (!confirm(`Gỡ 「${p.name_new}」 khỏi bảng quản lý?\n(Chỉ xóa khỏi danh sách — repo/profile/file KHÔNG bị đụng)`)) return;
    const r = await api("/api/project_del", { key: p.key });
    if (r.ok) { toast(`Đã gỡ 「${p.key}」`); loadProjects(); } else toast(r.error || "Lỗi", false);
  };
  act.append(del);
  card.append(act);
  return card;
}

/* ---- Tab 🧹 Watermark (rule media-library.md §2.10 ⑤b — vá ✦, nghiệm thu 1:1) ---- */
let WM_LAST = null; // kết quả lượt vá gần nhất — nguồn cho nút 💾 Lưu

async function wmRun() {
  const fd = new FormData();
  let n = 0;
  for (const slot of ["T1", "T2", "T3"]) {
    const inp = $("#wm-f-" + slot);
    if (inp && inp.files[0]) { fd.append(slot, inp.files[0]); n++; }
  }
  if (!n) { toast("Chọn ít nhất 1 ảnh (T1/T2/T3)", false); return; }
  const btn = $("#wm-run");
  btn.disabled = true;
  toast(`🧹 Đang vá ✦ ${n} ảnh…`);
  try {
    const r = await (await fetch("/api/wm_clean", { method: "POST", body: fd })).json();
    if (r.error) { toast(r.error, false); return; }
    WM_LAST = r;
    renderWmResults(r);
    const bad = r.results.filter((x) => x.error).length;
    toast(bad ? `⚠️ Vá xong ${n - bad}/${n} — ${bad} ảnh BỎ QUA (xem lý do bên dưới)`
              : "🧹 Vá xong — SOI crop 1:1 bên dưới TRƯỚC khi lưu", !bad);
  } catch (e) {
    toast("Lỗi vá watermark: " + e, false);
  } finally {
    btn.disabled = false;
  }
}

function renderWmResults(r) {
  const bust = Date.now(); // clean/corners tái dùng TÊN sau mỗi cú vá tay — phải phá cache
  const url = (name) => `/api/wm_img?work=${r.work}&f=${encodeURIComponent(name)}&t=${bust}`;
  const img = (name) => `<img class="wm-crop" src="${url(name)}" loading="lazy">`;
  $("#wm-results").innerHTML = r.results.map((it) => {
    if (it.error) return `
      <div class="channel">
        <div class="ch-head"><b>${it.slot}</b><span class="dim">${it.name}${it.size ? " · lô " + it.size : ""}</span></div>
        <div class="wm-err">🔴 ${it.error}</div>
      </div>`;
    const fixes = it.fixes || [];
    return `
      <div class="channel">
        <div class="ch-head"><b>${it.slot}</b>
          <span class="dim">${it.name} · lô ${it.size}
            · vá tự động: ${it.hits.length ? it.hits.map((h) => h > 0 ? h + " px" : "✗").join(", ") : "—"}
            ${fixes.length ? ` · vá tay ×${fixes.length}: ${fixes.map((f) => f.hits).join(", ")} px` : ""}</span></div>
        ${it.note ? `<div class="wm-err">⚠️ ${it.note}</div>` : ""}
        <div class="wm-full-row">
          <div><div class="dim">gốc</div><img class="wm-full" src="${url(it.src)}"></div>
          <div><div class="dim">bản sạch — 🖱 <b>bấm thẳng vào dấu ✦ còn sót để vá tay</b></div>
            <img class="wm-full wm-click" src="${url(it.clean)}" onclick="wmFixClick('${it.slot}', event)"
                 title="Bấm đúng tâm ✦ → vá ngay tại điểm bấm"></div>
        </div>
        ${it.spots.length ? `
        <div class="dim" style="margin:10px 0 4px">Mốc ✦ theo lô — 1:1 TRƯỚC → SAU (✦ đè nét chữ = loại ảnh, gen lại):</div>
        <div class="wm-crops">${it.spots.map((s) => img(s.before) + '<span class="wm-arrow">→</span>' + img(s.after)).join('<span class="wm-gap"></span>')}</div>` : ""}
        ${fixes.length ? `
        <div class="dim" style="margin:10px 0 4px">Vá tay — 1:1 TRƯỚC → SAU từng cú bấm:</div>
        <div class="wm-crops">${fixes.map((s) => img(s.before) + '<span class="wm-arrow">→</span>' + img(s.after)).join('<span class="wm-gap"></span>')}</div>` : ""}
        <div class="dim" style="margin:10px 0 4px">4 góc bản sạch, 1:1 (sheet thu nhỏ cho qua ✦ — soi từng ô):</div>
        <div class="wm-crops">${it.corners.map(img).join("")}</div>
      </div>`;
  }).join("");
  $("#wm-save-box").classList.toggle("hidden", !r.results.some((x) => x.clean));
}

async function wmFixClick(slot, ev) {
  if (!WM_LAST) return;
  const el = ev.currentTarget;
  const rect = el.getBoundingClientRect();
  const fx = (ev.clientX - rect.left) / rect.width;
  const fy = (ev.clientY - rect.top) / rect.height;
  toast(`🎯 Vá tay ${slot} tại (${(fx * 100).toFixed(1)}%, ${(fy * 100).toFixed(1)}%)…`);
  const r = await api("/api/wm_fix", {
    work: WM_LAST.work, slot, fx, fy,
    scale: parseFloat($("#wm-radius") ? $("#wm-radius").value : "1"),
  });
  if (r.error) { toast(r.error, false); return; }
  if (r.hits <= 0) {  // không vá gì / bị từ chối — không ghi vào lịch sử, hiện lý do
    toast("⚠️ " + (r.msg || "Quanh điểm bấm không có gì lệch nền — bấm trúng TÂM ✦ hơn"), false, true);
    return;
  }
  const it = WM_LAST.results.find((x) => x.slot === slot);
  it.fixes = it.fixes || [];
  it.fixes.push({ before: r.before, after: r.after, hits: r.hits });
  it.clean = r.clean;
  it.corners = r.corners;
  renderWmResults(WM_LAST);
  toast(`🎯 Đã vá ${r.hits} px tại điểm bấm — soi lại crop 1:1 「Vá tay」`);
}

/* ---- wiring ---- */
document.querySelectorAll(".tab").forEach((b) => b.onclick = () => {
  document.querySelectorAll(".tab, .tabpage").forEach((x) => x.classList.remove("active"));
  b.classList.add("active");
  $("#tab-" + b.dataset.tab).classList.add("active");
  if (b.dataset.tab === "projects") loadProjects();
  if (b.dataset.tab === "schedule") loadSchedule();
  if (b.dataset.tab === "profiles") loadProfiles();
  if (b.dataset.tab === "produce") loadAiModels();
  if (b.dataset.tab === "pending") loadPending();
  if (b.dataset.tab === "kho") loadKho();
});
$("#proj-rescan").onclick = () => { loadProjects(); toast("🔄 Đã dò lại trạng thái từ hệ thống"); };
$("#pa-add").onclick = async () => {
  const key = $("#pa-key").value.trim();
  if (!key) { toast("Điền key dự án (chữ thường/số/gạch ngang)", false); return; }
  const r = await api("/api/project_add", {
    key, name_new: $("#pa-name").value.trim(), niche_vn: $("#pa-niche").value.trim(),
    market: $("#pa-market").value, repo: $("#pa-repo").value.trim(),
    profile_dir: $("#pa-profile").value.trim(), gmail: $("#pa-gmail").value.trim(),
    status: $("#pa-status").value,
  });
  if (r.ok) {
    toast(`➕ Đã thêm dự án 「${key}」`);
    ["#pa-key", "#pa-name", "#pa-niche", "#pa-repo", "#pa-profile", "#pa-gmail"].forEach((q) => ($(q).value = ""));
    $("#proj-add-box").open = false;
    loadProjects();
  } else toast(r.error || "Lỗi thêm dự án", false);
};
$("#prof-refresh").onclick = loadProfiles;
$("#wm-run") && ($("#wm-run").onclick = wmRun);
$("#wm-save") && ($("#wm-save").onclick = async () => {
  if (!WM_LAST) return;
  const files = WM_LAST.results.filter((x) => x.clean)
    .map((x) => ({ slot: x.slot, work: WM_LAST.work }));
  const slug = $("#wm-slug").value.trim();
  if (!slug) { toast("Nhập slug folder video trước", false); return; }
  const r = await api("/api/wm_save", { channel: $("#wm-channel").value, slug, files });
  if (r.error) { toast(r.error, false); return; }
  toast(`💾 Đã lưu vào ${r.dir}\n· ${r.saved.join("\n· ")}`
    + (r.backed && r.backed.length ? `\n(bản cũ dời vào _thumb_old/: ${r.backed.join(", ")})` : ""),
    true, true);
});
// phòng thủ: nếu template lệch (thiếu element) thì bỏ qua, KHÔNG để crash cả script
$("#kho-refresh") && ($("#kho-refresh").onclick = () => loadKho(true));
$("#kho-search") && ($("#kho-search").oninput = renderKho);
$("#kho-ch") && ($("#kho-ch").onchange = renderKho);
$("#pend-refresh") && ($("#pend-refresh").onclick = () => loadPending(true));
$("#pend-search") && ($("#pend-search").oninput = renderPending);
$("#ppanel-close").onclick = () => $("#ppanel").classList.add("hidden");
$("#ppanel").onclick = (e) => { if (e.target.id === "ppanel") $("#ppanel").classList.add("hidden"); };
$("#prof-create").onclick = async () => {
  const key = $("#prof-key").value.trim();
  if (!key) { toast("Điền key kênh (chữ thường/số/gạch ngang)", false); return; }
  const r = await api("/api/profile_create", {
    key,
    name: $("#prof-name").value.trim(),
    gmail: $("#prof-gmail").value.trim(),
    profile_dir: $("#prof-dir").value.trim(),
  });
  toast(r.log, r.ok);
  if (r.ok) { ["#prof-key", "#prof-name", "#prof-gmail", "#prof-dir"].forEach((q) => $(q).value = ""); loadProfiles(); }
};
$("#refresh").onclick = () => {
  loadStatus();  // nạp lại dropdown kênh
  const t = document.querySelector(".tab.active")?.dataset.tab;
  if (t === "projects") loadProjects();
  else if (t === "schedule") loadSchedule();
  else if (t === "kho") loadKho(true);
  else if (t === "pending") loadPending(true);
  else if (t === "profiles") loadProfiles();
  else if (t === "produce") { loadAiModels(); loadJobs(); }
};
$("#panel-close").onclick = () => $("#panel").classList.add("hidden");
$("#panel").onclick = (e) => { if (e.target.id === "panel") $("#panel").classList.add("hidden"); };
document.querySelectorAll("#panel-actions [data-open]").forEach((b) =>
  b.onclick = () => openFolder(CURRENT.channel, CURRENT.slug, b.dataset.open));
$("#panel-done").onclick = () => markDone(CURRENT.channel, CURRENT.slug);
$("#panel-repack").onclick = async () => {
  await pack(CURRENT.channel, CURRENT.slug);
  openPanel(CURRENT.channel, CURRENT.slug); // mở lại panel với giờ hẹn mới
};
$("#panel-ai-fix").onclick = async () => {
  if (!confirm(`AI sẽ bổ sung vào script của ${CURRENT.slug}:\n- ${CURRENT.missing.join("\n- ")}\n\nrồi đóng gói lại. Chạy nền vài phút. OK?`)) return;
  const r = await api("/api/job", {
    type: "fix_meta", channel: CURRENT.channel, slug: CURRENT.slug,
    missing: CURRENT.missing.join(", "),
  });
  if (r.error) { toast(r.error, false); return; }
  toast(`🤖 Job bổ sung đã chạy nền (${r.id}) — theo dõi ở tab 🏭 Sản xuất, xong thì mở lại panel này`);
};
$("#slot-add-btn").onclick = async () => {
  const channel = $("#slot-add-channel").value;
  const date = $("#slot-add-date").value;
  const time = $("#slot-add-time").value;
  if (!channel || !date || !time) { toast("Chọn đủ kênh + ngày + giờ", false); return; }
  const r = await api("/api/slot_add", { channel, date, time });
  if (r.error) { toast(r.error, false); return; }
  toast(`➕ Đã thêm slot ${time} VN ngày ${date} cho ${channel}`);
  loadSchedule();
};
$("#schedule-ai-btn").onclick = async () => {
  const channel = $("#slot-add-channel").value;
  if (!channel) return;
  const btn = $("#schedule-ai-btn");
  const out = $("#schedule-ai");
  btn.disabled = true;
  out.classList.remove("hidden");
  out.textContent = `🤖 AI đang nghiên cứu giờ vàng cho [${channel}] — đối chiếu baseline + kéo giờ đăng thật ↔ view thật, ~30–90 giây…`;
  out.scrollIntoView({ behavior: "smooth" });
  try {
    const r = await api("/api/ai_schedule", { channel });
    out.textContent = r.log || "(không có output)";
  } catch (e) {
    out.textContent = "Lỗi gọi AI: " + e;
  }
  btn.disabled = false;
};
$("#ana-load").onclick = () => anaRun("load");
$("#ana-ai").onclick = () => {
  const ch = $("#ana-channel").value;
  if (ch) aiAnalyze(ch, null, null, $("#ana-ai"));
};
$("#ana-check").onclick = () => anaRun("check");
$("#ana-sync").onclick = () => {
  if (confirm("Sync sẽ TỰ move folder các video phát hiện đã lên kênh. Chắc chưa?")) anaRun("sync");
};

/* ---- Tab Sản xuất (jobs) ---- */
let watchingJob = null;
let lastJobStatus = {}; // id -> status lần poll trước (để toast khi job chuyển done/failed)

async function loadVoiceStatus() {
  try {
    const v = await (await fetch("/api/voice_status")).json();
    const dot = (on) => `<span class="${on ? "voice-on" : "voice-off"}">●</span>`;
    $("#voice-status").innerHTML =
      `${dot(v.voicevox)} VOICEVOX ${dot(v.aivis)} AivisSpeech` +
      (!v.voicevox && !v.aivis ? ' <span class="warn">— render job cần voice engine!</span>' : "");
  } catch (e) { /* im lặng */ }
}

// Gợi ý bước kế trong vòng đời: script→render, render→thumbnail, thumbnail→đóng gói
function nextStepBtn(j) {
  const btn = document.createElement("button");
  if (j.type === "script") {
    btn.textContent = "→ 🎬 Render";
    btn.title = "Điền sẵn form render — nhập slug từ log job script";
    btn.onclick = () => {
      $("#job-channel").value = j.channel;
      $("#job-type").value = "render";
      $("#job-input").placeholder = "Nhập slug file script vừa tạo (xem 📜 Log)";
      $("#job-input").focus();
    };
  } else if (j.type === "render") {
    btn.textContent = "→ 🖼️ Thumbnail";
    btn.onclick = () => {
      $("#job-channel").value = j.channel;
      $("#job-type").value = "thumbnail";
      $("#job-input").value = j.label;
      $("#job-input").focus();
    };
  } else if (j.type === "fix_meta") {
    btn.textContent = "→ 📋 Panel";
    btn.title = "Mở lại panel Upload xem đã đủ thông tin chưa";
    btn.onclick = () => openPanel(j.channel, j.label);
  } else {
    btn.textContent = "→ 📦 Đóng gói";
    btn.onclick = () => pack(j.channel, j.label);
  }
  return btn;
}

async function loadJobs() {
  loadVoiceStatus();
  const jobs = await (await fetch("/api/jobs")).json();
  jobs.forEach((j) => {
    if (lastJobStatus[j.id] === "running" && (j.status === "done" || j.status === "failed")) {
      toast(`${j.status === "done" ? "✅" : "❌"} Job ${j.type} [${j.channel}] ${j.label} → ${j.status.toUpperCase()}`,
            j.status === "done");
    }
    lastJobStatus[j.id] = j.status;
  });
  const box = $("#jobs-list");
  if (!jobs.length) { box.textContent = "chưa có job nào"; return; }
  box.innerHTML = "";
  const badge = { running: "b-render", done: "b-goi", failed: "b-do", killed: "b-script" };
  const icon = { script: "✍️", render: "🎬", thumbnail: "🖼️", fix_meta: "🩹" };
  jobs.forEach((j) => {
    const row = document.createElement("div");
    row.className = "video";
    const meta = document.createElement("span");
    meta.className = "slug";
    meta.textContent = `${j.started} ${icon[j.type] || ""} ${j.type} · ${j.channel}`;
    const label = document.createElement("span");
    label.style.flex = "1";
    label.textContent = j.label;
    const st = document.createElement("span");
    st.className = `badge ${badge[j.status] || "b-script"}`;
    st.textContent = j.status === "running" ? "ĐANG CHẠY" : j.status.toUpperCase();
    const act = document.createElement("span");
    act.className = "actions";
    const logBtn = document.createElement("button");
    logBtn.textContent = "📜 Log";
    logBtn.onclick = () => watchJob(j.id);
    act.append(logBtn);
    if (j.status === "done") act.append(nextStepBtn(j));
    if (j.status === "running") {
      const killBtn = document.createElement("button");
      killBtn.className = "danger";
      killBtn.textContent = "✕";
      killBtn.title = "Dừng job";
      killBtn.onclick = async () => {
        if (confirm("Dừng job này?")) { await api("/api/job_kill", { id: j.id }); loadJobs(); }
      };
      act.append(killBtn);
    }
    row.append(meta, label, st, act);
    box.append(row);
  });
}

async function watchJob(id) {
  watchingJob = id;
  const pre = $("#job-log");
  pre.classList.remove("hidden");
  const tick = async () => {
    if (watchingJob !== id) return;
    const r = await (await fetch(`/api/job_log?id=${id}`)).json();
    pre.textContent = `[${r.status}] job ${id}\n${"─".repeat(60)}\n${r.log || "(đang khởi động…)"}`;
    pre.scrollTop = pre.scrollHeight;
    if (r.status === "running") setTimeout(tick, 4000);
    else loadJobs();
  };
  tick();
  pre.scrollIntoView({ behavior: "smooth" });
}

$("#job-run").onclick = async () => {
  const channel = $("#job-channel").value;
  const type = $("#job-type").value;
  const val = $("#job-input").value.trim();
  if (!val) { toast("Nhập đề tài (script) hoặc slug (render/thumbnail) đã", false); return; }
  const body = { type, channel };
  if (type === "script") body.premise = val; else body.slug = val;
  const r = await api("/api/job", body);
  if (r.error) { toast(r.error, false); return; }
  toast(r.warn ? `🚀 Job đã chạy nền: ${r.id}\n${r.warn}` : `🚀 Job đã chạy nền: ${r.id} — bấm 📜 Log để theo dõi`, !r.warn);
  $("#job-input").value = "";
  await loadJobs();
  watchJob(r.id);
};
$("#jobs-refresh").onclick = loadJobs;
setInterval(() => { if ($("#tab-produce").classList.contains("active")) loadJobs(); }, 15000);

loadProjects();        // tab mặc định giờ là 📋 Dự án
loadStatus();          // nạp dropdown kênh cho tab Analytics/Sản xuất
setInterval(loadStatus, 60000);
loadSchedule();        // nạp sẵn dropdown slot-add + cache cho tab Lịch đăng
// Lịch là cửa sổ trượt "7 ngày tới" — treo tab qua đêm vẫn tự trôi theo ngày mới
setInterval(() => { if ($("#tab-schedule").classList.contains("active")) loadSchedule(); }, 300000);
loadJobs();
