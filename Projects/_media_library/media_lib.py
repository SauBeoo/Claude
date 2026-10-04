# -*- coding: utf-8 -*-
"""media_lib.py — Kho media dùng chung mọi kênh (clips + photos).

Nguồn sự thật về chính sách: E:\\Claude\\.claude\\rules\\media-library.md
Nguyên tắc: mọi tool fetch CHECK KHO TRƯỚC (search) → thiếu mới tải →
tải xong nhập kho (add_file). File trong kho và trong folder video là
HARDLINK cùng inode (NTFS, cùng ổ E:) → không tốn thêm dung lượng.

Dùng như module:
    sys.path.insert(0, r"E:\\Claude\\Projects\\_media_library")
    import media_lib
    hits = media_lib.search("corn kernels closeup", kind="photo",
                            unused_for="youtube-jp-health")
    media_lib.link_out(hits[0]["name"], dest_path)
    media_lib.mark_used(hits[0]["name"], "youtube-jp-health/07_xxx")

CLI:
    python media_lib.py search "candle warm" --kind clip [--unused-for <kênh>]
    python media_lib.py ingest-manifest <MANIFEST.json> <clips_dir> --used-by <kênh>/<video>
    python media_lib.py ingest-bg <bg_dir> --channel <kênh> [--usage-log <USAGE.log>]
    python media_lib.py ingest-photos <slides_dir> <SLIDES.json> --used-by <kênh>/<video>
    python media_lib.py mark-used <tên file trong kho> <kênh>/<video>
    python media_lib.py stats
"""
import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIB_DIR = Path(__file__).resolve().parent
CLIPS_DIR = LIB_DIR / "clips"
PHOTOS_DIR = LIB_DIR / "photos"
AVATARS_DIR = LIB_DIR / "avatars"  # b-roll người dẫn AI (HeyGen) — kind="avatar"
HANDMADE_DIR = LIB_DIR / "handmade"  # footage TỰ LÀM (tay thật/iPad) — kind="handmade"
INDEX_PATH = LIB_DIR / "INDEX.json"

STOP = {"a", "an", "the", "of", "in", "on", "and", "or", "with", "at", "for",
        "to", "up", "by", "into", "from", "its", "his", "her"}


# ---------------------------------------------------------------- index I/O

def load_index():
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {}


def save_index(idx):
    tmp = INDEX_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(INDEX_PATH)


# ---------------------------------------------------------------- matching

def _tokens(*texts):
    out = set()
    for t in texts:
        if not t:
            continue
        for w in re.split(r"[^0-9a-zA-ZÀ-ɏ]+", str(t).lower()):
            if len(w) >= 2 and w not in STOP:
                out.add(w)
    return out


def _entry_tokens(e):
    return _tokens(*(e.get("queries", []) + e.get("tags", []) + [e.get("title", "")]))


def _is_used(e, channel):
    return any(u.startswith(channel + "/") or u == channel
               for u in e.get("used_in", []))


def search(query, kind=None, unused_for=None, limit=8, min_score=0.5, idx=None):
    """Trả list dict {name, score, used, entry} sort điểm giảm dần,
    cùng điểm thì asset CHƯA dùng (trong kênh unused_for) đứng trước."""
    idx = idx if idx is not None else load_index()
    qtok = _tokens(query)
    if not qtok:
        return []
    hits = []
    for name, e in idx.items():
        if kind and e.get("kind") != kind:
            continue
        sc = len(qtok & _entry_tokens(e)) / len(qtok)
        if sc < min_score:
            continue
        used = _is_used(e, unused_for) if unused_for else False
        hits.append({"name": name, "score": round(sc, 3), "used": used, "entry": e})
    hits.sort(key=lambda h: (-h["score"], h["used"]))
    return hits[:limit]


# ---------------------------------------------------------------- file ops

def link_or_copy(src, dest):
    """Hardlink (0 byte thêm); fail (khác ổ/FS lạ) thì copy."""
    src, dest = Path(src), Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        if dest.stat().st_size == src.stat().st_size:
            return dest  # coi như cùng file rồi
        dest.unlink()
    try:
        os.link(src, dest)
    except OSError:
        shutil.copy2(src, dest)
    return dest


def _slug(text, maxlen=20):
    s = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^0-9a-zA-Z]+", "-", s.lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "asset"


def _kind_dir(kind):
    if kind == "clip":
        return CLIPS_DIR
    if kind == "avatar":
        return AVATARS_DIR
    if kind == "handmade":
        return HANDMADE_DIR
    return PHOTOS_DIR


