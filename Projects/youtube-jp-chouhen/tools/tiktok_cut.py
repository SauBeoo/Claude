# -*- coding: utf-8 -*-
"""
tiktok_cut.py — AI chọn đoạn hấp dẫn nhất trong video đã render → cắt clip dọc 9:16 cho TikTok
(dẫn traffic về kênh YouTube). User chốt 2026-07-20.

Cách chọn đoạn (AI, claude CLI headless): đọc subs.srt → chọn 2–3 đoạn 45–90s cao trào,
kết thúc NGAY TRƯỚC một cú reveal (cliffhanger) để người xem tò mò đi tìm kênh.
Không lấy đoạn CTA, không spoil twist cuối.

Clip xuất: nền blur 9:16 + video gốc 16:9 ở giữa (giữ nguyên phụ đề đã burn) +
hook text trên đầu + CTA 「続きはYouTubeで【kênh】」 dưới đáy. Kèm TIKTOK.txt (caption + hashtag).

Dùng:
  python tiktok_cut.py <slug> --channel <key>            # tự tìm video trong 0N_VIDEO/ hoặc 07_UPLOADED/
  python tiktok_cut.py <slug> --channel <key> --n 3      # số đoạn muốn cắt
Standalone — mọi kênh gọi bằng đường dẫn tuyệt đối. Được upload_pack.py --done gọi tự động.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOOLS = Path(__file__).parent
sys.path.insert(0, str(TOOLS))
from upload_pack import CHANNELS, PROJECTS_ROOT  # noqa: E402

FONTS = {  # font đậm theo ngôn ngữ overlay
    "jp": "C:/Windows/Fonts/YuGothB.ttc",
    "kr": "C:/Windows/Fonts/malgunbd.ttf",
    "vn": "C:/Windows/Fonts/segoeuib.ttf",
}
CTA_TEXT = {
    "jp": "続きは YouTube【{name}】で",
    "kr": "전체 이야기는 유튜브 【{name}】에서",
    "vn": "Xem full trên YouTube【{name}】",
}


def channel_display_name(channel: str) -> str:
    """Tên kênh THẬT để in lên CTA — ưu tiên browser_profiles.json (tên user chốt),
    fallback CHANNELS[name] (một số kênh name config ≠ tên kênh thật, vd health)."""
    try:
        cfg = json.loads((PROJECTS_ROOT / "yt-dashboard" / "browser_profiles.json")
                         .read_text(encoding="utf-8"))
        name = cfg["profiles"][channel].get("channel_name", "")
        if name:
            return name
    except (OSError, KeyError, json.JSONDecodeError):
        pass
    return CHANNELS[channel]["name"]


def find_dirs(proj: Path, slug: str):
    """Tìm folder video của slug trong mọi 0N_VIDEO/ và 07_UPLOADED/ (kho)."""
    hits = []
    for d in sorted(proj.glob("0[0-9]_VIDEO")) + [proj / "07_UPLOADED"]:
        if (d / slug).is_dir():
            hits.append(d / slug)
    return hits


def srt_compact(srt: Path) -> str:
    """Nén srt thành 'H:MM:SS|text' mỗi dòng cho AI đọc (bỏ index + end-time)."""
    out = []
    for block in re.split(r"\n\s*\n", srt.read_text(encoding="utf-8-sig")):
        m = re.search(r"(\d+):(\d+):(\d+)[,.]\d+\s*-->", block)
        if not m:
            continue
        text = " ".join(line.strip() for line in block.splitlines()
                        if line.strip() and "-->" not in line and not line.strip().isdigit())
        out.append(f"{int(m.group(1))}:{m.group(2)}:{m.group(3)}|{text}")
    return "\n".join(out)


def _ai_model_args() -> list:
    """Model do user chọn trên dashboard (ai_models.json key 'tiktok'); không có → mặc định settings máy."""
    try:
        m = json.loads((PROJECTS_ROOT / "yt-dashboard" / "ai_models.json")
                       .read_text(encoding="utf-8")).get("tiktok", "")
        return ["--model", m] if m else []
    except (OSError, json.JSONDecodeError):
        return []


def ai_pick(srt_text: str, channel_name: str, n: int) -> list[dict]:
    """AI chọn n đoạn hấp dẫn nhất. Trả [{start,end,hook,caption}]. Lỗi/không có claude → []."""
    claude = shutil.which("claude")
    if not claude:
        print("⚠️ Không thấy claude CLI — bỏ qua bước AI chọn đoạn.")
        return []
    prompt = f"""Bạn là editor viral TikTok. Dưới đây là phụ đề (H:MM:SS|câu) của một video YouTube dài của kênh 「{channel_name}」.

