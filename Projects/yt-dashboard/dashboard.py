# -*- coding: utf-8 -*-
"""
dashboard.py — web dashboard local quản lý pipeline YouTube đa kênh.

Chạy:  python dashboard.py   (hoặc double-click run_dashboard.cmd)
→ tự mở http://127.0.0.1:8765 — bảng trạng thái mọi kênh, nút đóng gói / panel
upload copy-từng-ô / đánh dấu đã đăng (chuyển kho) / đối chiếu kênh thật / analytics.

TÁI SỬ DỤNG: mọi logic nghiệp vụ nằm ở bộ engine (upload_pack / pipeline_status /
analytics_report) trong `config.json → tools_dir`. Bộ kênh khác → đổi tools_dir.
Dashboard chỉ là lớp vỏ: đọc = import hàm, ghi = subprocess gọi CLI (log chuẩn).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
CFG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
TOOLS = Path(CFG["tools_dir"])
PORT = int(CFG.get("port", 8765))
sys.path.insert(0, str(TOOLS))

from flask import Flask, jsonify, render_template, request, send_file

from upload_pack import (CHANNELS, PROJECTS_ROOT, VN_TZ, WEEKDAY_VN, find_video_dir,  # engine
                         slot_hm, slot_key)
from pipeline_status import scan_channel, upcoming_slots

PY = sys.executable
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # sửa index.html là có ngay, khỏi restart (tránh lệch template↔app.js)
app.jinja_env.auto_reload = True

HIST = BASE / "history"  # snapshot analytics + AI report (engine giữ stateless, dashboard tự lưu)


@app.before_request
def _guard_host():
    # Chặn DNS rebinding: trang web lạ trỏ domain về 127.0.0.1 sẽ mang Host lạ.
    if request.host.split(":")[0] not in ("127.0.0.1", "localhost"):
        return "forbidden", 403


def run_tool(script: str, *args: str, timeout: int = 600) -> tuple[bool, str]:
    try:
        p = subprocess.run([PY, str(TOOLS / script), *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""))
        return False, f"⏱️ QUÁ {timeout}s — process bị dừng giữa chừng!\n{out}".strip()
    return p.returncode == 0, ((p.stdout or "") + (p.stderr or "")).strip()


def save_history(channel: str, kind: str, text: str, ext: str = "txt") -> Path:
    d = HIST / channel
    d.mkdir(parents=True, exist_ok=True)
    f = d / f"{datetime.now():%Y%m%d-%H%M%S}_{kind}.{ext}"
    f.write_text(text, encoding="utf-8")
    return f


@app.get("/")
def index():
    return render_template("index.html")


CHSTATE = BASE / "channels_state.json"  # bật/tắt kênh trên dashboard: {"key": {"active": false}}


def _inactive() -> set:
    try:
        d = json.loads(CHSTATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return {k for k, v in d.items() if not v.get("active", True)}


@app.post("/api/channel_active")
def api_channel_active():
    d = request.json
    if d["channel"] not in CHANNELS:
        return jsonify({"error": "kênh không tồn tại"}), 400
    try:
        st = json.loads(CHSTATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        st = {}
    st.setdefault(d["channel"], {})["active"] = bool(d["active"])
    CHSTATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    return jsonify({"ok": True})


@app.get("/api/status")
def api_status():
    out = []
    inact = _inactive()
    for key in sorted(CHANNELS):
        if key in inact:  # kênh tắt: không scan, không slot — chỉ trả tên để hiện chỗ bật lại
            out.append({"key": key, "name": CHANNELS[key]["name"], "active": False,
                        "uploaded": 0, "rows": [], "slots": [], "suggest": [],
                        "has_token": False})
            continue
        st = scan_channel(key)
        cfg = st["cfg"]
        slots = upcoming_slots(cfg)
        queue = [s for s, stg in st["rows"] if stg.startswith("GÓI SẴN")] + \
                [s for s, stg in st["rows"] if stg.startswith("RENDER ✓")]
        out.append({
            "key": key, "name": cfg["name"], "active": True, "uploaded": st["uploaded"],
            "rows": [{"slug": s, "stage": stg} for s, stg in st["rows"]],
            "slots": slots,
            "suggest": [{"slot": sl, "slug": q} for sl, q in zip(slots, queue)],
            "has_token": (PROJECTS_ROOT / cfg["project"] / "credentials" / "token.json").exists(),
        })
    return jsonify(out)


OVERRIDES = BASE / "schedule_overrides.json"  # ghim tay video↔slot: "date|channel|hh:mm" -> slug ("" = để trống)


def _load_overrides(today_iso: str = "") -> dict:
    try:
        ov = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if today_iso:  # tự dọn ghim của ngày đã qua
        ov = {k: v for k, v in ov.items() if k.split("|")[0] >= today_iso}
    return ov


EXTRA_SLOTS = BASE / "extra_slots.json"  # slot thêm tay theo ngày: ["date|hh:mm_VN|channel", ...]


def _load_extras(today_iso: str = "") -> list[str]:
    try:
        ex = json.loads(EXTRA_SLOTS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if today_iso:
        ex = [e for e in ex if e.split("|")[0] >= today_iso]
    return ex


@app.post("/api/slot_add")
def api_slot_add():
    """Thêm 1 slot lẻ (ngày + giờ VN + kênh) vào lịch — không đụng lịch cố định trong engine."""
    d = request.json
    if d["channel"] not in CHANNELS:
        return jsonify({"error": "kênh không tồn tại"}), 400
    try:
        datetime.strptime(f"{d['date']} {d['time']}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "ngày/giờ sai format (YYYY-MM-DD / HH:MM)"}), 400
    ekey = f"{d['date']}|{d['time']}|{d['channel']}"
    ex = _load_extras(datetime.now().date().isoformat())
    if ekey not in ex:
        ex.append(ekey)
    EXTRA_SLOTS.write_text(json.dumps(ex, ensure_ascii=False, indent=1), encoding="utf-8")
    return jsonify({"ok": True})


@app.post("/api/slot_del")
def api_slot_del():
    d = request.json
    ekey = f"{d['date']}|{d['time']}|{d['channel']}"
    ex = [e for e in _load_extras(datetime.now().date().isoformat()) if e != ekey]
    EXTRA_SLOTS.write_text(json.dumps(ex, ensure_ascii=False, indent=1), encoding="utf-8")
    # dọn luôn ghim gắn vào slot vừa xóa
    ov = _load_overrides()
    ov.pop(f"{d['date']}|{d['channel']}|{d['time']}", None)
    OVERRIDES.write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")
    return jsonify({"ok": True})


@app.post("/api/slot_pin")
def api_slot_pin():
    """Ghim/bỏ ghim video vào 1 slot cụ thể (chỉ đổi hiển thị ghép lịch — muốn chốt giờ hẹn
    thật vào METADATA thì bấm 📦⏰ gói lại với slot đó)."""
    d = request.json
    okey = f"{d['date']}|{d['channel']}|{d['time']}"
    ov = _load_overrides(datetime.now().date().isoformat())
    if d.get("clear"):
        ov.pop(okey, None)
    else:
        ov[okey] = d.get("slug", "")
    OVERRIDES.write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")
    return jsonify({"ok": True})


@app.get("/api/schedule")
def api_schedule():
    """Lịch đăng 7 ngày tới, GỘP mọi kênh, quy về giờ VN (giờ bấm nút đăng theo
    upload-schedule.md). Slot có ghim tay (schedule_overrides.json) thì theo ghim,
    còn lại tự ghép queue (GÓI SẴN trước, RENDER ✓ sau)."""
    from datetime import timedelta, timezone as _tzc
    days_n = min(int(request.args.get("days", 7)), 14)
    vn = _tzc(timedelta(hours=VN_TZ))
    now_vn = datetime.now(vn)
    ov = _load_overrides(now_vn.date().isoformat())
    extras = _load_extras(now_vn.date().isoformat())
    grid: dict[str, list] = {}
    queues: dict[str, list] = {}
    names: dict[str, str] = {}
    _projs = _load_projects().get("projects", [])
    # Kênh tắt = channels_state (nút 💤 cũ) HOẶC status=paused ở tab Dự án — union để 2 nguồn khỏi lệch
    inact = _inactive() | {p["key"] for p in _projs if p.get("status") == "paused"}
    # Lịch override đặt tay từ tab Dự án (projects.json) — kênh nào có slots thì đè lịch rule
    _psched = {p["key"]: (p.get("slots") or []) for p in _projs}
    for key in sorted(CHANNELS):
        if key in inact:  # kênh tắt không chiếm slot trên lịch
            continue
        st = scan_channel(key)
        cfg = st["cfg"]
        names[key] = cfg["name"]
        stages = dict(st["rows"])
        uploaded_set = set(st.get("uploaded_slugs", []))  # đã chuyển kho (07_UPLOADED) → KHÔNG hiện trong lịch đăng
        queue_all = [s for s, stg in st["rows"] if stg.startswith("GÓI SẴN")] + \
                    [s for s, stg in st["rows"] if stg.startswith("RENDER ✓")]
        queues[key] = [{"slug": s, "stage": stages[s]} for s in queue_all]
        pinned_slugs = {v for k2, v in ov.items() if k2.split("|")[1] == key and v}
        queue = [s for s in queue_all if s not in pinned_slugs]
        tz = _tzc(timedelta(hours=cfg["tz"]))
        now = datetime.now(tz)
        slots_use = _psched.get(key) or cfg["slots"]  # override từ tab Dự án > lịch rule
        # Gom slot cố định + slot thêm tay, xếp theo thời gian rồi mới ghép queue (giữ thứ tự đúng)
        times: list[tuple] = []  # (t_local, tv, extra?)
        for d in range(days_n + 1):  # +1 ngày local đệm lệch múi giờ
            day = (now + timedelta(days=d)).date()
            for slot in sorted(slots_use, key=slot_key):
                wd, hour, minute = slot_hm(slot)
                if day.weekday() != wd:
                    continue
                t = datetime(day.year, day.month, day.day, hour, minute, tzinfo=tz)
                if t.date() < now.date():  # chỉ bỏ slot của NGÀY đã qua — giữ nguyên slot hôm nay dù đã quá giờ (hết ngày mới chuyển)
                    continue
                tv = t.astimezone(vn)
                if (tv.date() - now_vn.date()).days >= days_n:
                    continue
                times.append((t, tv, False))
        for e in extras:
            e_date, e_time, e_ch = e.split("|")
            if e_ch != key:
                continue
            tv = datetime.strptime(f"{e_date} {e_time}", "%Y-%m-%d %H:%M").replace(tzinfo=vn)
            if tv.date() < now_vn.date() or (tv.date() - now_vn.date()).days >= days_n:  # giữ slot lẻ hôm nay dù quá giờ
                continue
            times.append((tv.astimezone(tz), tv, True))
        for t, tv, extra in sorted(times, key=lambda x: x[0]):
            okey = f"{tv.date().isoformat()}|{key}|{tv:%H:%M}"
            past = tv <= now_vn  # slot hôm nay đã qua giờ (vẫn hiện cả ngày, nhưng xử lý khác)
            if okey in ov:
                slug, pin = ov[okey] or None, True
            elif past:
                # đã qua giờ + không ghim → hiện slot để tham chiếu nhưng KHÔNG hút video
                # trong hàng đợi (nếu không, video kế sẽ bị "ăn" vào ô đã qua, mất đề xuất cho ngày sau)
                slug, pin = None, False
            else:
                slug, pin = (queue.pop(0) if queue else None), False
            if slug and slug in uploaded_set:   # video đã chuyển kho → bỏ khỏi lịch (kể cả pin override cũ còn sót)
                slug, pin = None, False
            grid.setdefault(tv.date().isoformat(), []).append({
                "sort": tv.strftime("%H:%M"), "vn": tv.strftime("%H:%M"),
                "local": f"{t:%H:%M} {cfg['tz_name']}" if cfg["tz"] != VN_TZ else "",
                "slot_arg": f"{t:%Y-%m-%d %H:%M}",  # format --slot của upload_pack (giờ local kênh)
                "key": key, "name": cfg["name"], "video": slug,
                "stage": stages.get(slug) if slug else None, "pinned": pin, "extra": extra,
                "past": past,
            })
    # Kênh MỚI (ngoài CHANNELS) có lịch đặt tay trong projects.json → khung "dự kiến" (chưa có video)
    for p in _load_projects().get("projects", []):
        pk = p["key"]
        if pk in CHANNELS or p.get("status") == "paused" or not p.get("slots"):
            continue
        ptz = _tzc(timedelta(hours=p.get("tz", 9)))
        ptzn = p.get("tz_name", "JST")
        names[pk] = p.get("name_new", pk)
        now_p = datetime.now(ptz)
        for dd in range(days_n + 1):
            day = (now_p + timedelta(days=dd)).date()
            for slot in sorted(p["slots"], key=slot_key):
                wd, hour, minute = slot_hm(slot)
                if day.weekday() != wd:
                    continue
                t = datetime(day.year, day.month, day.day, hour, minute, tzinfo=ptz)
                if t.date() < now_p.date():
                    continue
                tv = t.astimezone(vn)
                if tv.date() < now_vn.date() or (tv.date() - now_vn.date()).days >= days_n:
                    continue
                grid.setdefault(tv.date().isoformat(), []).append({
                    "sort": tv.strftime("%H:%M"), "vn": tv.strftime("%H:%M"),
                    "local": f"{t:%H:%M} {ptzn}" if p.get("tz", 9) != VN_TZ else "",
                    "slot_arg": f"{t:%Y-%m-%d %H:%M}", "key": pk, "name": names[pk],
                    "video": None, "stage": None, "pinned": False, "extra": False,
                    "past": tv <= now_vn, "plan": True,
                })
    out = []
    for d in range(days_n):
        day = (now_vn + timedelta(days=d)).date()
        iso = day.isoformat()
        out.append({
            "date": iso, "today": d == 0,
            "label": f"{WEEKDAY_VN[day.weekday()]} {day:%d/%m}",
            "slots": sorted(grid.get(iso, []), key=lambda s: s["sort"]),
        })
    return jsonify({"now": now_vn.strftime("%H:%M %d/%m"), "days": out,
                    "queues": queues, "channels": names})


@app.get("/api/metadata")
def api_metadata():
    key, slug = request.args["channel"], request.args["slug"]
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    if request.args.get("kho"):  # đọc từ kho 07_UPLOADED/<slug>/ (video đã cắt, còn metadata)
        d = proj / "07_UPLOADED" / slug
        vdir = d if d.is_dir() else None
    else:
        vdir = find_video_dir(proj, slug)
    meta = (vdir / "_upload" / "METADATA.txt") if vdir else None
    if not meta or not meta.exists():
        return jsonify({"error": "Chưa có gói — bấm Đóng gói trước."}), 404
    text = meta.read_text(encoding="utf-8-sig")

    def grab(num: str) -> str:
        m = re.search(rf"\[{num}\][^\n]*\n-{{10,}}\n(.*?)\n-{{10,}}", text, re.S)
        return m.group(1).strip() if m else ""

    fname = re.search(r"\[1\][^\n]*\n\s*(\S+\.mp4)", text)
    sched = re.search(r"HẸN GIỜ \(Schedule\):\s*(.+)", text)
    checklist = re.findall(r"\[ \] (.+)", text)
    # Nhắc đo lại trend: job script headless chỉ ước lượng bằng WebSearch (rule youtube-upload-seo.md 0.5)
    if not any("Trends" in c for c in checklist):
        checklist.append("Đã đo lại Google Trends (gprop=youtube, 30 ngày) cho title/hashtag/tag")
    warns = re.findall(r"^\s+- (.+)$", text.split("⚠️ CẢNH BÁO:")[1], re.M) \
        if "⚠️ CẢNH BÁO:" in text else []
    # Giờ hẹn trong METADATA tính LÚC ĐÓNG GÓI — gói xong để lâu chưa đăng thì nó thành quá khứ
    sched_str = sched.group(1).strip() if sched else ""
    sched_past = False
    m2 = re.match(r"(\d{4}-\d{2}-\d{2}) \([^)]*\) (\d{2}:\d{2})", sched_str)
    if m2:
        from datetime import timedelta, timezone as _tzc
        tz = _tzc(timedelta(hours=CHANNELS[key]["tz"]))
        t = datetime.strptime(f"{m2.group(1)} {m2.group(2)}", "%Y-%m-%d %H:%M").replace(tzinfo=tz)
        sched_past = t <= datetime.now(tz)
    pack = meta.parent
    # --- bóc 3 title A/B từ METADATA.txt (upload_pack ghi các dòng "[A1] …" dưới mục [2]) ---
    ab_titles = []
    try:
        for _ln in meta.read_text(encoding="utf-8-sig").splitlines():
            _mm = re.match(r"\s*\[(A\d)\]\s*(.+?)(?:\s*<--.*)?$", _ln)
            if _mm:
                ab_titles.append({"tag": _mm.group(1), "title": _mm.group(2).strip()})
    except Exception:
        pass
    return jsonify({
        "file": fname.group(1) if fname else "", "title": grab("2"),
        "description": grab("3"), "tags": grab("4"), "pinned": grab("9"),
        "schedule": sched_str, "schedule_past": sched_past,
        "checklist": checklist, "warnings": warns,
        "srt": (pack / "subs.srt").exists(),
        "thumb": (pack / "thumbnail.png").exists(),
        # BỘ A/B: thumbnail.png = T1, thumbnail_T2/T3.png = biến thể
        "thumbs": [f.name for f in sorted(pack.glob("thumbnail*.png"))],
        "ab_titles": ab_titles,
    })


@app.get("/api/thumb")
def api_thumb():
    """Serve thumbnail.png trong gói _upload để panel hiện preview."""
    proj = PROJECTS_ROOT / CHANNELS[request.args["channel"]]["project"]
    slug = request.args["slug"]
    if request.args.get("kho"):
        d = proj / "07_UPLOADED" / slug
        vdir = d if d.is_dir() else None
    else:
        vdir = find_video_dir(proj, slug)
    _name = request.args.get("v") or "thumbnail.png"
    if not re.fullmatch(r"thumbnail(_T\d+)?\.png", _name):   # chặn path traversal
        return "", 400
    p = (vdir / "_upload" / _name) if vdir else None
    if not p or not p.exists():
        return "", 404
    return send_file(p, mimetype="image/png", max_age=0)


# ---------------- 🧹 XÓA WATERMARK THUMBNAIL (rule media-library.md §2.10 ⑤b) ----------------
# Vá dấu ✦ trên thumbnail AI đã bake chữ. Logic vá + hằng số mốc ✦ theo LÔ kích thước nằm
# ở tool gốc strip_wm_thumb.py (nguồn sự thật duy nhất) — dashboard chỉ nạp module gọi lại,
# KHÔNG chép công thức, để thêm lô mới chỉ sửa 1 chỗ.
WM_TOOL = PROJECTS_ROOT / "youtube-jp-shokutaku" / "tools" / "strip_wm_thumb.py"
WM_WORK = BASE / "wm_work"
_wm_mod = None


def _wm_tool():
    global _wm_mod
    if _wm_mod is None:
        import importlib.util
        old_stdout = sys.stdout  # tool wrap sys.stdout lúc import — giữ rồi trả lại
        try:
            spec = importlib.util.spec_from_file_location("strip_wm_thumb", WM_TOOL)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        finally:
            if sys.stdout is not old_stdout:
                try:
                    sys.stdout.detach()  # tách buffer — nếu không, wrapper bị GC sẽ ĐÓNG stdout thật
                except Exception:
                    pass
                sys.stdout = old_stdout
        _wm_mod = mod
    return _wm_mod


def _wm_prune():
    """Dọn lượt vá cũ hơn 3 ngày — wm_work chỉ là chỗ nghiệm thu tạm, bản chốt đã copy đi."""
    import time
    if not WM_WORK.is_dir():
        return
    cutoff = time.time() - 3 * 86400
    for d in WM_WORK.iterdir():
        if d.is_dir() and d.stat().st_mtime < cutoff:
            shutil.rmtree(d, ignore_errors=True)


def _wm_crop(im, cx, cy, half_w, half_h, dest):
    """Crop 1:1 quanh (cx,cy), kẹp trong khung — KHÔNG resize (sheet thu nhỏ cho qua ✦)."""
    W, H = im.size
    x0 = max(0, min(W - 2 * half_w, cx - half_w))
    y0 = max(0, min(H - 2 * half_h, cy - half_h))
    im.crop((x0, y0, min(W, x0 + 2 * half_w), min(H, y0 + 2 * half_h))).save(dest)


def _wm_corners(clean, work, slot):
    """4 góc bản sạch 1920×1080, crop 1:1 — rule: soi CẢ 4 góc, sheet thu nhỏ cho qua ✦."""
    names, cw, ch = [], 340, 200
    for j, (cx, cy) in enumerate([(cw // 2, ch // 2), (1920 - cw // 2, ch // 2),
                                  (cw // 2, 1080 - ch // 2), (1920 - cw // 2, 1080 - ch // 2)]):
        p = work / f"{slot}_corner{j}.png"
        _wm_crop(clean, cx, cy, cw // 2, ch // 2, p)
        names.append(p.name)
    return names


WM_ALPHA_NPZ = PROJECTS_ROOT / "_media_library" / "wm_alpha_star.npz"
_wm_alpha = None


def _wm_alpha_tmpl():
    """Alpha map ✦ của generator (đo 2026-08-15 từ ảnh nền đen phẳng, lô 2752×1536, chuẩn
    r=60, max 0.33). ✦ là lớp phủ TRẮNG bán trong suốt cùng shape ở mọi ảnh → biết alpha
    là ĐẢO được phép blend, không phải đoán màu nền."""
    global _wm_alpha
    if _wm_alpha is None and WM_ALPHA_NPZ.exists():
        import numpy as np
        _wm_alpha = np.load(WM_ALPHA_NPZ)["alpha"]
    return _wm_alpha


def _wm_unblend(a, cx, cy, r, rng, tmpl):
    """UNBLEND ✦ trên nền HỖN HỢP (chữ/bóng đổ/vân — nơi mọi cách lấp màu đều lem):
    bg = (px − 255·α·k)/(1 − α·k) — nét chữ, gradient, vân giữ nguyên TỪNG PIXEL.
      · căn tâm: quét ±8px, cực đại presence = tương quan highpass(ảnh)↔highpass(α)
        (đo thật: có ✦ 0.44–1.00 · không ✦ 0.09–0.22 → gate 0.30)
      · k (đậm/nhạt ✦ từng ảnh): quét 0.6–1.4, chọn min |presence sau unblend|
      · còn sót (presence sau >0.12) → dập lõi bằng nội suy harmonic nhỏ.
    Trả >0 = px đã xử · 0 = không thấy ✦ tại đây (không đụng ảnh)."""
    import numpy as np
    from scipy import ndimage
    alpha = tmpl if abs(r - 60) < 2 else np.clip(ndimage.zoom(tmpl, r / 60.0), 0, 0.6)
    if alpha.shape[0] % 2:  # zoom ra cỡ lẻ → cắt 1px cho khớp slice 2*Rt
        alpha = alpha[:-1, :-1]
    Rt = alpha.shape[0] // 2
    H, W = a.shape[:2]
    S = max(6, int(8 * r / 60))
    cx = min(max(cx, Rt + S), W - Rt - S)
    cy = min(max(cy, Rt + S), H - Rt - S)
    act = alpha > 0.02
    a_hp = alpha - ndimage.gaussian_filter(alpha, 4)
    a_hp_n = a_hp[act] - a_hp[act].mean()

    def presence(gray):
        g_hp = gray - ndimage.gaussian_filter(gray, 4)
        v = g_hp[act] - g_hp[act].mean()
        return float((v * a_hp_n).sum() / max(np.sqrt((v ** 2).sum() * (a_hp_n ** 2).sum()), 1e-6))

    core = alpha > 0.12
    c_hp_n = a_hp[core] - a_hp[core].mean()

    def presence_core(gray):
        g_hp = gray - ndimage.gaussian_filter(gray, 4)
        v = g_hp[core] - g_hp[core].mean()
        return float((v * c_hp_n).sum() / max(np.sqrt((v ** 2).sum() * (c_hp_n ** 2).sum()), 1e-6))

    best = (-9.0, 0, 0)
    for dy in range(-S, S + 1):
        for dx in range(-S, S + 1):
            p = presence(a[cy + dy - Rt:cy + dy + Rt, cx + dx - Rt:cx + dx + Rt].mean(axis=2))
            if p > best[0]:
                best = (p, dx, dy)
    p0, dx, dy = best
    if p0 <= 0.30:
        return 0
    cx, cy = cx + dx, cy + dy
    g = a[cy - Rt:cy + Rt, cx - Rt:cx + Rt].mean(axis=2)
    ks = np.arange(0.6, 1.45, 0.05)

    def unb(gray, amap):
        return np.clip((gray - 255.0 * amap) / (1.0 - amap), 0, 255)

    k = ks[int(np.argmin([abs(presence(unb(g, alpha * q))) for q in ks]))]
    # fit thêm k RIÊNG cho lõi (band α>0.12) — profile ✦ chênh giữa các ảnh; kẹp lệch
    # ±0.25 so k toàn cục để không trừ lố thành chóp đen (đã dính khi thả trần +0.75).
    # ⛔ Đừng thay bằng phép LẤP màu: row-median lệch gradient ngang, harmonic kéo màu
    # trắng của viền chữ phía dưới lên — cả hai đã thử và tệ hơn phép ĐẢO.
    ks2 = np.arange(max(0.6, k - 0.25), k + 0.30, 0.05)
    kc = ks2[int(np.argmin([abs(presence_core(unb(g, alpha * (k + (q - k) * np.clip(alpha / 0.2, 0, 1)))))
                            for q in ks2]))]
    amap = (alpha * (k + (kc - k) * np.clip(alpha / 0.2, 0, 1)))[..., None]
    sub = a[cy - Rt:cy + Rt, cx - Rt:cx + Rt]
    a[cy - Rt:cy + Rt, cx - Rt:cx + Rt] = np.clip((sub - 255.0 * amap) / (1.0 - amap), 0, 255)
    return int(act.sum())


def _wm_patch(a, cx, cy, r, rng, manual=False):
    """Vá ✦ tại một điểm — KHÔNG dùng is_glyph của tool gốc. Lý do (bắt được 2026-08-15,
    chouhen 2752×1536): is_glyph coi MỌI pixel tối là nét chữ và né ra → trên nền áo ĐEN
    thì cả nền lẫn dấu ✦ xám đều bị loại, tool 「vá」 mà không đụng một pixel — hits=0/
    hits rác, ✦ còn nguyên. Tool gốc sinh ra cho thumbnail shokutaku (✦ sáng/tường kem).

    Cách mới, chạy được cả nền SÁNG lẫn TỐI:
      1. bg = median màu VÀNH KHUYÊN quanh điểm (r..1.5r) — nền cục bộ, không giả định tông.
      2. mask thô = |pixel − bg| > 8 (kênh lệch nhất, 2 chiều — ăn cả ✦ sáng, ✦ xám, tia mờ).
      3. CHỈ GIỮ các blob dính vùng tâm điểm bấm (scipy.ndimage.label) — chữ/hoạ tiết gần đó
         là blob rời, không bị ăn nhầm. Đây là lớp bảo vệ chữ thay cho is_glyph.
      4. fill từng pixel = median pixel SẠCH cùng hàng trong cửa sổ ±30px (bám gradient/mép
         vật), thiếu thì nới ±90px, kiệt thì dùng bg. + dilate/blur mép + nhiễu ±1.2.
    Trả: >0 = số pixel đã vá · 0 = không có gì lệch nền · mã âm = TỪ CHỐI vá (xem _WM_MSG)."""
    import numpy as np
    from PIL import Image, ImageFilter
    from scipy import ndimage
    H, W = a.shape[:2]
    R2 = int(r * 1.5) + 6
    cx, cy = min(max(cx, R2), W - R2), min(max(cy, R2), H - R2)
    y0, y1, x0, x1 = cy - R2, cy + R2, cx - R2, cx + R2
    box = a[y0:y1, x0:x1]
    h, w = box.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - w / 2) ** 2 + (yy - h / 2) ** 2)
    ring = (d >= r) & (d <= R2 - 3)
    bg = np.median(box[ring], axis=0)
    # Nền đồng nhất? (đo thật chouhen 2026-08-15: nền phẳng 0–16% · nền dính chữ 49–57%
    # → ngưỡng 30%). Nền hỗn hợp ⇒ bg-median vô nghĩa, vá kiểu trung vị là lem loang lên
    # chữ — chuyển sang chế độ BẢNG MÀU (vá được ✦ nằm giữa các nét chữ/mảng màu phẳng).
    if (np.abs(box[ring] - bg).max(axis=1) > 12).mean() > 0.30:
        tmpl = _wm_alpha_tmpl()
        if tmpl is not None:
            got = _wm_unblend(a, cx, cy, r, rng, tmpl)
            if got > 0 or not manual:
                return got  # >0 = xong · 0 = không thấy ✦, auto DỪNG ở đây (không đụng ảnh)
        if manual:  # user khẳng định có dấu tại điểm bấm (dấu khác shape ✦) → vá harmonic
            return _wm_patch_shape(a, box, r, y0, y1, x0, x1, rng)
        return -1
    dev = np.abs(box - bg).max(axis=2)
    rough = (dev > 8) & (d <= r * 1.25)
    if not rough.any():
        return 0
    lab, n = ndimage.label(rough, structure=np.ones((3, 3)))
    keep_ids = set(np.unique(lab[(d <= max(6, r * 0.22)) & rough])) - {0}
    if not keep_ids:  # tâm bấm hơi trượt — lấy blob to nhất trong bán kính
        sizes = ndimage.sum(rough, lab, range(1, n + 1))
        if not len(sizes):
            return 0
        keep_ids = {int(np.argmax(sizes)) + 1}
    # Loại blob CHẠM RÌA vùng phân tích: cấu trúc chạy xuyên qua (viền vật/nét chữ) chứ
    # không phải ✦ cô lập — vá nó là để lại vệt (ca T1 spot2 lem lên viền trắng).
    rim_ids = set(np.unique(lab[d > r * 1.15])) - {0}
    keep_ids -= rim_ids
    if not keep_ids:
        return -3
    mask = np.isin(lab, list(keep_ids))
    if mask.sum() > 2.5 * r * r:  # to bất thường so với ✦ — không vá mù
        return -2
    mask_d = ndimage.binary_dilation(mask, iterations=2)  # nới 2px phủ mép alpha của ✦
    fill = np.empty_like(box)
    for i in range(h):
        row, mrow = box[i], mask_d[i]
        for j in np.flatnonzero(mrow):
            med = None
            for win in (30, 90):
                lo, hi = max(0, j - win), min(w, j + win)
                seg = row[lo:hi][~mrow[lo:hi]]
                if len(seg) >= 8:
                    med = np.median(seg, axis=0)
                    break
            fill[i, j] = bg if med is None else med
    m = np.asarray(Image.fromarray((mask_d * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(1.6)), dtype=float) / 255
    m = np.maximum(m, mask_d * 1.0)[..., None]  # trong mask vá đủ 100%, mép ngoài mờ dần
    a[y0:y1, x0:x1] = box * (1 - m) + np.where(mask_d[..., None], fill, box) * m
    a[y0:y1, x0:x1] += rng.normal(0, 1.2, box.shape) * (m > 0.2)
    return int(mask.sum())


def _wm_patch_shape(a, box, r, y0, y1, x0, x1, rng):
    """VÁ TRÒN NHỎ tại điểm bấm — đường cuối khi nền hỗn hợp mà mẫu ✦ không khớp
    (vết SÓT sau unblend, dấu khác shape). Mask tròn 0.30r (default r=60 → 18px — đo
    thật: vá chóp sót T3 bằng vòng 14px là sạch, viền chữ cách ~5px không bị kéo),
    fill nội suy HARMONIC từ mép vào. ⚠️ Vùng càng to càng dễ kéo nhầm màu cấu trúc
    lân cận — cỡ vùng vá do user chọn, có crop 1:1 nghiệm thu."""
    import numpy as np
    from PIL import Image, ImageFilter
    from scipy import ndimage
    h, w = box.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    s = max(8.0, r * 0.30)
    mask = (xx - w / 2) ** 2 + (yy - h / 2) ** 2 <= s * s
    mask = ndimage.binary_dilation(mask, iterations=2)
    _, (iy, ix) = ndimage.distance_transform_edt(mask, return_indices=True)
    fill = box.copy()
    fill[mask] = box[iy[mask], ix[mask]]
    for _ in range(1200):
        avg = (np.roll(fill, 1, 0) + np.roll(fill, -1, 0)
               + np.roll(fill, 1, 1) + np.roll(fill, -1, 1)) / 4
        fill[mask] = avg[mask]
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(1.5)), dtype=float) / 255
    m = np.maximum(m, mask * 1.0)[..., None]
    a[y0:y1, x0:x1] = box * (1 - m) + np.where(mask[..., None], fill, box) * m
    a[y0:y1, x0:x1] += rng.normal(0, 1.0, box.shape) * (m > 0.2)
    return int(mask.sum())


# Mã trả về của _wm_patch → lời giải thích cho user (hiện ở note/toast)
_WM_MSG = {
    0: "không thấy dấu ✦ tại điểm này (đã đối chiếu mẫu ✦ của generator) — chỗ đó có thể vốn sạch; "
       "còn thấy dấu thì bấm trúng TÂM nó hơn",
    -1: "nền quanh điểm hỗn hợp mà máy chưa có mẫu ✦ (thiếu _media_library/wm_alpha_star.npz) — "
        "bấm tay vào dấu để vá",
    -2: "vùng lệch to bất thường so với một dấu ✦ — không vá mù",
    -3: "vùng lệch dính điểm này chạy XUYÊN rìa vùng vá (viền vật/nét chữ, không phải ✦ cô lập) "
        "— ✦ có tia dài thì tăng 「cỡ vùng vá」 rồi bấm lại",
}


@app.post("/api/wm_clean")
def api_wm_clean():
    """Nhận tối đa 3 ảnh (field T1/T2/T3 theo bộ A/B 3×3). Lô đã có mốc ✦ → vá tự động;
    lô lạ / mốc trượt → KHÔNG vá mù, trả preview để user VÁ TAY: bấm thẳng vào dấu ✦
    (/api/wm_fix — chốt vị trí bằng MẮT, đúng rule vì máy định vị đã thất bại 4/4 lần).
    Luôn giữ bản full-res <slot>_work.png làm trạng thái hiện tại + crop 1:1 nghiệm thu."""
    import numpy as np
    from PIL import Image
    mod = _wm_tool()
    _wm_prune()
    work = WM_WORK / datetime.now().strftime("%Y%m%d-%H%M%S")
    work.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    results = []
    for slot in ("T1", "T2", "T3"):
        f = request.files.get(slot)
        if not f or not f.filename:
            continue
        stem = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(f.filename).stem)[:60] or slot
        src = work / f"{slot}_src_{stem}.png"
        src.write_bytes(f.read())
        item = {"slot": slot, "name": f.filename, "src": src.name}
        try:
            im = Image.open(src).convert("RGB")
        except Exception as e:
            item["error"] = f"Không đọc được ảnh: {e}"
            results.append(item)
            continue
        W, H = im.size
        item["size"] = f"{W}x{H}"
        a = np.asarray(im).astype(float)
        r = mod.R.get(W, max(20, W // 46))
        spots = mod.SPOTS.get((W, H))
        hits = []
        if spots:
            # vá auto tại mốc lô bằng _wm_patch (KHÔNG dùng clean_one của tool — nó né mọi
            # pixel tối nên bó tay với ✦ xám trên nền đen, ca chouhen 2026-08-15)
            hits = [_wm_patch(a, int(W * fx), int(H * fy), r, rng) for fx, fy in spots]
            if any(h < 0 for h in hits):
                item["note"] = " · ".join(
                    f"mốc {i}: {_WM_MSG[h]}" for i, h in enumerate(hits) if h < 0)
            elif all(h == 0 for h in hits):
                item["note"] = ("Mốc lô KHÔNG bắt được gì (hits=0) — ✦ của lô ảnh này nằm CHỖ KHÁC "
                                "(toạ độ ✦ khác nhau giữa các lô) hoặc ảnh vốn sạch. "
                                "Còn thấy ✦ → BẤM THẲNG vào nó trên ảnh 「bản sạch」 để vá tay.")
        else:
            item["note"] = (f"Lô {W}x{H} chưa có mốc ✦ → CHƯA vá tự động (không vá mù). "
                            f"BẤM THẲNG vào dấu ✦ trên ảnh 「bản sạch」 bên dưới để vá tay. "
                            f"Lô đã có mốc: " + " · ".join(f"{w}x{h}" for w, h in mod.SPOTS))
        arr = np.clip(a, 0, 255).astype(np.uint8)
        Image.fromarray(arr).save(work / f"{slot}_work.png")  # trạng thái full-res — nguồn vá tay + xuất chốt
        clean = Image.fromarray(arr).resize((1920, 1080), Image.LANCZOS)
        out = work / f"{slot}_clean_{stem}.jpg"
        clean.save(out, quality=95)
        crops = []
        for i, (fx, fy) in enumerate(spots or []):
            before = work / f"{slot}_spot{i}_before.png"
            after = work / f"{slot}_spot{i}_after.png"
            _wm_crop(im, int(W * fx), int(H * fy), r + 55, r + 45, before)
            sr = round(r * 1920 / W)
            _wm_crop(clean, int(1920 * fx), int(1080 * fy), sr + 55, sr + 45, after)
            crops.append({"before": before.name, "after": after.name})
        item.update({"clean": out.name, "hits": hits, "spots": crops,
                     "corners": _wm_corners(clean, work, slot)})
        results.append(item)
    if not results:
        return jsonify({"error": "Chưa chọn ảnh nào (T1/T2/T3)."}), 400
    return jsonify({"work": work.name, "results": results})


@app.post("/api/wm_fix")
def api_wm_fix():
    """VÁ TAY: user bấm thẳng vào dấu ✦ trên preview → vá trên bản full-res tại đúng điểm đó
    (mặt nạ 2 chiều — ăn cả tia mờ), regen preview + crop trước/sau + 4 góc. Bấm được nhiều lần
    (✦ to có tia, lô 2 dấu…) — mỗi lần vá chồng lên trạng thái hiện tại."""
    import numpy as np
    from PIL import Image
    d = request.json
    work, slot = d.get("work", ""), d.get("slot", "")
    if not re.fullmatch(r"[0-9-]+", work) or slot not in ("T1", "T2", "T3"):
        return jsonify({"error": "Tham số sai."}), 400
    wdir = WM_WORK / work
    workimg = wdir / f"{slot}_work.png"
    if not workimg.exists():
        return jsonify({"error": "Không thấy ảnh làm việc — chạy lại 🧹 Xóa watermark."}), 404
    try:
        fx, fy = float(d["fx"]), float(d["fy"])
        assert 0.0 <= fx <= 1.0 and 0.0 <= fy <= 1.0
    except Exception:
        return jsonify({"error": "Toạ độ điểm bấm sai."}), 400
    mod = _wm_tool()
    im = Image.open(workimg).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(float)
    r = int(mod.R.get(W, max(20, W // 46)) * float(d.get("scale", 1.0)))
    r = max(16, min(r, min(W, H) // 4))
    cx, cy = int(W * fx), int(H * fy)
    hit = _wm_patch(a, cx, cy, r, np.random.default_rng(7), manual=True)
    arr = np.clip(a, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(workimg)
    clean = Image.fromarray(arr).resize((1920, 1080), Image.LANCZOS)
    cleans = sorted(wdir.glob(f"{slot}_clean_*.jpg"))
    cname = cleans[0].name if cleans else f"{slot}_clean_fix.jpg"
    clean.save(wdir / cname, quality=95)
    ts = datetime.now().strftime("%H%M%S%f")
    bname, aname = f"{slot}_fix{ts}_b.png", f"{slot}_fix{ts}_a.png"
    _wm_crop(im, cx, cy, r + 55, r + 45, wdir / bname)      # im = TRƯỚC cú vá này
    sr = round(r * 1920 / W)
    _wm_crop(clean, int(1920 * fx), int(1080 * fy), sr + 55, sr + 45, wdir / aname)
    return jsonify({"ok": True, "hits": hit, "msg": _WM_MSG.get(hit, "") if hit <= 0 else "",
                    "clean": cname, "before": bname, "after": aname,
                    "corners": _wm_corners(clean, wdir, slot)})


@app.get("/api/wm_img")
def api_wm_img():
    """Serve ảnh trong wm_work để nghiệm thu — chỉ nhận tên file phẳng (chặn path traversal)."""
    work, name = request.args.get("work", ""), request.args.get("f", "")
    if not re.fullmatch(r"[0-9-]+", work) or not re.fullmatch(r"[A-Za-z0-9._-]+", name):
        return "", 400
    p = WM_WORK / work / name
    if not p.exists():
        return "", 404
    return send_file(p, max_age=0)


@app.post("/api/wm_save")
def api_wm_save():
    """Xuất bản chốt vào folder video, tên CHUẨN GÓI UPLOAD (user chốt 2026-08-15):
    T1 → thumbnail.png · T2 → thumbnail_T2.png · T3 → thumbnail_T3.png (1920×1080, từ
    bản full-res đã vá). PNG vượt trần 2 MB của YouTube → xuất thêm .jpg q95 cạnh nó
    (rule ab-3title-3thumb §3 mục 4). File cũ trùng tên KHÔNG mất — dời vào _thumb_old/."""
    from PIL import Image
    d = request.json
    key, slug = d.get("channel", ""), (d.get("slug") or "").strip()
    if key not in CHANNELS or not slug:
        return jsonify({"error": "Chọn kênh + nhập slug folder video trước."}), 400
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    vdir = find_video_dir(proj, slug)
    if not vdir:
        return jsonify({"error": f"Không thấy folder video 「{slug}」 trong {CHANNELS[key]['project']}."}), 404
    NAMES = {"T1": "thumbnail", "T2": "thumbnail_T2", "T3": "thumbnail_T3"}
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    def _backup(p: Path):
        if p.exists():
            old = vdir / "_thumb_old"
            old.mkdir(exist_ok=True)
            dst = old / f"{p.stem}_{ts}{p.suffix}"
            try:
                shutil.move(str(p), dst)
            except PermissionError:  # file đang bị mở (Explorer preview…) — copy vẫn giữ được bản cũ
                shutil.copy2(p, dst)
            return True
        return False

    saved, backed = [], []
    for it in d.get("files", []):
        work, slot = it.get("work", ""), it.get("slot", "")
        if not re.fullmatch(r"[0-9-]+", work) or slot not in NAMES:
            continue
        src = WM_WORK / work / f"{slot}_work.png"
        if not src.exists():
            continue
        im = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
        dest = vdir / f"{NAMES[slot]}.png"
        if _backup(dest):
            backed.append(dest.name)
        im.save(dest)
        mb = dest.stat().st_size / 1024 / 1024
        saved.append(f"{dest.name} ({mb:.1f} MB)")
        if mb > 2.0:  # trần 2 MB YouTube — xuất kèm jpg q95, upload dùng bản jpg
            jp = dest.with_suffix(".jpg")
            if _backup(jp):
                backed.append(jp.name)
            im.save(jp, quality=95)
            saved.append(f"{jp.name} ({jp.stat().st_size / 1024 / 1024:.1f} MB — dùng bản này, PNG quá trần 2 MB)")
    if not saved:
        return jsonify({"error": "Không có bản sạch nào để lưu — chạy 🧹 Xóa watermark trước."}), 400
    return jsonify({"ok": True, "dir": str(vdir), "saved": saved, "backed": backed})


@app.get("/api/kho")
def api_kho():
    """Liệt kê video ĐÃ chuyển kho (07_UPLOADED/<slug>/) theo kênh — để tra cứu/update lại.
    Kho đã cắt mp4, chỉ còn _upload (metadata+subs+ảnh) + _scripts + UPLOADED.txt."""
    out = []
    for key, cfg in CHANNELS.items():
        proj = PROJECTS_ROOT / cfg["project"]
        up = proj / "07_UPLOADED"
        items = []
        if up.is_dir():
            for d in sorted((x for x in up.iterdir() if x.is_dir() and not x.name.startswith("_")),
                            reverse=True):
                updir, scr = d / "_upload", d / "_scripts"
                metaf = updir / "METADATA.txt"
                if not metaf.exists():
                    continue  # ẩn video KHÔNG có file metadata (user chốt 2026-07-22)
                mtxt = metaf.read_text(encoding="utf-8-sig")
                mtit = re.search(r"\[2\][^\n]*\n-{10,}\n(.*?)\n-{10,}", mtxt, re.S)
                txt = (d / "UPLOADED.txt").read_text(encoding="utf-8", errors="ignore") \
                    if (d / "UPLOADED.txt").exists() else ""
                mu = re.search(r"uploaded:\s*([\d-]+\s[\d:]+)", txt)   # chỉ lấy ngày giờ, bỏ đuôi ghi chú
                mpu = re.search(r"publishAt:\s*(.+)", txt)
                items.append({
                    "slug": d.name,
                    "title": mtit.group(1).strip() if mtit else "",
                    "uploaded": mu.group(1).strip() if mu else "",
                    "publishAt": mpu.group(1).strip() if mpu else "",
                    "has_thumb": (updir / "thumbnail.png").exists(),
                    "has_srt": (updir / "subs.srt").exists(),
                    "scripts": sorted(p.name for p in scr.glob("*")) if scr.is_dir() else [],
                })
        out.append({"key": key, "name": cfg["name"], "count": len(items), "items": items})
    return jsonify(out)


@app.post("/api/pack")
def api_pack():
    d = request.json
    args = [d["slug"], "--channel", d["channel"], "--force"]
    if d.get("thumb"):
        args += ["--thumb", d["thumb"]]
    if d.get("slot"):  # chốt giờ hẹn cụ thể (format "YYYY-MM-DD HH:MM" giờ local kênh)
        args += ["--slot", d["slot"]]
    ok, log = run_tool("upload_pack.py", *args)
    return jsonify({"ok": ok, "log": log})


@app.post("/api/done")
def api_done():
    """--done kèm AI cắt TikTok + dọn kho (vài phút) → chạy NỀN như job, frontend poll log tới khi xong."""
    d = request.json
    running = [j for j in JOBS.values() if _job_status(j) == "running"]
    if any(j["type"] == "done" and j["label"] == d["slug"] for j in running):
        return jsonify({"error": f"'{d['slug']}' đang chuyển kho rồi — xem log ở tab 🏭 Sản xuất"}), 409
    jid = spawn_tool_job("done", d["channel"], d["slug"],
                         "upload_pack.py", d["slug"], "--channel", d["channel"], "--done")
    return jsonify({"id": jid})


@app.post("/api/sync")
def api_sync():
    d = request.json
    flag = "--sync" if d.get("apply") else "--check"
    ok, log = run_tool("pipeline_status.py", "--channel", d["channel"], flag)
    return jsonify({"ok": ok, "log": log})


@app.get("/api/analytics")
def api_analytics():
    ch = request.args["channel"]
    ok, log = run_tool("analytics_report.py", "--channel", ch,
                       "-n", request.args.get("n", "10"))
    if ok and log:
        f = save_history(ch, "kenh", log)
        log += f"\n\n💾 Đã lưu snapshot: {f}"
    return jsonify({"ok": ok, "log": log})


@app.get("/api/channel_videos")
def api_channel_videos():
    """Danh sách video THẬT trên kênh (kèm videoId) — nguồn cho nút 'Mổ video'."""
    key = request.args["channel"]
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    if not (proj / "credentials" / "token.json").exists():
        return jsonify({"error": "Kênh chưa có token API"}), 400
    from upload_api import get_service  # lazy
    yt = get_service(proj)
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=pl,
                                    maxResults=25).execute().get("items", [])
    ids = ",".join(i["contentDetails"]["videoId"] for i in items)
    vids = yt.videos().list(part="snippet,statistics,status", id=ids).execute()["items"] if ids else []
    return jsonify([{
        "id": v["id"], "title": v["snippet"]["title"],
        "published": v["snippet"].get("publishedAt", "")[:10],
        "views": v.get("statistics", {}).get("viewCount", "0"),
        "privacy": v["status"].get("privacyStatus", "?"),
        "publishAt": v["status"].get("publishAt", ""),
    } for v in vids])


@app.get("/api/video_report")
def api_video_report():
    """Mổ 1 video: theo ngày + nguồn traffic + keyword + retention (analytics_report --video)."""
    ch, vid = request.args["channel"], request.args["video"]
    ok, log = run_tool("analytics_report.py", "--channel", ch, "--video", vid)
    if ok and log:
        f = save_history(ch, f"video-{vid}", log)
        log += f"\n\n💾 Đã lưu snapshot: {f}"
    return jsonify({"ok": ok, "log": log})


def _bring_explorer_front(folder_name: str) -> None:
    """Windows không cho process nền cướp focus → cửa sổ Explorer mở ra nằm SAU browser.
    Tìm cửa sổ CabinetWClass có title bắt đầu bằng tên folder (Win11: '_upload - File Explorer')
    rồi kéo lên trước bằng SwitchToThisWindow + Alt-hack SetForegroundWindow."""
    import ctypes
    u = ctypes.windll.user32
    hit = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if cls.value == "CabinetWClass":
            t = ctypes.create_unicode_buffer(512)
            u.GetWindowTextW(h, t, 512)
            if t.value.startswith(folder_name):
                hit.append(h)
        return True

    u.EnumWindows(cb, 0)
    if hit:
        h = hit[0]
        u.ShowWindow(h, 9)                 # SW_RESTORE
        u.SwitchToThisWindow(h, True)      # kéo lên trước, hoạt động cả từ process nền
        u.keybd_event(0x12, 0, 0, 0)       # Alt down — mở khóa foreground
        u.SetForegroundWindow(h)
        u.keybd_event(0x12, 0, 2, 0)       # Alt up


# ───────────────────────── JOBS: sản xuất bằng Claude Code headless ─────────────────────────
# Mỗi job = 1 agent `claude -p` chạy nền TRONG repo kênh đó (cwd = project) → tự ăn CLAUDE.md
# + skill của kênh. Log stream-json ghi ra file, UI tail + dịch sang dòng người đọc được.
import threading
import uuid

JOBS_DIR = BASE / "jobs"
JOBS_DIR.mkdir(exist_ok=True)
REGISTRY = JOBS_DIR / "registry.json"
JOBS: dict[str, dict] = {}  # id -> {type, channel, label, status, started, pid, proc, log}
_REG_LOCK = threading.Lock()


def _save_registry() -> None:
    with _REG_LOCK:
        rows = [{k: (str(v) if k == "log" else v) for k, v in j.items() if k != "proc"}
                for j in JOBS.values()]
        REGISTRY.write_text(json.dumps({jid: r for jid, r in zip(JOBS, rows)},
                                       ensure_ascii=False, indent=1), encoding="utf-8")


def _pid_alive(pid: int) -> bool:
    """Windows: KHÔNG dùng os.kill(pid, 0) — trên Win nó TerminateProcess luôn."""
    import ctypes
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = ctypes.c_ulong()
    ok = k.GetExitCodeProcess(h, ctypes.byref(code))
    k.CloseHandle(h)
    return bool(ok) and code.value == 259  # STILL_ACTIVE


def _load_registry() -> None:
    """Restart dashboard giữa chừng → job cũ vẫn hiện, probe pid xem còn sống không."""
    if not REGISTRY.exists():
        return
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    for jid, j in list(data.items())[-50:]:
        j["proc"] = None
        j["log"] = Path(j["log"])
        JOBS[jid] = j


def _kill_tree(j: dict) -> None:
    """Giết cả cây process (claude + ffmpeg/python con) — proc.kill() chỉ giết cha."""
    pid = j.get("pid") or (j["proc"].pid if j.get("proc") else None)
    if pid:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
    if j.get("proc") and j["proc"].poll() is None:
        j["proc"].kill()


_load_registry()

JOB_PROMPTS = {
    "script": """Bạn đang đứng trong repo kênh {name}. NHIỆM VỤ: viết MỘT kịch bản video MỚI hoàn chỉnh \