def find_by_source(source, source_id, idx=None):
    idx = idx if idx is not None else load_index()
    for name, e in idx.items():
        if e.get("source") == source and str(e.get("source_id")) == str(source_id):
            return name
    return None


def add_file(src_path, kind, source="pexels", source_id="", url="", query="",
             title="", tags=None, license="Pexels License", width=0, height=0,
             duration=0, used_by=None, name=None, idx=None, autosave=True):
    """Nhập 1 file vào kho (hardlink, không di chuyển file gốc).
    Dedup theo (source, source_id): đã có → chỉ merge query/tags. Trả tên trong kho."""
    idx = idx if idx is not None else load_index()
    src_path = Path(src_path)
    ext = src_path.suffix.lower()
    source_id = str(source_id) if source_id else src_path.stem

    exist = find_by_source(source, source_id, idx) if source_id else None
    if exist:
        e = idx[exist]
        if query and query not in e.setdefault("queries", []):
            e["queries"].append(query)
        for t in (tags or []):
            if t not in e.setdefault("tags", []):
                e["tags"].append(t)
        if used_by and used_by not in e.setdefault("used_in", []):
            e["used_in"].append(used_by)
        if autosave:
            save_index(idx)
        return exist

    if not name:
        name = f"{_slug(query or title)}_{source_id}{ext}"
    lib_path = _kind_dir(kind) / name
    if not lib_path.exists():
        link_or_copy(src_path, lib_path)
    idx[name] = {
        "kind": kind, "source": source, "source_id": source_id, "url": url,
        "license": license, "title": title or "", "queries": [query] if query else [],
        "tags": tags or [], "width": width, "height": height,
        "duration": duration, "used_in": [used_by] if used_by else [],
        "added": date.today().isoformat(),
    }
    if autosave:
        save_index(idx)
    return name


def link_out(name, dest, used_by=None, idx=None):
    """Lấy asset từ kho ra folder video (hardlink) + tùy chọn mark used."""
    idx = idx if idx is not None else load_index()
    e = idx.get(name)
    if not e:
        raise KeyError(f"không có trong kho: {name}")
    src = _kind_dir(e["kind"]) / name
    link_or_copy(src, dest)
    if used_by:
        mark_used(name, used_by, idx=idx)
    return dest


def mark_used(name, channel_video, idx=None, autosave=True):
    idx = idx if idx is not None else load_index()
    e = idx.get(name)
    if e is not None and channel_video not in e.setdefault("used_in", []):
        e["used_in"].append(channel_video)
        if autosave:
            save_index(idx)


# ---------------------------------------------------------------- ingest

def ingest_manifest(manifest_path, clips_dir, used_by):
    """Kiểu co-dai: MANIFEST.json {'00': {pexels_id,url,query,duration,w,h}} + clip_XX.mp4."""
    idx = load_index()
    mf = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    n = 0
    for k, m in mf.items():
        if not m:
            continue
        f = Path(clips_dir) / f"clip_{k}.mp4"
        if not f.exists():
            continue
        add_file(f, "clip", source="pexels", source_id=m.get("pexels_id"),
                 url=m.get("url", ""), query=m.get("query", ""),
                 width=m.get("width", 0), height=m.get("height", 0),
                 duration=m.get("duration", 0), used_by=used_by,
                 idx=idx, autosave=False)
        n += 1
    save_index(idx)
    print(f"ingest-manifest: {n} clip ← {clips_dir}")


def ingest_bg(bg_dir, channel, usage_log=None, sources_md=None):
    """Kiểu _bg chouhen/kr: <mood>_<id>.mp4 hoặc <id>.mp4; tags = prefix mood;
    used_in đọc từ USAGE.log (tab: date, video, clip1,clip2,...)."""
    idx = load_index()
    bg_dir = Path(bg_dir)
    usage = {}  # clip filename -> set(video slug)
    log = Path(usage_log) if usage_log else bg_dir / "USAGE.log"
    if log.exists():
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                for c in parts[2].split(","):
                    usage.setdefault(c.strip(), set()).add(parts[1].strip())
    # query gốc từ SOURCES.md (kr ghi query từng clip) — best effort
    srcq = {}
    smd = Path(sources_md) if sources_md else bg_dir / "SOURCES.md"
    if smd.exists():
        for line in smd.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.search(r"`(\S+?\.mp4)`.*?query \"([^\"]+)\"", line)
            if m:
                srcq[m.group(1)] = m.group(2)
    n = 0
    for f in sorted(bg_dir.glob("*.mp4")):
        stem = f.stem
        m = re.match(r"([a-zA-Z]+[a-zA-Z0-9]*?)_?(\d+)$", stem)
        mood, sid = (m.group(1), m.group(2)) if m and m.group(1) else ("", stem)
        if not m:
            sid = stem
        first_used = sorted(usage.get(f.name, set()))
        nm = add_file(f, "clip", source="pexels", source_id=sid,
                      query=srcq.get(f.name, ""), tags=[mood] if mood else [],
                      used_by=None, name=f.name, idx=idx, autosave=False)
        for v in first_used:
            mark_used(nm, f"{channel}/{v}", idx=idx, autosave=False)
        n += 1
    save_index(idx)
    print(f"ingest-bg: {n} clip ← {bg_dir} (usage: {len(usage)} clip có log)")


