# -*- coding: utf-8 -*-
"""
pipeline_status.py — dashboard trạng thái toàn hệ 6 kênh YouTube (1 lệnh).

Mỗi video xếp vào 1 giai đoạn:
  SCRIPT   — có script (chưa render)
  RENDER…  — folder video có nhưng thiếu mp4/srt
  RENDER ✓ — mp4 + srt xong (chưa đóng gói)
  GÓI SẴN  — _upload/METADATA.txt sẵn sàng kéo thả
  ĐÃ ĐĂNG? — có UPLOADED.txt nhưng CHƯA chuyển kho (chạy upload_pack --done)
(video trong 07_UPLOADED/ = đã đăng, chỉ đếm tổng)

Kèm: lịch slot 7 ngày tới (rule upload-schedule) + đề xuất video nào vào slot nào.

Dùng:
  python tools/pipeline_status.py                    # toàn hệ
  python tools/pipeline_status.py --channel chouhen  # 1 kênh
  python tools/pipeline_status.py --sync             # kênh có token API: đối chiếu video ĐÃ LÊN KÊNH
                                                     # thật, phát hiện quên --done; --sync tự ghi sổ + move
"""
import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent))

from upload_pack import (CHANNELS, PROJECTS_ROOT, VN_TZ, WEEKDAY_VN, find_script,
                         mark_done, parse_ctr, slot_hm, slot_key)

RE_SLUG = re.compile(r"^\d\d_")  # video slug chuẩn: NN_ten-slug


def scan_channel(key: str) -> dict:
    cfg = CHANNELS[key]
    proj = PROJECTS_ROOT / cfg["project"]
    rows, uploaded_count = [], 0

    up_root = proj / "07_UPLOADED"
    uploaded_slugs = {p.name for p in up_root.iterdir() if p.is_dir()} if up_root.is_dir() else set()
    uploaded_count = len(uploaded_slugs)

    seen = set()
    for vdir in sorted(proj.glob("0[0-9]_VIDEO/*/")):
        slug = vdir.name
        if not RE_SLUG.match(slug) or slug.startswith("_"):
            continue
        seen.add(slug)
        mp4 = (vdir / f"{slug}.mp4").exists() or any(
            p.name for p in vdir.glob("*.mp4") if "_test" not in p.name)
        srt = (vdir / "subs.srt").exists() or bool(next(iter(proj.glob(f"0[0-9]_VOICE/{slug}/subs.srt")), None))
        pack = (vdir / "_upload" / "METADATA.txt").exists()
        if (vdir / "UPLOADED.txt").exists():
            stage = "ĐÃ ĐĂNG? (chưa chuyển kho → chạy --done)"
        elif pack:
            stage = "GÓI SẴN"
        elif mp4 and srt:
            stage = "RENDER ✓ (chưa gói)"
        else:
            stage = "RENDER…(dở)"
        rows.append((slug, stage))

    # script có mà chưa render (chưa có folder video, chưa nằm kho)
    for s in sorted(proj.glob("0[0-9]_SCRIPTS/*.md")):
        slug = s.stem
        if RE_SLUG.match(slug) and not slug.endswith("_TTS") \
                and slug not in seen and slug not in uploaded_slugs:
            rows.append((slug, "SCRIPT (chưa render)"))

    return {"key": key, "cfg": cfg, "rows": rows, "uploaded": uploaded_count,
            "uploaded_slugs": sorted(uploaded_slugs)}  # slug đã chuyển kho 07_UPLOADED → dashboard loại khỏi lịch


def upcoming_slots(cfg: dict, days: int = 7) -> list[str]:
    tz = timezone(timedelta(hours=cfg["tz"]))
    now = datetime.now(tz)
    out = []
    for d in range(days):
        day = (now + timedelta(days=d)).date()
        for slot in sorted(cfg["slots"], key=slot_key):
            wd, hour, minute = slot_hm(slot)
            if day.weekday() != wd:
                continue
            t = datetime(day.year, day.month, day.day, hour, minute, tzinfo=tz)
            if t <= now:
                continue
            vn = t.astimezone(timezone(timedelta(hours=VN_TZ)))
            out.append(f"{WEEKDAY_VN[t.weekday()]} {t:%d/%m} {t:%H:%M} {cfg['tz_name']}"
                       + (f" ({vn:%H:%M} VN)" if cfg["tz"] != VN_TZ else ""))
    return out


def sync_channel(key: str, do_move: bool) -> None:
    """Đối chiếu kho local với video THẬT trên kênh (cần credentials/token.json)."""
    cfg = CHANNELS[key]
    proj = PROJECTS_ROOT / cfg["project"]
    if not (proj / "credentials" / "token.json").exists():
        return
    from upload_api import get_service  # lazy: chỉ cần google libs khi sync
    yt = get_service(proj)
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads_pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    titles = []
    resp = yt.playlistItems().list(part="snippet", playlistId=uploads_pl, maxResults=50).execute()
    titles = [it["snippet"]["title"].strip() for it in resp.get("items", [])]

    for vdir in sorted(proj.glob("0[0-9]_VIDEO/*/")):
        slug = vdir.name
        if not RE_SLUG.match(slug):
            continue
        script = find_script(proj, slug)
        if not script:
            continue
        t = (parse_ctr(script.read_text(encoding="utf-8")).get("title") or "").strip()
        if t and any(t == pub or pub.startswith(t[:30]) for pub in titles):
            if do_move:
                print(f"  ↪ {slug}: ĐÃ lên kênh → ghi sổ + chuyển kho")
                mark_done(proj, slug)
            else:
                print(f"  ⚠️ {slug}: title đã XUẤT HIỆN trên kênh nhưng folder còn ở 0N_VIDEO — quên --done? (thêm --sync để tự chuyển)")


def main():
    ap = argparse.ArgumentParser(description="Dashboard pipeline 6 kênh")
    ap.add_argument("--channel", choices=sorted(CHANNELS), help="chỉ xem 1 kênh")
    ap.add_argument("--sync", action="store_true",
                    help="kênh có token: video đã lên kênh thật mà chưa chuyển kho → tự ghi sổ + move")
    ap.add_argument("--check", action="store_true", help="như --sync nhưng CHỈ BÁO, không move")
    a = ap.parse_args()

    keys = [a.channel] if a.channel else sorted(CHANNELS)
    print(f"════ PIPELINE STATUS — {datetime.now():%Y-%m-%d %H:%M} ════")
    for key in keys:
        st = scan_channel(key)
        cfg = st["cfg"]
        print(f"\n▶ {cfg['name']} [{key}] — đã đăng (kho): {st['uploaded']}")
        if not st["rows"]:
            print("   (kho trống — không có video đang làm)")
        for slug, stage in st["rows"]:
            print(f"   {slug:<38} {stage}")
        slots = upcoming_slots(cfg)
        queue = [s for s, stg in st["rows"] if stg.startswith("GÓI SẴN")] + \
                [s for s, stg in st["rows"] if stg.startswith("RENDER ✓")]
        if slots:
            print(f"   Slot 7 ngày tới: {' · '.join(slots)}")
            if queue:
                pair = " · ".join(f"{sl} ← {q}" for sl, q in zip(slots, queue))
                print(f"   Đề xuất: {pair}")
            else:
                print("   ⚠️ Slot sắp tới nhưng KHÔNG có video sẵn — cần render/gói gấp")
        if a.sync or a.check:
            sync_channel(key, do_move=a.sync)


if __name__ == "__main__":
    main()