cho kênh này, theo đúng skill biên kịch + CLAUDE.md của project (độ dài chuẩn kênh, văn phong, cấu trúc).

Đề tài / premise: {premise}

Yêu cầu bắt buộc:
1. Làm trọn gói KHÔNG hỏi lại. Đánh số file = số lớn nhất hiện có trong thư mục script + 1.
2. Đủ các khối đóng gói: Title chốt · Tên file upload (slug SEO) · 3 dòng đầu 概要欄 · mô tả đầy đủ \
theo timeline (timestamp điền sau render thì ghi chú rõ) · tags + hashtag · text/prompt thumbnail · \
pinned comment (nếu format kênh có).
3. Xuất luôn file _TTS đúng chuẩn kênh (1 dòng = 1 câu) và chèn câu CTA giữa video canonical theo \
.claude/rules/cta-midvideo.md đúng vị trí.
4. Trend: phiên này KHÔNG có browser — dùng WebSearch ước lượng keyword, và GHI CHÚ rõ trong script \
rằng bảng Google Trends (gprop=youtube, 30 ngày) cần đo lại trước khi upload.
5. Quét compliance theo .claude/rules/youtube-compliance.md, báo từ cần né ngay trong script.
6. Kết thúc: in đường dẫn các file đã tạo + tóm tắt cốt truyện/nội dung 5 dòng.""",

    "render": """Bạn đang đứng trong repo kênh {name}. NHIỆM VỤ: RENDER VIDEO cho script `{slug}` theo \