NHIỆM VỤ: chọn đúng {n} đoạn ĐẮT NHẤT để cắt làm TikTok dẫn người xem đi tìm kênh YouTube. Tiêu chí BẮT BUỘC:
1. Mỗi đoạn 45–90 giây, tự đứng được (người chưa xem vẫn hiểu tình huống trong 5s đầu).
2. Đoạn phải là cao trào/đối đầu/tình tiết sốc, và KẾT THÚC NGAY TRƯỚC một cú reveal hoặc câu trả lời — cắt đúng lúc người xem muốn biết điều gì xảy ra tiếp (cliffhanger). ĐÓ là lý do họ đi tìm kênh.
3. KHÔNG lấy đoạn chứa lời kêu gọi like/comment/đăng ký (高評価/コメント/チャンネル/구독/đăng ký).
4. KHÔNG spoil twist cuối video, không lấy 2 đoạn trùng nội dung.
5. hook: 1 dòng text ngắn (≤14 ký tự CJK hoặc ≤30 ký tự latin, cùng ngôn ngữ với phụ đề) đè lên đầu clip — kiểu giật tít gây tò mò, không spoil.
6. caption: caption đăng TikTok (cùng ngôn ngữ phụ đề, ≤100 ký tự) + 3-4 hashtag phổ biến của ngách.

TRẢ VỀ DUY NHẤT một JSON array, không giải thích:
[{{"start":"H:MM:SS","end":"H:MM:SS","hook":"...","caption":"..."}}]

