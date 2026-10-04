# -*- coding: utf-8 -*-
"""patch_archival.py — thay slide bằng clip phim tư liệu trong một project.json.

⚠️ Track slide do import_pipeline sinh ra CÓ CHỒNG LẤN 12 frame giữa hai clip liền
nhau (đó là lớp hoà tan của kênh). Nên KHÔNG được "khoét lỗ" trên timeline: làm vậy
đẻ ra mảnh vụn 0,4s đúng bằng phần chồng lấn. Cách đúng là **thay TRỌN một slide**:
clip tư liệu nhận đúng `from` và `durationInFrames` của slide bị thay ⇒ số entry và
nhịp dựng của bản gốc giữ nguyên tuyệt đối.

Vì độ dài phải khớp slide, tool tự CẮT LẠI footage đúng số giây cần (gọi build_vf
của cut_archival.py) thay vì dùng file đã cắt sẵn.

Chạy nhiều lần cho cùng kết quả: luôn dựng lại từ project.orig.json.

Usage:
  py -3 tools/patch_archival.py --project showa-01-v2 --spec <spec.json>
"""

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
CUT_TOOL = Path(r"E:\Claude\Projects\youtube-jp-showa\tools\cut_archival.py")


def load_cut_tool():
    spec = importlib.util.spec_from_file_location("cut_archival", CUT_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--fade", type=float, default=0.5)
    ap.add_argument("--max-slide", type=float, default=11.0,
                    help="giây — slide dài hơn mức này thì không thay (footage đứng quá lâu)")
    a = ap.parse_args()

    cut = load_cut_tool()
    pdir = ROOT / "projects" / a.project
    pjson, orig = pdir / "project.json", pdir / "project.orig.json"
    if not orig.exists():
        shutil.copy2(pjson, orig)
        print(f"  · lưu bản gốc → {orig.name}")

    proj = json.loads(orig.read_text(encoding="utf-8"))
    fps = proj["meta"]["fps"]
    fade = int(round(a.fade * fps))
    lines = proj["captions"]["lines"]
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    assets = ROOT / "public" / "projects" / a.project / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    track = next(t for t in proj["tracks"] if t["id"] == "trk-slides")
    clips = sorted(track["clips"], key=lambda c: c["from"])

    used, report = set(), []
    for item in spec["cuts"]:
        anchor = int(round(lines[item["line"]]["startMs"] / 1000 * fps))
        # slide đang hiển thị tại mốc câu neo = slide cuối cùng bắt đầu <= anchor
        idx = max(i for i, c in enumerate(clips) if c["from"] <= anchor)
        if idx in used:
            print(f"  ⚠️ {item['id']}: slide {idx} đã bị thay bởi cut khác — bỏ qua")
            continue
        target = clips[idx]
        need = target["durationInFrames"] / fps
        if need > a.max_slide:
            print(f"  ⚠️ {item['id']}: slide {idx} dài {need:.1f}s > trần {a.max_slide}s — bỏ qua")
            continue

        src = Path(item["src"])
        active = cut.ACTIVE.get(src.name)
        if active is None:
            print(f"  ❌ chưa đo vùng ảnh thật cho {src.name}")
            return 2
        out = assets / f"{item['id']}.mp4"
        vf = cut.build_vf(active, float(item.get("ybias", 0.5)), float(item.get("grade", 1.0)))
        r = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", str(item["ss"]),
             "-t", f"{need + 0.2:.3f}", "-i", str(src), "-an", "-vf", vf, "-r", str(fps),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", str(out)],
            capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ cắt {item['id']}: {r.stderr[-250:]}")
            return 3

        # 🔴 GATE: cửa sổ cắt KHÔNG được vắt qua chỗ đổi cảnh của phim gốc.
        # Bẫy đã dính thật (2026-08-17): cắt 866,0s+6,5s cho câu 「あなたが、小学生だった頃の」
        # → 3 giây đầu là học sinh, 3 giây sau phim đã cắt sang mấy bà mặc kimono đi dạo.
        # Soi 1 frame ở giây thứ 2 KHÔNG bắt được — phải để MÁY dò đổi cảnh trên chính clip đã cắt.
        # ⚠️ PHẢI dùng `scdet`, KHÔNG dùng `select=gt(scene,0.35)`. Đã thử và nó IM LẶNG
        # trên đúng ca hỏng: phim 8mm/16mm cũ nhiều hạt, điểm `scene` cực đại chỉ ~0,28
        # nên ngưỡng 0,35 không bao giờ chạm. `scdet=threshold=8` bắt đúng cú cắt ở giây
        # 1,47 (score 10,96). Gate nào chưa thử trên một ca hỏng thật thì coi như chưa có.
        sc = subprocess.run(
            ["ffmpeg", "-v", "info", "-i", str(out), "-vf", "scdet=threshold=8",
             "-f", "null", "-"], capture_output=True, text=True)
        import re as _re
        ts = sorted({round(float(m), 1)
                     for m in _re.findall(r"lavfi\.scd\.time:\s*([\d.]+)", sc.stderr)})
        # gộp các frame liền nhau của cùng một cú cắt
        ts = [t for i, t in enumerate(ts) if i == 0 or t - ts[i - 1] > 0.4]
        if ts:
            # ⚠️ chứ không phải 🔴: cắt trong phim tài liệu là chuyện thường, và đo thật
            # 5/9 clip hiện dùng đều có cắt mà CHỦ THỂ không đổi (phố → phố, học sinh →
            # học sinh). Cái giết là cắt làm ĐỔI CHỦ THỂ (học sinh → mấy bà kimono).
            # ⇒ máy chỉ trỏ chỗ cần soi; việc "chủ thể có đổi không" vẫn phải nhìn.
            print(f"  ⚠️ {item['id']}: phim gốc đổi cảnh ở giây {ts} — SOI 2 frame quanh "
                  f"mốc đó xem CHỦ THỂ có đổi không (đổi thì lệch với lời đọc)")

        used.add(idx)
        clips[idx] = {
            "id": item["id"], "kind": "video",
            "from": target["from"], "durationInFrames": target["durationInFrames"],
            "asset": f"assets/{item['id']}.mp4",
            "trimStartFrames": 0, "fit": "cover", "layout": {},
            "motion": "none",     # phim đã có chuyển động thật — không pan chồng lên
            "speed": 1, "mirror": False, "volume": 0,
            "fadeInFrames": fade, "wipeInFrames": 0, "wipeDir": "left",
            "filter": {},         # grade đã đốt sẵn lúc cắt
        }
        report.append((target["from"] / fps, item["id"], idx, need,
                       lines[item["line"]]["text"], item.get("note", "")))

    track["clips"] = clips
    pjson.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")

    total = proj["timeline"]["durationInFrames"] / fps
    short = [c for c in clips if c["durationInFrames"] < 6 * fps]
    print(f"\n✅ {a.project}: {len(clips)} entry ({len(report)} clip tư liệu thay slide)")
    print(f"   nhịp {len(clips)/(total/60):.1f} hình/phút · entry <6s: {len(short)} "
          f"(bản gốc cũng {len(short)} — patch KHÔNG đổi nhịp)")
    for t, cid, idx, need, text, note in report:
        print(f"   · {int(t//60):02d}:{t%60:04.1f}  {cid:24} thay slide-{idx:<3} {need:4.1f}s")
        print(f"        lời: {text[:44]}")
        print(f"        hình: {note.split('—')[0].strip()[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