ĐÚNG pipeline ghi trong CLAUDE.md của project này (chia stage/resume chống bị kill, media lấy qua kho \
chung theo .claude/rules/media-library.md, duyệt contact sheet bằng cách trích frame, verify sau render).

Yêu cầu bắt buộc:
1. Thiếu file _TTS thì tạo từ script trước (đúng chuẩn 1 dòng = 1 câu + CTA giữa video).
2. Voice engine (VOICEVOX port 50021 / AivisSpeech port 10101 tùy kênh) chưa chạy → thử khởi động theo \
đường dẫn đã biết; không được thì DỪNG và ghi rõ user cần mở engine nào rồi chạy lại job.
3. Sau render PHẢI verify: duration khớp voice, phụ đề đổi theo lời (trích 2 frame cách 6s), CTA overlay, \
BGM gain đúng chuẩn kênh (-40dB).
4. Kết thúc: in đường dẫn mp4 + duration + mọi cảnh báo.""",

    "fix_meta": """Bạn đang đứng trong repo kênh {name}. NHIỆM VỤ: BỔ SUNG thông tin upload còn THIẾU \
cho video `{slug}` rồi ĐÓNG GÓI LẠI. Panel upload đang báo thiếu: {missing}

Cách làm bắt buộc:
1. Đọc script của `{slug}` trong 0N_SCRIPTS/ + CLAUDE.md/skill biên kịch của kênh để viết ĐÚNG format \
chuẩn kênh (Title CHỐT / Tên file upload slug SEO / 3 dòng đầu 概要欄 / mô tả đầy đủ theo timeline / \
タグ+hashtag / text+prompt thumbnail / pinned comment nếu format kênh có).
2. CHỈ viết thêm phần thiếu vào đúng mục Đóng gói CTR trong file script — KHÔNG phá phần đã có. \
Tuân .claude/rules/youtube-upload-seo.md (keyword đứng đầu title, 3 dòng đầu không lời chào, mô tả \
200-300 từ theo timeline) + quét .claude/rules/youtube-compliance.md, báo từ cần né. \
Trend: phiên này không có browser — ước lượng bằng WebSearch và GHI CHÚ trong script là cần đo lại \
Google Trends (gprop=youtube, 30 ngày) trước khi đăng.
3. Thiếu thumbnail.png: ảnh nguồn/khuôn kênh đủ thì chạy tool make_thumb + tự duyệt 3 cửa; cần ảnh AI \
gen thì viết prompt hoàn chỉnh vào script, in prompt + ĐƯỜNG DẪN lưu ảnh ra log, ghi rõ user gen xong \
chạy job 🖼️ Thumbnail.
4. Thiếu subs.srt: KHÔNG tự render trong job này — ghi rõ user cần chạy job 🎬 Render.
5. Xong thì đóng gói lại: chạy `python "{tools}\\upload_pack.py" {slug} --channel {channel} --force` \
và dán output (kể cả cảnh báo pre-flight).
6. Kết thúc: liệt kê từng mục ĐÃ bổ sung + việc user còn phải tự làm (nếu có).""",

    "thumbnail": """Bạn đang đứng trong repo kênh {name}. NHIỆM VỤ: làm THUMBNAIL cho video `{slug}` theo \