PHỤ ĐỀ:
{srt_text}"""
    margs = _ai_model_args()
    print(f"🤖 AI đang đọc phụ đề để chọn đoạn đắt nhất (~1-2 phút, model: {margs[1] if margs else 'mặc định'})…")
    p = subprocess.run([claude, "-p", prompt, *margs], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    m = re.search(r"\[.*\]", p.stdout or "", re.S)
    if not m:
        print(f"⚠️ AI không trả JSON hợp lệ:\n{(p.stdout or p.stderr or '')[:500]}")
        return []
    try:
        segs = json.loads(m.group(0))
    except json.JSONDecodeError:
        print("⚠️ JSON của AI parse lỗi — bỏ qua.")
        return []
    ok = [s for s in segs if re.fullmatch(r"\d+:\d\d:\d\d", s.get("start", ""))
          and re.fullmatch(r"\d+:\d\d:\d\d", s.get("end", ""))]
    return ok[:n]


def cut_clip(mp4: Path, seg: dict, out: Path, lang: str, channel_name: str) -> bool:
    """Cắt 1 đoạn → clip dọc 1080x1920: nền blur + khung gốc giữa + hook trên + CTA đáy."""
    font = FONTS.get(lang, FONTS["jp"]).replace(":", r"\:")
    hook_f = out.with_suffix(".hook.txt")
    cta_f = out.with_suffix(".cta.txt")
    hook_f.write_text(seg.get("hook", ""), encoding="utf-8")
    cta_f.write_text(CTA_TEXT.get(lang, CTA_TEXT["jp"]).format(name=channel_name), encoding="utf-8")

    def tf(p: Path) -> str:
        return str(p).replace("\\", "/").replace(":", r"\:")

    vf = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];"
        "[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,"
        f"drawtext=textfile='{tf(hook_f)}':fontfile='{font}':fontsize=72:fontcolor=white:"
        "borderw=4:bordercolor=black:box=1:boxcolor=black@0.45:boxborderw=22:x=(w-text_w)/2:y=200,"
        f"drawtext=textfile='{tf(cta_f)}':fontfile='{font}':fontsize=52:fontcolor=yellow:"
        "borderw=3:bordercolor=black:box=1:boxcolor=black@0.55:boxborderw=18:x=(w-text_w)/2:y=1420"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", seg["start"], "-to", seg["end"],
           "-i", str(mp4), "-filter_complex", vf,
           "-c:v", "libx264", "-preset", "fast", "-crf", "21",
           "-c:a", "aac", "-b:a", "160k", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    hook_f.unlink(missing_ok=True)
    cta_f.unlink(missing_ok=True)
    if p.returncode != 0:
        print(f"⚠️ ffmpeg lỗi đoạn {seg['start']}–{seg['end']}: {(p.stderr or '')[-300:]}")
        return False
    return True


def make_clips(vdir: Path, channel: str, n: int = 3) -> int:
    """Chạy trọn: tìm mp4+srt trong vdir → AI chọn → cắt vào _tiktok/. Trả số clip tạo được."""
    cfg = CHANNELS[channel]
    lang = cfg.get("cta_lang", "jp")
    ch_name = channel_display_name(channel)
    slug = vdir.name
    # tìm mp4: ưu tiên bản gốc <slug>.mp4, rồi mp4 bất kỳ ở gốc, rồi trong _upload
    cands = [vdir / f"{slug}.mp4"] + sorted(vdir.glob("*.mp4"))
    if (vdir / "_upload").exists():
        cands += sorted((vdir / "_upload").glob("*.mp4"))
    mp4 = next((f for f in cands if f.exists()), None)
    srt = next((f for f in [vdir / "subs.srt", vdir / "_upload" / "subs.srt"] if f.exists()), None)
    if not mp4 or not srt:
        print(f"⚠️ {slug}: thiếu {'mp4' if not mp4 else 'subs.srt'} — không cắt TikTok được.")
        return 0
    tkdir = vdir / "_tiktok"
    if tkdir.exists() and any(tkdir.glob("*.mp4")):
        print(f"ℹ️ {slug}: _tiktok/ đã có clip — bỏ qua (xóa folder nếu muốn cắt lại).")
        return len(list(tkdir.glob("*.mp4")))
    segs = ai_pick(srt_compact(srt), ch_name, n)
    if not segs:
        return 0
    tkdir.mkdir(exist_ok=True)
    made, lines = 0, []
    for i, seg in enumerate(segs, 1):
        out = tkdir / f"{slug}_tk{i}.mp4"
        print(f"✂️ Cắt {seg['start']}–{seg['end']} → {out.name}")
        if cut_clip(mp4, seg, out, lang, ch_name):
            made += 1
            lines.append(f"[{out.name}] {seg['start']}–{seg['end']}\n  hook   : {seg.get('hook', '')}\n"
                         f"  caption: {seg.get('caption', '')}\n")
    if made:
        (tkdir / "TIKTOK.txt").write_text(
            f"Clip TikTok dẫn về kênh YouTube 「{ch_name}」 — AI chọn đoạn (tiktok_cut.py)\n"
            f"Đăng kèm link kênh trong bio/comment.\n\n" + "\n".join(lines), encoding="utf-8")
        print(f"✅ {made} clip TikTok → {tkdir} (caption trong TIKTOK.txt)")
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--channel", default="chouhen", choices=sorted(CHANNELS))
    ap.add_argument("--n", type=int, default=3, help="số đoạn muốn cắt (mặc định 3)")
    a = ap.parse_args()
    proj = PROJECTS_ROOT / CHANNELS[a.channel]["project"]
    dirs = find_dirs(proj, a.slug)
    if not dirs:
        sys.exit(f"❌ Không thấy folder video {a.slug} trong {proj}")
    sys.exit(0 if make_clips(dirs[0], a.channel, a.n) else 2)


if __name__ == "__main__":
    main()