def ingest_photos(slides_dir, slides_json, used_by):
    """slide_XX.jpg + SLIDES json (q của cùng index) + ATTRIBUTIONS.md (title/license/url)."""
    idx = load_index()
    slides_dir = Path(slides_dir)
    cfg = json.loads(Path(slides_json).read_text(encoding="utf-8"))
    attrs = {}
    amd = slides_dir / "ATTRIBUTIONS.md"
    if amd.exists():
        for line in amd.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"-\s*slide_(\d+):\s*\"(.*?)\"\s*—\s*(.*?)\s*\((.*?)\)\s*(\S*)", line)
            if m:
                attrs[int(m.group(1))] = {"title": m.group(2), "creator": m.group(3),
                                          "license": m.group(4), "url": m.group(5)}
    prefix = _slug(used_by.split("/")[-1], 24)
    n = 0
    for i, spec in enumerate(cfg):
        f = None
        for ext in (".jpg", ".png"):
            p = slides_dir / f"slide_{i:02d}{ext}"
            if p.exists():
                f = p
                break
        if not f:
            continue
        a = attrs.get(i, {})
        sid_m = re.search(r"(\d{5,})/?\s*$", a.get("url", ""))
        source = "pexels" if "pexels.com" in a.get("url", "") else "stock"
        sid = sid_m.group(1) if sid_m else f"{prefix}-{i:02d}"
        add_file(f, "photo", source=source, source_id=sid, url=a.get("url", ""),
                 query=spec.get("q", ""), title=a.get("title", ""),
                 license=a.get("license", "Pexels License"),
                 used_by=used_by, idx=idx, autosave=False)
        n += 1
    save_index(idx)
    print(f"ingest-photos: {n} ảnh ← {slides_dir}")


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--kind", choices=["clip", "photo"])
    s.add_argument("--unused-for")
    s.add_argument("--min-score", type=float, default=0.5)
    s.add_argument("--limit", type=int, default=8)

    m = sub.add_parser("ingest-manifest")
    m.add_argument("manifest")
    m.add_argument("clips_dir")
    m.add_argument("--used-by", required=True)

    b = sub.add_parser("ingest-bg")
    b.add_argument("bg_dir")
    b.add_argument("--channel", required=True)
    b.add_argument("--usage-log")
    b.add_argument("--sources-md")

    p = sub.add_parser("ingest-photos")
    p.add_argument("slides_dir")
    p.add_argument("slides_json")
    p.add_argument("--used-by", required=True)

    u = sub.add_parser("mark-used")
    u.add_argument("name")
    u.add_argument("channel_video")

    sub.add_parser("stats")

    a = ap.parse_args()
    if a.cmd == "search":
        for h in search(a.query, kind=a.kind, unused_for=a.unused_for,
                        min_score=a.min_score, limit=a.limit):
            flag = "ĐÃ DÙNG" if h["used"] else "chưa dùng"
            e = h["entry"]
            print(f"{h['score']:.2f}  {h['name']}  [{e['kind']}] ({flag}) "
                  f"q={e.get('queries', [])[:2]} tags={e.get('tags', [])}")
    elif a.cmd == "ingest-manifest":
        ingest_manifest(a.manifest, a.clips_dir, a.used_by)
    elif a.cmd == "ingest-bg":
        ingest_bg(a.bg_dir, a.channel, a.usage_log, a.sources_md)
    elif a.cmd == "ingest-photos":
        ingest_photos(a.slides_dir, a.slides_json, a.used_by)
    elif a.cmd == "mark-used":
        mark_used(a.name, a.channel_video)
        print("OK")
    elif a.cmd == "stats":
        idx = load_index()
        clips = [e for e in idx.values() if e["kind"] == "clip"]
        photos = [e for e in idx.values() if e["kind"] == "photo"]
        used = sum(1 for e in idx.values() if e.get("used_in"))
        print(f"kho: {len(clips)} clip + {len(photos)} ảnh = {len(idx)} asset "
              f"({used} đã dùng ít nhất 1 video)")


if __name__ == "__main__":
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    main()