đúng luật thumbnail của kênh (CLAUDE.md + rule/thư viện khuôn nếu có, 3 nguyên tắc gác cổng hình, \
xoay khuôn chống trùng video liền trước).

Yêu cầu:
1. Đọc khối thumbnail/Đóng gói CTR trong script của `{slug}`.
2. Nếu khuôn cần ẢNH AI GEN mà ảnh chưa có: viết PROMPT hoàn chỉnh (chính + fallback) vào file script \
(nếu chưa có), IN prompt ra log kèm ĐƯỜNG DẪN chính xác user cần lưu ảnh sau khi gen, rồi kết thúc job.
3. Nếu ảnh nguồn đã sẵn: chạy tool make_thumb tương ứng của kênh, tự duyệt 3 cửa (che chữ/so mẫu chuẩn \
kênh/preview 120px), xuất preview, in đường dẫn kết quả.
4. Quét compliance text thumbnail theo rule. Kết thúc: báo rõ trạng thái + việc user còn phải làm (nếu có).""",
}


def spawn_job(jtype: str, channel: str, params: dict) -> str:
    claude = shutil.which("claude")
    if not claude:
        raise RuntimeError("Không tìm thấy claude CLI")
    cfg = CHANNELS[channel]
    proj = PROJECTS_ROOT / cfg["project"]
    prompt = JOB_PROMPTS[jtype].format(name=cfg["name"], channel=channel,
                                       tools=str(TOOLS), **params)
    jid = f"{datetime.now():%m%d-%H%M%S}-{jtype}-{uuid.uuid4().hex[:4]}"
    log = JOBS_DIR / f"{jid}.log"
    f = open(log, "w", encoding="utf-8")
    # Quyền của job agent: allowlist tool cần cho sản xuất (KHÔNG bỏ hết rào chắn).
    # Job chỉ chạy trong repo kênh (cwd) do chính user bấm nút từ localhost.
    proc = subprocess.Popen(
        [claude, "-p", prompt, *_model_args("jobs"), "--output-format", "stream-json", "--verbose",
         "--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep",
         "WebSearch", "WebFetch", "Skill", "ToolSearch", "TodoWrite"],
        stdout=f, stderr=subprocess.STDOUT, cwd=str(proj),
        text=True, encoding="utf-8", errors="replace")
    JOBS[jid] = {"type": jtype, "channel": channel, "status": "running",
                 "label": params.get("slug") or (params.get("premise") or "")[:40],
                 "started": datetime.now().strftime("%H:%M"), "pid": proc.pid,
                 "proc": proc, "log": log}
    _save_registry()
    return jid


# ---------- Model AI cho từng tính năng (user chọn trên web, tab Sản xuất) ----------
AI_MODELS_FILE = BASE / "ai_models.json"  # {"jobs": "sonnet", ...} — thiếu key = dùng mặc định settings máy
AI_PURPOSES = {
    "jobs": "Job sản xuất (script/render/thumbnail)",
    "tiktok": "Chọn đoạn cắt TikTok",
    "analytics": "Phân tích kênh/video",
    "schedule": "Nghiên cứu giờ vàng",
}
AI_MODEL_OPTIONS = ["", "opus", "sonnet", "haiku"]


def _ai_models() -> dict:
    try:
        return json.loads(AI_MODELS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _model_args(purpose: str) -> list:
    """Cờ --model cho claude -p theo lựa chọn trên web; không chọn → [] (ăn mặc định settings máy)."""
    m = _ai_models().get(purpose, "")
    return ["--model", m] if m else []


@app.get("/api/ai_models")
def api_ai_models_get():
    cur = _ai_models()
    return jsonify({"purposes": [{"key": k, "label": v, "model": cur.get(k, "")}
                                 for k, v in AI_PURPOSES.items()],
                    "options": AI_MODEL_OPTIONS})


@app.post("/api/ai_models")
def api_ai_models_set():
    d = request.json
    if d.get("purpose") not in AI_PURPOSES or d.get("model", "") not in AI_MODEL_OPTIONS:
        return jsonify({"error": "purpose/model không hợp lệ"}), 400
    cur = _ai_models()
    if d.get("model"):
        cur[d["purpose"]] = d["model"]
    else:
        cur.pop(d["purpose"], None)
    AI_MODELS_FILE.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")
    return jsonify({"ok": True})


def spawn_tool_job(jtype: str, channel: str, label: str, script: str, *args: str) -> str:
    """Job chạy 1 tool python thuần (không phải claude agent) — log chảy thẳng ra file, xem qua /api/job_log."""
    jid = f"{datetime.now():%m%d-%H%M%S}-{jtype}-{uuid.uuid4().hex[:4]}"
    log = JOBS_DIR / f"{jid}.log"
    f = open(log, "w", encoding="utf-8")
    proc = subprocess.Popen([PY, "-u", str(TOOLS / script), *args],
                            stdout=f, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace")
    JOBS[jid] = {"type": jtype, "channel": channel, "status": "running", "label": label,
                 "started": datetime.now().strftime("%H:%M"), "pid": proc.pid,
                 "proc": proc, "log": log}
    _save_registry()
    return jid


def _job_status(j: dict) -> str:
    if j["status"] in ("killed", "done", "failed"):
        return j["status"]
    if j.get("proc") is not None:
        rc = j["proc"].poll()
        if rc is None:
            return "running"
        j["status"] = "done" if rc == 0 else "failed"
    elif j.get("pid") and _pid_alive(j["pid"]):  # job khôi phục từ registry
        return "running"
    else:
        j["status"] = "done"  # đã kết thúc lúc dashboard tắt — không rõ mã thoát
    _save_registry()
    return j["status"]


def _parse_stream_log(path: Path, tail_chars: int = 12000) -> str:
    """Dịch stream-json của claude -p sang log người đọc được."""
    out = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line.startswith("{"):
                if line:
                    out.append(line)
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "assistant":
                for blk in (ev.get("message") or {}).get("content", []):
                    if blk.get("type") == "text" and blk.get("text", "").strip():
                        out.append(blk["text"].strip())
                    elif blk.get("type") == "tool_use":
                        name = blk.get("name", "?")
                        inp = blk.get("input") or {}
                        hint = (inp.get("command") or inp.get("file_path")
                                or inp.get("pattern") or inp.get("query") or "")
                        out.append(f"  ⚙ {name}: {str(hint)[:110]}")
            elif t == "result":
                out.append("\n══ KẾT QUẢ ══\n" + (ev.get("result") or "").strip())
    except OSError:
        return "(chưa có log)"
    text = "\n".join(out)
    return text[-tail_chars:] if len(text) > tail_chars else text


@app.post("/api/job")
def api_job():
    d = request.json
    jtype = d["type"]
    if jtype not in JOB_PROMPTS:
        return jsonify({"error": "loại job không hợp lệ"}), 400
    params = {"premise": d.get("premise", ""), "slug": d.get("slug", ""),
              "missing": d.get("missing", "(không rõ — tự đối chiếu METADATA với format chuẩn kênh)")}
    if jtype == "script" and not params["premise"].strip():
        return jsonify({"error": "Thiếu đề tài/premise"}), 400
    if jtype in ("render", "thumbnail", "fix_meta") and not params["slug"].strip():
        return jsonify({"error": "Thiếu slug video"}), 400
    label = params["slug"] or params["premise"][:40]
    running = [j for j in JOBS.values() if _job_status(j) == "running"]
    if any(j["type"] == jtype and j["channel"] == d["channel"] and j["label"] == label
           for j in running):
        return jsonify({"error": f"Job {jtype} cho '{label}' đang chạy rồi — chờ xong hoặc kill trước"}), 409
    warn = ""
    if jtype == "render" and any(j["type"] == "render" for j in running):
        warn = "⚠️ Đang có render khác chạy — 2 render tranh voice engine/CPU, cân nhắc chờ."
    jid = spawn_job(jtype, d["channel"], params)
    return jsonify({"id": jid, "warn": warn})


@app.get("/api/jobs")
def api_jobs():
    return jsonify([
        {"id": jid, "type": j["type"], "channel": j["channel"], "label": j["label"],
         "status": _job_status(j), "started": j["started"]}
        for jid, j in sorted(JOBS.items(), reverse=True)
    ])


@app.get("/api/job_log")
def api_job_log():
    j = JOBS.get(request.args["id"])
    if not j:
        return jsonify({"error": "không thấy job"}), 404
    return jsonify({"status": _job_status(j), "log": _parse_stream_log(j["log"])})


@app.post("/api/job_kill")
def api_job_kill():
    j = JOBS.get(request.json["id"])
    if not j:
        return jsonify({"error": "không thấy job"}), 404
    if _job_status(j) == "running":
        _kill_tree(j)
        j["status"] = "killed"
        _save_registry()
    return jsonify({"ok": True})


@app.get("/api/voice_status")
def api_voice_status():
    """Voice engine đang mở không — render job cần nó (VOICEVOX 50021 / AivisSpeech 10101)."""
    import socket

    def up(port: int) -> bool:
        s = socket.socket()
        s.settimeout(0.3)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except OSError:
            return False
        finally:
            s.close()

    return jsonify({"voicevox": up(50021), "aivis": up(10101)})


AI_PROMPT_CHANNEL = """Bạn là chuyên gia tăng trưởng kênh YouTube faceless. Dưới đây là số liệu THẬT \
của kênh. Phân tích bằng tiếng Việt, ngắn gọn, markdown đơn giản:

## 3 phát hiện quan trọng nhất
(mỗi cái kèm con số dẫn chứng từ dữ liệu)

## Nguyên nhân giả định
(mỗi phát hiện 1 nguyên nhân, ghi rõ độ tin cậy: [chắc chắn] / [khả năng cao] / [phỏng đoán])

## 3 hành động ưu tiên tuần này
(cụ thể, làm được ngay, xếp theo tác động/công sức)

Nguyên tắc: KHÔNG bịa số. Nếu cỡ mẫu quá nhỏ để kết luận thì nói thẳng. \
Video <72h tuổi thì chưa phán xét view. Trả lời gọn dưới 400 từ.

=== SỐ LIỆU KÊNH ===
{data}
"""

AI_PROMPT_VIDEO = """Bạn là chuyên gia tối ưu video YouTube faceless dài (朗読/健康/audio drama). \
Dưới đây là số liệu THẬT của MỘT video (theo ngày + nguồn traffic + keyword + đường retention). \
Phân tích bằng tiếng Việt, ngắn gọn, markdown đơn giản:

## Chẩn đoán
- Video đang ở giai đoạn nào (chưa được thuật toán thử / đang sóng đề xuất / sóng đã tắt)? Dẫn chứng.
- Nguồn traffic nói lên điều gì (related vs search vs browse)?
- Retention: hook đầu giữ được bao nhiêu %, plateau ở đâu, rớt mạnh chỗ nào (đổi ra phút), vùng CTA ~50% có gây rớt không?

## Kết luận: giữ gì, sửa gì
(3-4 gạch đầu dòng, cụ thể: thumbnail/title/hook/đề tài/CTA)

Nguyên tắc: KHÔNG bịa số. Ít data thì nói thẳng "chưa đủ data". Trả lời gọn dưới 350 từ.

=== SỐ LIỆU VIDEO ===
{data}
"""


AI_PROMPT_SCHEDULE = """Bạn là chuyên gia tăng trưởng kênh YouTube faceless. Nhiệm vụ: đánh giá \
GIỜ VÀNG ĐĂNG VIDEO cho kênh dưới đây — lịch hiện tại đã tối ưu để kéo view chưa, có nên đổi không. \
Phân tích bằng tiếng Việt, markdown đơn giản, gọn dưới 450 từ:

## Chẩn đoán lịch hiện tại
(so slot hiện tại với baseline nghiên cứu + thói quen khán giả mục tiêu của kênh — hợp lý chỗ nào, đáng ngờ chỗ nào)

## Tín hiệu từ data thật
(video đăng thứ/giờ nào đang kéo view tốt hơn? Nêu con số. GHI RÕ cỡ mẫu — dưới ~10 video thì nói thẳng \
"chưa đủ kết luận, chỉ là gợi ý". Video <72h tuổi chưa phán xét. View tổng bị lệch bởi tuổi video — chú ý chuẩn hóa.)

## Kết luận: GIỮ hay ĐỔI
(nếu ĐỔI: đề xuất thứ + giờ cụ thể và lý do; kèm cách thử nghiệm 2–4 tuần — đăng xen kẽ 2 slot rồi so view 72h đầu)

## Nguồn sự thật cuối
(nhắc: kênh đủ ~10–20 video → YouTube Studio → Audience → "When your viewers are on YouTube" là chuẩn cuối, \
đè mọi baseline; vẫn giữ nguyên tắc đăng trước peak 2–3h)

Nguyên tắc: KHÔNG bịa số. Không suy diễn quá mức từ mẫu nhỏ.

=== KÊNH: {name} — LỊCH CỐ ĐỊNH HIỆN TẠI (giờ địa phương thị trường) ===
{slots}

=== BASELINE NGHIÊN CỨU (rule upload-schedule.md của workspace) ===
{rule}

=== VIDEO ĐÃ ĐĂNG THẬT (giờ địa phương kênh, view tại thời điểm đo) ===
{uploads}
"""


@app.post("/api/ai_schedule")
def api_ai_schedule():
    """AI nghiên cứu giờ vàng: lịch cố định + baseline rule + giờ đăng thật ↔ view thật → giữ/đổi."""
    d = request.json
    key = d["channel"]
    claude = shutil.which("claude")
    if not claude:
        return jsonify({"ok": False, "log": "Không tìm thấy claude CLI trên PATH"}), 500
    cfg = CHANNELS[key]
    from datetime import timedelta, timezone as _tzc
    tz = _tzc(timedelta(hours=cfg["tz"]))
    slots_txt = "\n".join(f"- {WEEKDAY_VN[wd]} {h:02d}:{mi:02d} {cfg['tz_name']}"
                          for wd, h, mi in (slot_hm(s) for s in sorted(cfg["slots"])))

    rule_file = PROJECTS_ROOT.parent / ".claude" / "rules" / "upload-schedule.md"
    rule = rule_file.read_text(encoding="utf-8") if rule_file.exists() else "(không đọc được rule)"
    rule = rule.split("## 3. NGUỒN")[0]  # bỏ list link, giữ nguyên tắc + bảng + số liệu nền

    uploads_txt = "(kênh chưa có token API — không có data thật; phân tích theo baseline + khán giả mục tiêu, ghi rõ điều đó)"
    proj = PROJECTS_ROOT / cfg["project"]
    if (proj / "credentials" / "token.json").exists():
        try:
            from upload_api import get_service  # lazy
            yt = get_service(proj)
            ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
            pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
            items = yt.playlistItems().list(part="contentDetails", playlistId=pl,
                                            maxResults=50).execute().get("items", [])
            ids = ",".join(i["contentDetails"]["videoId"] for i in items)
            vids = yt.videos().list(part="snippet,statistics,status", id=ids).execute()["items"] if ids else []
            now_local = datetime.now(tz)
            lines = []
            for v in vids:
                pub = v["snippet"].get("publishedAt", "")
                if not pub or v["status"].get("privacyStatus") != "public":
                    continue
                t = datetime.fromisoformat(pub.replace("Z", "+00:00")).astimezone(tz)
                age = (now_local - t).days
                views = v.get("statistics", {}).get("viewCount", "0")
                lines.append(f"- {WEEKDAY_VN[t.weekday()]} {t:%d/%m/%Y %H:%M}: {views} views"
                             f" · {age} ngày tuổi · 「{v['snippet']['title'][:45]}」")
            uploads_txt = "\n".join(lines) or "(chưa có video công khai trên kênh)"
        except Exception as e:  # token hỏng/quota — vẫn phân tích được phần baseline
            uploads_txt = f"(lỗi kéo data thật: {e} — phân tích theo baseline, ghi rõ điều đó)"

    prompt = AI_PROMPT_SCHEDULE.format(name=cfg["name"], slots=slots_txt, rule=rule, uploads=uploads_txt)
    p = subprocess.run([claude, "-p", prompt, *_model_args("schedule")], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300, cwd=str(BASE))
    if p.returncode != 0:
        return jsonify({"ok": False, "log": f"AI lỗi:\n{(p.stderr or p.stdout or '').strip()}"})
    report = (p.stdout or "").strip()
    f = save_history(key, "ai-schedule", report + "\n\n---\n```\n" + uploads_txt + "\n```\n", ext="md")
    return jsonify({"ok": True, "log": report + f"\n\n💾 Đã lưu report: {f}"})


@app.post("/api/ai_analyze")
def api_ai_analyze():
    """AI đọc số liệu và trả về phân tích + khuyến nghị.
    Gọi Claude Code headless (`claude -p`) — chạy trên subscription sẵn có, không cần API key."""
    import shutil as _sh
    d = request.json
    claude = _sh.which("claude")
    if not claude:
        return jsonify({"ok": False, "log": "Không tìm thấy claude CLI trên PATH"}), 500

    # 1. Gom số liệu tươi bằng engine
    if d.get("video"):
        ok, data = run_tool("analytics_report.py", "--channel", d["channel"], "--video", d["video"])
        prompt = AI_PROMPT_VIDEO.format(data=data)
    else:
        ok, data = run_tool("analytics_report.py", "--channel", d["channel"], "-n", "15")
        prompt = AI_PROMPT_CHANNEL.format(data=data)
    if not ok:
        return jsonify({"ok": False, "log": f"Không kéo được số liệu:\n{data}"})

    # 2. Đưa cho AI phân tích (chạy ở BASE để không kéo theo context project khác)
    p = subprocess.run([claude, "-p", prompt, *_model_args("analytics")], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300, cwd=str(BASE))
    if p.returncode != 0:
        return jsonify({"ok": False, "log": f"AI lỗi:\n{(p.stderr or p.stdout or '').strip()}"})
    report = (p.stdout or "").strip()
    kind = f"ai-video-{d['video']}" if d.get("video") else "ai-kenh"
    f = save_history(d["channel"], kind, report + "\n\n---\n<details>số liệu đầu vào</details>\n\n```\n" + data + "\n```\n", ext="md")
    return jsonify({"ok": True, "log": report + f"\n\n💾 Đã lưu report: {f}"})


@app.post("/api/open")
def api_open():
    d = request.json
    what = d.get("what", "pack")
    if what == "studio":
        cfg = _load_bprofiles()
        p = cfg.get("profiles", {}).get(d.get("channel", ""))
        chrome = _chrome_exe(cfg)
        if p and chrome:
            subprocess.Popen([chrome, f"--profile-directory={p['profile_dir']}", "https://studio.youtube.com"])
            return jsonify({"ok": True, "log": f"▶ Studio — Chrome profile riêng 「{p['profile_dir']}」"})
        webbrowser.open("https://studio.youtube.com")
        return jsonify({"ok": True, "log": "▶ Đã mở YouTube Studio (browser mặc định — kênh chưa có profile)"})
    proj = PROJECTS_ROOT / CHANNELS[d["channel"]]["project"]
    vdir = find_video_dir(proj, d["slug"])
    if what == "video":  # icon folder ở tab Chuẩn bị đăng: mở folder video (chứa ảnh nguồn để duyệt)
        target = vdir
        if not target:  # chưa render/fetch → mở folder SCRIPTS chứa script làm fallback
            target = next((sd for sd in sorted(proj.glob("0*_SCRIPTS"))
                           if (sd / f"{d['slug']}.md").exists()), None)
    else:
        target = (vdir / "_upload") if (what == "pack" and vdir) else vdir
    if not target or not target.exists():
        return jsonify({"ok": False, "log": "Không thấy folder (chưa fetch ảnh / chưa render)"}), 404
    if PROJECTS_ROOT not in target.resolve().parents:  # chỉ mở path trong workspace
        return jsonify({"ok": False, "log": "Path ngoài workspace"}), 400
    os.startfile(target)  # noqa — Windows only (dedupe: folder đang mở thì tái dùng cửa sổ)
    import time
    time.sleep(0.6)  # chờ Explorer kịp tạo cửa sổ rồi mới kéo lên trước
    _bring_explorer_front(target.name)
    return jsonify({"ok": True, "log": f"📂 Đã mở {target.name} — không thấy thì nhìn taskbar"})


# ---------- Browser Profiles: mỗi kênh 1 Chrome profile riêng ----------
# Nguồn sự thật mapping: browser_profiles.json (rule: .claude/rules/channel-browser.md)
BPROFILES = BASE / "browser_profiles.json"
CHROME_USER_DATA = Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data"


def _load_bprofiles() -> dict:
    try:
        return json.loads(BPROFILES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"profiles": {}}


def _chrome_exe(cfg: dict) -> str:
    c = cfg.get("chrome_exe", "")
    if c and Path(c).exists():
        return c
    for p in (r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if Path(p).exists():
            return p
    return ""


def _gmail_of_profile(profile_dir: str) -> str:
    """Gmail đang login thật của 1 profile (đọc Local State, readonly) — để đối chiếu với mapping."""
    try:
        ls = json.loads((CHROME_USER_DATA / "Local State").read_text(encoding="utf-8"))
        return ls["profile"]["info_cache"].get(profile_dir, {}).get("user_name", "")
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return ""


@app.get("/api/profiles")
def api_profiles():
    cfg = _load_bprofiles()
    rows = []
    for key, p in sorted(cfg.get("profiles", {}).items()):
        pd = p.get("profile_dir", "")
        rows.append({
            "key": key,
            "channel_name": p.get("channel_name") or CHANNELS.get(key, {}).get("name", key),
            "gmail": p.get("gmail", ""),
            "gmail_live": _gmail_of_profile(pd),
            "profile_dir": pd,
            "exists": (CHROME_USER_DATA / pd).exists() if pd else False,
            "in_channels": key in CHANNELS,
        })
    return jsonify({"chrome": _chrome_exe(cfg), "rows": rows})


@app.post("/api/profile_open")
def api_profile_open():
    d = request.json
    cfg = _load_bprofiles()
    p = cfg.get("profiles", {}).get(d.get("key", ""))
    if not p:
        return jsonify({"ok": False, "log": "Kênh chưa có profile trong mapping"}), 404
    chrome = _chrome_exe(cfg)
    if not chrome:
        return jsonify({"ok": False, "log": "Không tìm thấy chrome.exe"}), 500
    url = d.get("url") or "https://studio.youtube.com"
    if not url.startswith("https://"):
        return jsonify({"ok": False, "log": "URL không hợp lệ"}), 400
    subprocess.Popen([chrome, f"--profile-directory={p['profile_dir']}", url])
    return jsonify({"ok": True, "log": f"▶ Chrome profile 「{p['profile_dir']}」 → {url}"})


def _make_shortcut(chrome: str, prof_dir: str, lnk_name: str) -> bool:
    ps = (
        "$ws = New-Object -ComObject WScript.Shell; "
        "$desktop = [Environment]::GetFolderPath('Desktop'); "
        f"$l = $ws.CreateShortcut(\"$desktop\\{lnk_name}\"); "
        f"$l.TargetPath = '{chrome}'; "
        f"$l.Arguments = '--profile-directory=\"{prof_dir}\" https://studio.youtube.com'; "
        f"$l.WorkingDirectory = '{Path(chrome).parent}'; "
        f"$l.IconLocation = '{chrome},0'; "
        "$l.Save()"
    )
    p = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, timeout=60)
    return p.returncode == 0


@app.post("/api/profile_create")
def api_profile_create():
    """Kênh mới → profile Chrome mới (folder + tên hiển thị + shortcut desktop + mapping).
    Truyền profile_dir = tận dụng profile sẵn có (chỉ đăng ký mapping + shortcut, không tạo folder)."""
    d = request.json
    key = (d.get("key") or "").strip().lower()
    name = (d.get("name") or "").strip() or key
    gmail = (d.get("gmail") or "").strip()
    reuse = (d.get("profile_dir") or "").strip()  # vd "Profile 12" — bỏ trống = tạo mới yt-<key>
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,30}", key):
        return jsonify({"ok": False, "log": "key: chữ thường/số/gạch ngang, 2–31 ký tự"}), 400
    cfg = _load_bprofiles()
    if key in cfg.get("profiles", {}):
        return jsonify({"ok": False, "log": f"Kênh 「{key}」 đã có profile: {cfg['profiles'][key]['profile_dir']}"}), 400
    chrome = _chrome_exe(cfg)
    if not chrome:
        return jsonify({"ok": False, "log": "Không tìm thấy chrome.exe"}), 500

    if reuse:
        if not (CHROME_USER_DATA / reuse).exists():
            return jsonify({"ok": False, "log": f"Profile 「{reuse}」 không tồn tại trong Chrome User Data"}), 400
        prof_dir, created = reuse, "tận dụng profile sẵn có"
    else:
        prof_dir, created = f"yt-{key}", "profile MỚI (mở lần đầu rồi login Gmail kênh)"
        pdir = CHROME_USER_DATA / prof_dir
        if not pdir.exists():
            pdir.mkdir(parents=True)
            (pdir / "Preferences").write_text(
                json.dumps({"profile": {"name": f"YT {name}"}}, ensure_ascii=False), encoding="utf-8")

    lnk = f"YT - {key}.lnk"
    lnk_ok = _make_shortcut(chrome, prof_dir, lnk)
    cfg.setdefault("profiles", {})[key] = {
        "channel_name": name, "gmail": gmail, "profile_dir": prof_dir, "shortcut": lnk}
    cfg.setdefault("chrome_exe", chrome)
    BPROFILES.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    note = "" if lnk_ok else "\n⚠️ Shortcut desktop tạo lỗi — tạo tay sau."
    return jsonify({"ok": True, "log": f"✅ 「{key}」 → profile 「{prof_dir}」 ({created}) + shortcut 「{lnk}」{note}"})


@app.post("/api/profile_edit")
def api_profile_edit():
    """Sửa thông tin hiển thị của 1 profile: channel_name + gmail. GIỮ NGUYÊN profile_dir/shortcut."""
    d = request.json
    key = (d.get("key") or "").strip()
    cfg = _load_bprofiles()
    p = cfg.get("profiles", {}).get(key)
    if not p:
        return jsonify({"ok": False, "log": f"Kênh 「{key}」 không có trong mapping"}), 404
    name = (d.get("channel_name") or "").strip()
    gmail = (d.get("gmail") or "").strip()
    if not name:
        return jsonify({"ok": False, "log": "Tên kênh không được để trống"}), 400
    p["channel_name"], p["gmail"] = name, gmail
    BPROFILES.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return jsonify({"ok": True, "log": f"✏️ Đã cập nhật 「{key}」 → {name} · {gmail or '(chưa có gmail)'}"})


@app.post("/api/profile_del")
def api_profile_del():
    """Gỡ 1 profile KHỎI MAPPING (browser_profiles.json). GIỮ NGUYÊN folder Chrome + shortcut desktop."""
    d = request.json
    key = (d.get("key") or "").strip()
    cfg = _load_bprofiles()
    if key not in cfg.get("profiles", {}):
        return jsonify({"ok": False, "log": f"Kênh 「{key}」 không có trong mapping"}), 404
    pdir = cfg["profiles"].pop(key).get("profile_dir", "")
    BPROFILES.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    warn = "\n⚠️ Kênh này còn trong CHANNELS (đang sản xuất) — mất mapping thì --open không tự mở đúng profile." \
        if key in CHANNELS else ""
    return jsonify({"ok": True, "log": f"🗑️ Đã gỡ 「{key}」 khỏi mapping (folder 「{pdir}」 + shortcut vẫn giữ).{warn}"})


# ───────────────────── PENDING: bài chuẩn bị đăng (script + slide, chưa upload) ─────────────────────
def _script_title(md_path: Path) -> str:
    """Lấy tiêu đề = heading '# ...' đầu tiên; không có thì lấy tên slug."""
    try:
        for line in md_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if s.startswith("# "):
                return s[2:].strip()
    except OSError:
        pass
    return md_path.stem


def _count_json_list(p: Path) -> int:
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return len(data) if isinstance(data, list) else 0
    except (OSError, json.JSONDecodeError):
        return 0


def _pending_scripts(proj: Path) -> list:
    """Mọi script .md trong 0*_SCRIPTS/ CHƯA nằm trong 07_UPLOADED/ = bài chuẩn bị đăng."""
    uploaded = set()
    up = proj / "07_UPLOADED"
    if up.is_dir():
        uploaded = {x.name for x in up.iterdir() if x.is_dir()}
    rows, seen = [], set()
    for sd in sorted(proj.glob("0*_SCRIPTS")):
        for f in sorted(sd.glob("*.md")):
            low = f.name.lower()
            if f.name.startswith("_") or "_tts" in low or "legacy" in low or "proof" in low:
                continue
            slug = f.stem
            if slug in seen or slug in uploaded:
                continue
            seen.add(slug)
            slides = sorted(sd.glob(f"{slug}_SLIDES_*.json"))
            rows.append({
                "slug": slug,
                "title": _script_title(f),
                "has_tts": (sd / f"{slug}_TTS.md").exists(),
                "n_slides": _count_json_list(slides[0]) if slides else 0,
                "slide_files": [s.name for s in slides],
                "has_video": bool(find_video_dir(proj, slug)),
            })
    return rows


@app.get("/api/pending")
def api_pending():
    out = []
    for key, cfg in CHANNELS.items():
        proj = PROJECTS_ROOT / cfg["project"]
        items = _pending_scripts(proj)
        out.append({"key": key, "name": cfg["name"], "count": len(items), "items": items})
    return jsonify(out)


def _preview_dir(proj: Path, slug: str) -> Path | None:
    """Folder ảnh NGUỒN sẽ ghép vào video (slides_img_photo/slide_NN.jpg) — có TRƯỚC render,
    để duyệt trước. Fallback: slides_img (một số video dùng png)."""
    vdir = find_video_dir(proj, slug)
    if not vdir:
        return None
    for name in ("slides_img_photo", "slides_img"):
        d = vdir / name
        if d.is_dir() and any(d.glob("slide_*.*")):
            return d
    return None


def _slides_json_items(scripts_dir: Path, slug: str) -> list:
    """Câu match theo thứ tự slide (để chú thích ảnh khi duyệt)."""
    for sf in sorted(scripts_dir.glob(f"{slug}_SLIDES_*.json")):
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            return []
    return []


@app.get("/api/pending_detail")
def api_pending_detail():
    key, slug = request.args.get("channel", ""), request.args.get("slug", "")
    if key not in CHANNELS:
        return jsonify({"error": "kênh không tồn tại"}), 404
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    md = None
    tts_txt = tts_file = ""
    slide_items = []
    for sd in sorted(proj.glob("0*_SCRIPTS")):
        f = sd / f"{slug}.md"
        if f.exists():
            md = f
            t = sd / f"{slug}_TTS.md"
            if t.exists():
                tts_file, tts_txt = t.name, t.read_text(encoding="utf-8", errors="ignore")
            slide_items = _slides_json_items(sd, slug)
            break
    if not md:
        return jsonify({"error": "Không tìm thấy script cho slug này"}), 404
    # Ảnh nguồn để DUYỆT TRƯỚC render (slides_img_photo/slide_NN.*), ghép câu match theo index
    pdir = _preview_dir(proj, slug)
    imgs = []
    if pdir:
        for p in sorted(pdir.glob("slide_*.*")):
            m = re.search(r"slide_(\d+)", p.stem)
            idx = int(m.group(1)) if m else len(imgs)
            it = slide_items[idx] if idx < len(slide_items) else {}
            imgs.append({"file": p.name, "match": it.get("match", ""),
                         "q": it.get("q") or it.get("query", "")})
    vdir = find_video_dir(proj, slug)
    return jsonify({
        "slug": slug, "title": _script_title(md), "script_file": md.name,
        "script": md.read_text(encoding="utf-8", errors="ignore"),
        "tts_file": tts_file, "tts": tts_txt,
        "preview_imgs": imgs, "fetched": bool(imgs), "n_spec": len(slide_items),
        "has_folder": bool(vdir),
    })


@app.get("/api/pending_img")
def api_pending_img():
    """Serve 1 ảnh nguồn (slides_img_photo/slide_NN.jpg|png) để duyệt trước render."""
    key, slug = request.args.get("channel", ""), request.args.get("slug", "")
    fname = request.args.get("file", "")
    if key not in CHANNELS or not re.fullmatch(r"slide_\d+\.(jpg|jpeg|png|webp)", fname, re.I):
        return "", 404
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    pdir = _preview_dir(proj, slug)
    p = (pdir / fname) if pdir else None
    if not p or not p.exists():
        return "", 404
    mt = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return send_file(p, mimetype=mt, max_age=0)


# ───────────────────────── PROJECTS: bảng quản lý dự án/kênh (giai đoạn pivot) ─────────────────────────
# Nguồn sự thật riêng (projects.json) — ĐỘC LẬP với CHANNELS: theo dõi cả kênh ĐANG chạy lẫn kênh
# mới đang rebrand/lên kế hoạch (chưa cấu hình sản xuất). Trạng thái + checklist do user chỉnh (bán tự
# động, lưu file). Signals (profile/token/script/video/uploaded) dò REALTIME từ hệ thống (update tự động).
PROJECTS_FILE = BASE / "projects.json"
PROJ_STATUS = ("active", "rebranding", "planning", "paused")
DEFAULT_CHECKLIST = [
    {"id": "trends", "label": "Đo Google Trends (gprop=youtube) rổ keyword ngách"},
    {"id": "benchmark", "label": "Mổ 3–5 kênh benchmark bằng mắt (title/thumbnail/giờ đăng/tag)"},
    {"id": "identity", "label": "Chốt tên kênh + persona + giọng TTS (voice test)"},
    {"id": "rebrand", "label": "Rebrand/lập kênh trên Studio + cập nhật mapping profile"},
    {"id": "script1", "label": "Script #1", "auto": "has_script"},
]


def _load_projects() -> dict:
    try:
        return json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"projects": []}


def _save_projects(data: dict) -> None:
    PROJECTS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _count_dirs(parent: Path) -> int:
    """Đếm folder con "thật" (bỏ folder _upload/_scripts... bắt đầu bằng _)."""
    if not parent.is_dir():
        return 0
    return sum(1 for x in parent.iterdir() if x.is_dir() and not x.name.startswith("_"))


def _count_rendered(parent: Path) -> int:
    """Đếm video ĐÃ RENDER = folder con có ít nhất 1 .mp4 (kể cả trong _upload/).

    Bẫy đã gặp 2026-07-26 (kaigo): folder 06_VIDEO/<slug>/ chỉ chứa genten/ (ảnh 原典 chụp
    lúc viết script, chưa render) mà _count_dirs đã tính là "có video" → checklist tự tick
    "Render video #1" khi chưa render. Signal video phải bám vào FILE mp4, không bám folder.
    """
    if not parent.is_dir():
        return 0
    n = 0
    for x in parent.iterdir():
        if x.is_dir() and not x.name.startswith("_") and next(x.rglob("*.mp4"), None):
            n += 1
    return n


def _project_signals(p: dict) -> dict:
    """Dò trạng thái THẬT từ hệ thống cho 1 project (update tự động)."""
    repo = (p.get("repo") or "").strip()
    proj = PROJECTS_ROOT / repo if repo else None
    scripts = videos = uploaded = 0
    repo_exists = bool(proj and proj.is_dir())
    if repo_exists:
        for d in proj.glob("0*_SCRIPTS"):  # repo dùng số khác nhau (03_/04_SCRIPTS)
            scripts += sum(1 for f in d.glob("*.md")
                           if not f.name.startswith("_") and "_TTS" not in f.name)
        for d in proj.glob("0*_VIDEO"):
            videos += _count_rendered(d)  # đếm theo file .mp4, KHÔNG theo folder (xem _count_rendered)
        uploaded = _count_dirs(proj / "07_UPLOADED")
    has_token = bool(proj and (proj / "credentials" / "token.json").exists())
    pd = (p.get("profile_dir") or "").strip()
    profile_exists = bool(pd) and (CHROME_USER_DATA / pd).exists()
    return {
        "repo_exists": repo_exists, "scripts": scripts, "videos": videos, "uploaded": uploaded,
        "has_token": has_token, "profile_exists": profile_exists,
        "gmail_live": _gmail_of_profile(pd) if pd else "",
        "has_script": scripts >= 1, "has_video": videos >= 1, "has_upload": uploaded >= 1,
    }


@app.get("/api/projects")
def api_projects():
    data = _load_projects()
    out = []
    for p in data.get("projects", []):
        sig = _project_signals(p)
        ticks = set(p.get("done_ticks", []))
        items, done_n = [], 0
        for it in p.get("checklist", []):
            auto = it.get("auto")
            auto_done = bool(auto and sig.get(auto))
            done = auto_done or (it["id"] in ticks)
            done_n += done
            items.append({"id": it["id"], "label": it["label"],
                          "done": done, "auto_done": auto_done, "auto": bool(auto)})
        base = {k: v for k, v in p.items() if k not in ("checklist", "done_ticks")}
        gmail_mismatch = bool(p.get("gmail") and sig["gmail_live"] and p["gmail"] != sig["gmail_live"])
        in_ch = p["key"] in CHANNELS
        proj_slots = [list(s) for s in (p.get("slots") or [])]
        if in_ch:  # kênh trong CHANNELS: lịch rule là mặc định, projects.json (nếu có) OVERRIDE
            c = CHANNELS[p["key"]]
            default_slots = [list(s) for s in c["slots"]]
            sched = {"slots": proj_slots or default_slots, "tz": c["tz"], "tz_name": c["tz_name"],
                     "editable": True, "source": "override" if proj_slots else "rule",
                     "default_slots": default_slots}
        else:  # kênh mới → lịch đặt tay trong projects.json
            sched = {"slots": proj_slots, "tz": p.get("tz", 9), "tz_name": p.get("tz_name", "JST"),
                     "editable": True, "source": "project", "default_slots": []}
        out.append({**base, "signals": sig, "checklist": items,
                    "gmail_mismatch": gmail_mismatch, "in_channels": in_ch, "sched": sched,
                    "progress": [done_n, len(items)]})
    rank = {s: i for i, s in enumerate(PROJ_STATUS)}
    out.sort(key=lambda p: (rank.get(p.get("status"), 9), p.get("wave", 9), p.get("key", "")))
    return jsonify(out)


@app.post("/api/project_set")
def api_project_set():
    """Bán tự động: đổi trạng thái / tick checklist tay / sửa ghi chú. Lưu vào projects.json."""
    d = request.json
    data = _load_projects()
    p = next((x for x in data.get("projects", []) if x["key"] == d.get("key")), None)
    if not p:
        return jsonify({"error": "project không tồn tại"}), 404
    if "status" in d:
        if d["status"] not in PROJ_STATUS:
            return jsonify({"error": "status không hợp lệ"}), 400
        p["status"] = d["status"]
        if p["key"] in CHANNELS:  # đồng bộ: paused = tắt kênh khỏi lịch/scan (channels_state.json)
            try:
                cs = json.loads(CHSTATE.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                cs = {}
            cs.setdefault(p["key"], {})["active"] = (d["status"] != "paused")
            CHSTATE.write_text(json.dumps(cs, ensure_ascii=False, indent=1), encoding="utf-8")
    if "tick" in d:  # {tick: <checklist id>, on: bool}
        ticks = set(p.get("done_ticks", []))
        ticks.add(d["tick"]) if d.get("on") else ticks.discard(d["tick"])
        p["done_ticks"] = sorted(ticks)
    if "note" in d:
        p["note"] = str(d["note"])[:600]
    _save_projects(data)
    return jsonify({"ok": True})


@app.post("/api/project_add")
def api_project_add():
    """Thêm project mới vào bảng quản lý (chỉ ghi projects.json — KHÔNG tạo repo/profile)."""
    d = request.json
    key = (d.get("key") or "").strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", key):
        return jsonify({"error": "key: chữ thường/số/gạch ngang, 2–41 ký tự"}), 400
    data = _load_projects()
    if any(x["key"] == key for x in data.get("projects", [])):
        return jsonify({"error": f"đã có project 「{key}」"}), 400
    status = d.get("status", "planning")
    if status not in PROJ_STATUS:
        status = "planning"
    data.setdefault("projects", []).append({
        "key": key,
        "name_new": (d.get("name_new") or "").strip() or key,
        "niche_vn": (d.get("niche_vn") or "").strip(),
        "market": (d.get("market") or "JP").strip().upper()[:4],
        "repo": (d.get("repo") or "").strip(),
        "profile_dir": (d.get("profile_dir") or "").strip(),
        "gmail": (d.get("gmail") or "").strip(),
        "old_name": (d.get("old_name") or "").strip(),
        "wave": int(d.get("wave") or 0),
        "status": status,
        "note": (d.get("note") or "").strip()[:600],
        "checklist": [] if d.get("no_checklist") else [dict(c) for c in DEFAULT_CHECKLIST],
        "done_ticks": [],
    })
    _save_projects(data)
    return jsonify({"ok": True})


@app.post("/api/project_schedule")
def api_project_schedule():
    """Đặt/sửa lịch đăng (thứ trong tuần + 1 giờ cố định, giờ địa phương thị trường) cho MỌI kênh.
    Kênh mới → hiện khung 'dự kiến' trên Lịch đăng. Kênh trong CHANNELS → lịch này OVERRIDE lịch
    rule (upload_pack.py). weekdays rỗng = xóa lịch/về mặc định rule (nút ↺)."""
    d = request.json
    data = _load_projects()
    p = next((x for x in data.get("projects", []) if x["key"] == d.get("key")), None)
    if not p:
        return jsonify({"error": "project không tồn tại"}), 404
    days = d.get("weekdays") or []  # 0=T2 .. 6=CN
    if not (isinstance(days, list) and all(isinstance(x, int) and 0 <= x <= 6 for x in days)):
        return jsonify({"error": "weekdays sai (list 0=T2..6=CN)"}), 400
    if days:
        try:
            hour = int(d.get("hour"))
            minute = int(d.get("minute") or 0)  # giờ lẻ phút (vd 17:30) — mặc định 0 cho lịch cũ
            assert 0 <= hour <= 23 and 0 <= minute <= 59
        except (TypeError, ValueError, AssertionError):
            return jsonify({"error": "giờ sai (0–23:00–59)"}), 400
        # Phút = 0 → giữ dạng [wd, hour] 2 phần tử như lịch cũ (đỡ đụng dữ liệu đã lưu)
        p["slots"] = [([wd, hour, minute] if minute else [wd, hour]) for wd in sorted(set(days))]
    else:
        p["slots"] = []  # về mặc định: kênh CHANNELS → theo rule; kênh mới → không có lịch
    if p["key"] in CHANNELS:  # tz theo thị trường của kênh (không đổi)
        p["tz"], p["tz_name"] = CHANNELS[p["key"]]["tz"], CHANNELS[p["key"]]["tz_name"]
    else:
        mkt = (p.get("market") or "JP").upper()
        p["tz"], p["tz_name"] = {"JP": (9, "JST"), "KR": (9, "KST"),
                                 "VN": (7, "ICT")}.get(mkt, (p.get("tz", 9), p.get("tz_name", "JST")))
    _save_projects(data)
    return jsonify({"ok": True, "slots": p["slots"]})


@app.post("/api/project_del")
def api_project_del():
    """Xóa 1 project khỏi bảng quản lý (chỉ gỡ khỏi projects.json — KHÔNG đụng repo/file thật)."""
    d = request.json
    data = _load_projects()
    n = len(data.get("projects", []))
    data["projects"] = [x for x in data.get("projects", []) if x["key"] != d.get("key")]
    if len(data["projects"]) == n:
        return jsonify({"error": "project không tồn tại"}), 404
    _save_projects(data)
    return jsonify({"ok": True})


@app.post("/api/proj_open")
def api_proj_open():
    """Mở Studio (Chrome theo profile_dir của project) hoặc mở folder repo — dùng profile_dir
    trực tiếp vì key project mới (suimin-rekishi…) khác key mapping cũ (chouhen…)."""
    d = request.json
    data = _load_projects()
    p = next((x for x in data.get("projects", []) if x["key"] == d.get("key")), None)
    if not p:
        return jsonify({"ok": False, "log": "project không tồn tại"}), 404
    if d.get("what") == "repo":
        repo = (p.get("repo") or "").strip()
        target = PROJECTS_ROOT / repo if repo else None
        if not target or not target.exists():
            return jsonify({"ok": False, "log": "Repo chưa tồn tại trên ổ đĩa"}), 404
        os.startfile(target)  # noqa — Windows
        import time
        time.sleep(0.6)
        _bring_explorer_front(target.name)
        return jsonify({"ok": True, "log": f"📂 Đã mở {target.name} — không thấy thì nhìn taskbar"})
    pd = (p.get("profile_dir") or "").strip()
    if not pd:
        return jsonify({"ok": False, "log": "Project chưa gán Chrome profile"}), 400
    chrome = _chrome_exe(_load_bprofiles())
    if not chrome:
        return jsonify({"ok": False, "log": "Không tìm thấy chrome.exe"}), 500
    subprocess.Popen([chrome, f"--profile-directory={pd}", "https://studio.youtube.com"])
    return jsonify({"ok": True, "log": f"▶ Studio — Chrome profile 「{pd}」"})


if __name__ == "__main__":
    threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    print(f"🎬 YT Dashboard — http://127.0.0.1:{PORT}  (Ctrl+C để tắt)")
    app.run(host="127.0.0.1", port=PORT, debug=False)
