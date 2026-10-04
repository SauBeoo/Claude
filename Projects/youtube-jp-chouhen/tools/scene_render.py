# -*- coding: utf-8 -*-
"""scene_render.py v3 — dựng video kênh youtube-jp-chouhen (真夜中の朗読便).

⭐ v3 (user chốt 2026-07-28) — BỎ BOOMERANG, hết cảnh "quay ngược quay xuôi".
   v2 lấy 8 giây đầu clip → ghép xuôi+ngược thành 16s → -stream_loop cho đủ ~95s
   mỗi cảnh ⇒ người xem thấy cùng một cảnh chạy tới-chạy-lui ~6 lần. Rất khó chịu.

2 CHẾ ĐỘ chuẩn (--motion):
  clip  (MẶC ĐỊNH) — mỗi cảnh = clip chạy TRỌN MỘT LẦN XUÔI, không lặp không đảo.
                     Độ dài cảnh = độ dài clip (cắt còn --scene-max nếu dài hơn),
                     clip dài được cắt thành nhiều "take" khác nhau (0-20s, 20-40s…)
                     nên vẫn đủ cảnh mà không phải phát lại cùng một đoạn.
                     Chuyển cảnh = crossfade hoà tan 0.9s như cũ.
  photo           — 100% ẢNH TĨNH (không pan, không zoom — user ghét Ken Burns),
                     mỗi ảnh --photo-sec giây rồi hoà tan sang ảnh sau.
                     Nguồn: 06_VIDEO/_bgphotos/  (python tools/fetch_bg.py --photos "…")
  boomerang       — hành vi v2 cũ, giữ lại để re-render video cũ cho khớp.

CHỐNG KILL RENDER DÀI (máy tự kill ffmpeg chạy >~24'):
- Timeline chia thành NHIỀU PART (~≤22 cảnh / ≤12 phút mỗi part), resumable.
    python tools/scene_render.py <slug> --stage segs    # cắt segment + _render_plan.json
    python tools/scene_render.py <slug> --stage parts   # ghép từng part (skip part đã xong)
    python tools/scene_render.py <slug> --stage final   # audio + concat + mux + CTA
  (bỏ --stage = chạy tuần tự cả 3; --part N để ghép đúng 1 part)
  --stage A / --stage B vẫn nhận (= part 0 / part 1) cho wrapper .cmd cũ.

Input: 06_VIDEO/<slug>/{voice.wav, subs.srt} (output khâu synth ambient_render --voice-only).
"""
import argparse
import datetime
import hashlib
import json
import math
import random
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
W, H, FPS = 1920, 1080, 30
XF = 0.9             # crossfade (giây) giữa 2 cảnh
GRADE = "eq=brightness=-0.10:saturation=0.85,vignette=PI/4.5"   # tông đêm khuya

# --- motion=clip ---
SCENE_MAX = 20.0     # trần độ dài 1 cảnh (clip dài hơn thì cắt thành nhiều take)
SCENE_MIN = 6.0      # đoạn thừa ngắn hơn ngần này thì bỏ, không làm cảnh riêng
# --- motion=photo ---
PHOTO_SEC = 16.0     # ảnh tĩnh hiện bao lâu trước khi hoà tan sang ảnh sau
# --- motion=boomerang (legacy) ---
BM_SRC = 8.0
SCENES_PER_HR = 38
# --- chia part ---
PART_MAX_SEGS = 22
PART_MAX_SEC = 720.0

# ⭐ CỠ CHỮ 45+ (user chốt 2026-08-03: "script ở video phải to để U45 còn dễ nhìn").
# Trước đó FontSize=17 — VI PHẠM `.claude/rules/audience-45plus.md` §3 mục 1 (sàn ≥22 cho
# mọi kênh JP). chouhen bị bỏ sót vì nó dùng renderer riêng, không đi qua channels.py như
# health/co-dai/shokutaku. Đo thật: 17 → dòng 38 ký chỉ chiếm ~1/3 bề ngang khung 1920.
# 28 → ~55%, đọc được trên loa/màn hình điện thoại của tệp nữ 45–70. Nền hộp cũng đục thêm
# (alpha 0x90 ≈ 56% đục → 0x40 ≈ 75% đục) vì rule đòi "nền đục, không chữ trần".
SUB_STYLE = ("FontName=Yu Gothic,FontSize=28,Bold=1,PrimaryColour=&H00FFFFFF,"
             "BackColour=&H40000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=30")

# ⭐ KHUNG "RADIO ĐÊM KHUYA" (--frame radio, user duyệt demo 2026-08-20, học từ format
# đối thủ uWTUB9BIWfk): typing-cam loop góc trái-trên + player UI + avatar (frame_static.png)
# + cột sóng showfreqs sinh THẬT từ voice.wav. Asset: tools/make_radio_frame.py →
# 06_VIDEO/_radio_frame/. Phụ đề đi kèm khung này: chữ XANH viền đen dày, cỡ ~60px,
# style outline (audience-45plus §3.1) — user chọn bản outline, không hộp.
RADIO_DIR = PROJ / "06_VIDEO" / "_radio_frame"
RADIO_CAM_W, RADIO_CAM_H = 705, 352
RADIO_WAVE = (855, 45, 544, 130)         # x, y, w, h — w/h phải CHẴN (libx264+yuv420p)
# FontSize 30 (SỬA 2026-08-27, hạ từ 48 — đo lại bằng máy trên video 35: FontSize=48 khiến
# dòng 42 ký (câu CTA) wrap thành 4 DÒNG, không phải "tối đa 2 dòng" như tin trước đó — filter
# `subtitles=` của ffmpeg này render FontSize KHÔNG map 1:1 px (đo: FontSize 48 → glyph cao
# ~110-130px, không phải ~48px). `original_size` KHÔNG sửa được (đã test, vô tác dụng với SRT).
# Đo thực nghiệm 2 dòng dài nhất kênh (41-42 ký): FontSize 30 là mốc CAO NHẤT còn giữ ≤2 dòng
# cho cả hai — 31-34 vẫn ra 3 dòng. Vi phạm `audience-45plus.md` §3 (≤2 dòng/khối) trước khi sửa:
# 76/481 khối (16%) của video 35 wrap 3 dòng. Đổi số này → chạy lại thử nghiệm đo bằng máy
# (không đoán mắt), KHÔNG chỉ dựa cảm giác "để to cho tệp 45+".
SUB_STYLE_RADIO = ("FontName=Yu Gothic,FontSize=30,Bold=1,PrimaryColour=&H00FFAA48,"
                   "BorderStyle=1,Outline=4,Shadow=0,MarginV=52")

BGM_DIR = PROJ / "06_VIDEO" / "bgm"
BGM_LOG = BGM_DIR / "ROTATION.log"       # dòng: <slug>\t<tên file>


def pick_bgm(slug, arg):
    """--bgm auto → xoay vòng nhạc nền để cả kênh không dùng mãi 1 track.

    Trước 2026-07-30 mọi video dùng đúng `Anguish.mp3` (default hardcode) — nghe 3 video
    liên tiếp là nhận ra ngay cùng một nền, và đúng là dấu hiệu "hàng loạt" YouTube quét.

    Chọn track có lần dùng CŨ NHẤT (chưa dùng thì ưu tiên trước). ⚠️ **Idempotent**: slug đã
    có trong ROTATION.log thì LUÔN trả lại đúng track cũ — render lại / resume không được
    đổi nhạc giữa các part (bài học `render-background.md` §2.5).
    """
    if arg != "auto":
        return PROJ / arg
    tracks = sorted(p for p in BGM_DIR.glob("*.mp3"))
    if not tracks:
        sys.exit(f"[LỖI] không có track nào trong {BGM_DIR} — chạy python tools/bgm_bank.py")
    hist = []
    if BGM_LOG.exists():
        for line in BGM_LOG.read_text(encoding="utf-8").splitlines():
            p = line.split("\t")
            if len(p) >= 2:
                hist.append((p[0], p[1]))
    for s, name in hist:                       # đã chốt track cho slug này rồi
        if s == slug:
            f = BGM_DIR / name
            if f.exists():
                print(f"BGM (đã chốt cho {slug}): {name}")
                return f
    last_use = {}
    for i, (_, name) in enumerate(hist):
        last_use[name] = i
    pick = min(tracks, key=lambda f: (last_use.get(f.name, -1), f.name))
    BGM_LOG.parent.mkdir(parents=True, exist_ok=True)
    with BGM_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{slug}\t{pick.name}\n")
    print(f"BGM (xoay vòng, {len(tracks)} track): {pick.name}")
    return pick


def run(cmd):
    r = subprocess.run(cmd, cwd=PROJ)
    if r.returncode != 0:
        sys.exit(f"[LỖI] lệnh fail: {' '.join(map(str, cmd))}")


def voice_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def snap(sec):
    """Bo về lưới frame — tránh lệch tích luỹ làm xfade cuối bị đứng hình."""
    return round(sec * FPS) / FPS


def read_usage(usage_log, slug):
    used = set()
    if not usage_log.exists():
        return used
    for line in usage_log.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split("\t")
        if len(parts) == 2 and parts[0] != slug:
            used.add(parts[1])
        elif len(parts) >= 3 and parts[1] != slug:
            used.update(parts[2].split(","))
    return used


def dedup_by_source(files, what="asset"):
    """Gộp các file là CÙNG MỘT asset gốc tải trùng dưới nhiều tên (phát hiện 2026-07-30).

    Tên file pool là `<query-slug>_<source_id>.mp4`, nên cùng một clip Pexels tải qua 2 query
    khác nhau ra 2 TÊN khác nhau → không lọc thì renderer coi là 2 clip khác và cho **cùng
    một đoạn phim xuất hiện 2-5 lần trong CÙNG một video** (quét thật: 18 id trùng thành 45
    file, id 31387301 có 5 bản). Đó đúng là thứ YouTube gọi là nội dung lặp, chỉ ở mức nội bộ
    một video — và nó cũng làm sổ `used_in` sai (clip đã lên sóng quay lại dưới tên khác).

    Giữ bản có tên ngắn/sớm nhất theo mỗi source_id; file không có id trong tên thì giữ nguyên.
    Đây là lớp CHẶN LÚC RENDER (không xoá gì) — hàng rào chặn lúc TẢI nằm ở fetch_bg.py.
    """
    seen, out, dropped = {}, [], 0
    for p in files:
        m = re.search(r"_(\d{5,})(?:\.[a-z0-9]+)$", p.name)
        if not m:
            out.append(p)
            continue
        sid = m.group(1)
        if sid in seen:
            dropped += 1
            continue
        seen[sid] = p
        out.append(p)
    if dropped:
        print(f"⚠️ bỏ {dropped} {what} TRÙNG asset gốc (cùng source_id, khác tên) "
              f"— giữ 1 bản/id, tránh lặp hình trong cùng video")
    return out


def pool_files(dirname, patterns, slug, what, howto):
    """Đọc pool asset + LỌC những cái đã bị loại khi duyệt mắt (<pool>/rejected/).

    Bắt buộc lọc: fetch_bg hardlink lại từ kho chung nên tên đã loại VẪN xuất hiện
    trong pool (bug video 09, 2026-07-26). Trả (danh sách đã ưu tiên chưa-dùng, pool_dir).
    """
    d = PROJ / "06_VIDEO" / dirname
    rejected = set()
    for pat in patterns:
        rejected |= {p.name for p in (d / "rejected").glob(pat)}
    files = []
    for pat in patterns:
        files += [p for p in d.glob(pat) if p.name not in rejected]
    files = sorted(set(files))
    if rejected:
        print(f"bỏ qua {len(rejected)} {what} nằm trong {dirname}/rejected/")
    if not files:
        sys.exit(f"[LỖI] 06_VIDEO/{dirname} trống — tải {what}: {howto}")
    files = dedup_by_source(files, what)
    used = read_usage(d / "USAGE.log", slug)
    rng = random.Random(int(hashlib.md5(slug.encode()).hexdigest(), 16))
    fresh = [c for c in files if c.name not in used]
    reused = [c for c in files if c.name in used]
    rng.shuffle(fresh)
    rng.shuffle(reused)
    return fresh + reused, d


# ---------- phụ đề: cắt theo mốc từng part ----------

def _parse_ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def _fmt_ts(t):
    if t < 0:
        t = 0
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60); t -= m * 60
    s = int(t); ms = round((t - s) * 1000)
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_srt_parts(src, bounds, vdir):
    """bounds = [t0, t1, …, tN] (N part). Ghi subs_p0.srt… theo thời gian tương đối part."""
    blocks = [b for b in src.read_text(encoding="utf-8").strip().split("\n\n") if b.strip()]
    n = len(bounds) - 1
    buckets = [[] for _ in range(n)]
    for blk in blocks:
        lines = blk.splitlines()
        st, en = [_parse_ts(x.strip()) for x in lines[1].split("-->")]
        text = "\n".join(lines[2:])
        for i in range(n):
            a, b = bounds[i], bounds[i + 1]
            if st < b and en > a:                      # câu chạm part này
                s2, e2 = max(st, a) - a, min(en, b) - a
                if e2 - s2 < 0.12:
                    continue
                buckets[i].append((s2, e2, text))
    counts = []
    for i, items in enumerate(buckets):
        out = []
        for k, (s2, e2, text) in enumerate(items, 1):
            out.append(f"{k}\n{_fmt_ts(s2)} --> {_fmt_ts(e2)}\n{text}")
        (vdir / f"subs_p{i}.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
        counts.append(len(out))
    return counts


# ---------- chọn cảnh ----------

def limit_pool(order, bg_only, bg_limit):
    """Khoá pool về đúng bộ clip của MỘT video (chốt 2026-08-08).

    Mặc định `pool_files` trả cả `_bg/` (hiện 300+ clip) → mỗi video ăn một bộ khác
    nhau và không kiểm soát được. User chốt kiểu dựng "kiếm ~15 clip rồi lặp lại":
      --bg-only <file danh sách tên clip, 1 dòng 1 tên, bỏ qua dòng trống và dòng #>
      --bg-limit N   (lấy N clip đầu của thứ tự đã ưu tiên-chưa-dùng)
    `--bg-only` thắng `--bg-limit`. Không cờ nào = hành vi cũ, không đụng video khác.
    """
    if bg_only:
        want, seen = [], set()
        for ln in Path(bg_only).read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and ln not in seen:
                want.append(ln)
                seen.add(ln)
        have = {p.name: p for p in order}
        miss = [n for n in want if n not in have]
        if miss:
            sys.exit(f"[LỖI] --bg-only: {len(miss)} clip không có trong pool (hoặc đã bị "
                     f"loại vào _bg/rejected/): {miss[:5]}")
        picked = [have[n] for n in want]
        print(f"pool KHOÁ theo --bg-only: {len(picked)} clip")
        return picked
    if bg_limit and bg_limit < len(order):
        print(f"pool CẮT theo --bg-limit: {bg_limit}/{len(order)} clip")
        return order[:bg_limit]
    return order


def cycle_shuffled(items, key, need, seed):
    """Rút `need` phần tử từ `items`, hết một vòng thì ĐẢO LẠI THỨ TỰ rồi rút tiếp.

    User chốt 2026-08-04: *"hình ảnh và video lặp lại thì đảo nó đi, không được
    để nó cạnh nhau."* Trước đó cả 2 chế độ dùng `items[i % len(items)]` → khi pool
    hết hàng thì phát lại **đúng trình tự cũ**, người nghe nhận ra ngay là vòng lặp.

    Hai bảo đảm:
      1. mỗi vòng mới được shuffle (seed theo slug + số vòng → render lại ra y hệt,
         không phá cơ chế resume của `render-background.md` §2.5);
      2. `key(phần tử đầu vòng mới) != key(phần tử cuối vòng trước)` — hoán với phần
         tử kế trong cùng vòng, nên không bao giờ có 2 cảnh liền nhau cùng nguồn.
    """
    cyc = max(1, math.ceil(need / max(1, len(items))))
    return _spread_all(items, key, need, cyc, random.Random(seed)), cyc


def _spread_all(items, key, need, cycles, rng):
    """Rải `items` (lặp `cycles` lượt) thành chuỗi dài `need`, sao cho:
       ① KHÔNG hai phần tử liền nhau nào cùng key;
       ② hai lần cùng một key cách nhau XA NHẤT có thể, đều trên cả bài.

    🔴 Lịch sử 3 vòng sửa, ghi để không đi lại đường cũ (2026-08-08):
      1. Bản gốc (08-04) chỉ chặn kề nhau ở **ranh giới vòng** rồi `shuffle()` phần
         còn lại → mô phỏng cấu hình video 20 ra **1 chỗ dính ở cảnh 78**.
      2. Sửa lần 1 — greedy "lấy nhóm nhiều phần tử nhất": đạt 0 chỗ kề nhau, NHƯNG
         dồn hai take của cùng clip lại gần nhau (**18/114 lần lặp cách <2 phút**).
      3. Sửa lần 2 — round-robin theo lớp: **tệ hơn nữa** (gần nhất 2 cảnh), vì lớp
         cuối vòng N và lớp đầu vòng N+1 đều bắt đầu bằng đúng nhóm clip dài.
      → Gốc của cả 2 lần hỏng là **chia theo VÒNG**. Bản này bỏ hẳn khái niệm vòng.

    Cách làm: mỗi key có `c` bản trong cả bài thì đặt chúng ở các mốc cách đều
    `N/c` (lệch pha ngẫu nhiên theo key), rồi sắp toàn chuỗi theo mốc. Khoảng cách
    lặp vì thế ≈ N/c ở MỌI chỗ, kể cả chỗ trước đây là mối nối giữa hai vòng.
    Deterministic theo seed → resume ra y hệt (`render-background.md` §2.5).
    """
    groups = {}
    for it in items * cycles:
        groups.setdefault(key(it), []).append(it)
    N = sum(len(g) for g in groups.values())
    marks = []
    for k, insts in sorted(groups.items()):
        # Trong CÙNG một clip: đan xen các ĐOẠN khác nhau (đoạn A, đoạn B, đoạn A…)
        # thay vì xáo ngẫu nhiên → hai lần phát lại **y hệt một đoạn** cách nhau gấp
        # đôi. Không có bước này thì shuffle hay xếp 2 bản cùng đoạn sát nhau.
        by_take = {}
        for it in insts:
            by_take.setdefault(it, []).append(it)
        takes = list(by_take)
        rng.shuffle(takes)
        insts = [by_take[t][i]
                 for i in range(max(len(v) for v in by_take.values()))
                 for t in takes if i < len(by_take[t])]
        u = rng.random()
        step = N / len(insts)
        for j, it in enumerate(insts):
            marks.append(((j + u) * step, rng.random(), k, it))
    marks.sort(key=lambda t: (t[0], t[1]))
    seq = [t[3] for t in marks]
    # chốt chặn cuối: nếu còn chỗ dính thì hoán với phần tử gần nhất khác key
    for i in range(1, len(seq)):
        if key(seq[i]) != key(seq[i - 1]):
            continue
        for j in range(i + 1, len(seq)):
            if key(seq[j]) != key(seq[i]) and (j + 1 >= len(seq) or key(seq[j + 1]) != key(seq[i])):
                seq[i], seq[j] = seq[j], seq[i]
                break
    return seq[:need]


def _spread(items, key, prev, rng):
    """(KHÔNG CÒN DÙNG — giữ lại để tra lịch sử, xem `_spread_all`.)
    Xếp lại `items` sao cho KHÔNG hai phần tử liền nhau nào cùng key.

    🔴 VÁ 2026-08-08. Bản trước chỉ chặn kề nhau ở ĐÚNG MỘT chỗ — phần tử đầu của
    vòng mới so với phần tử cuối vòng trước — rồi `shuffle()` toàn bộ phần còn lại,
    nên hai take của CÙNG một clip vẫn rơi cạnh nhau ở giữa vòng. Mô phỏng đúng cấu
    hình video 20 (15 clip × 3 take, 113 cảnh, 3 vòng) ra **1 chỗ dính ở vị trí 78**.
    Càng ít clip / càng nhiều vòng thì càng dính nhiều — mà "ít clip, lặp nhiều" đúng
    là cách user muốn dựng (chốt 2026-08-08: *"1 cảnh lặp lại không được ở cạnh nhau"*).

    Cách làm: **round-robin có XÁO NHÓM** — mỗi vòng xáo lại thứ tự các clip rồi rải
    take theo lớp (lớp 0 = take đầu của mọi clip, lớp 1 = take thứ hai của những clip
    có, …). Trong một lớp mọi phần tử khác key nên không bao giờ kề nhau; giữa hai lớp
    và giữa hai vòng thì chặn bằng phép hoán ở đầu.

    ⚠️ Bản trung gian (greedy "lấy nhóm nhiều phần tử nhất") đạt 0 chỗ kề nhau NHƯNG
    dồn hai take của cùng một clip lại gần nhau: đo trên video 20 ra **18/114 lần lặp
    cách nhau dưới 2 phút**, gần nhất chỉ 4 cảnh. Round-robin đẩy khoảng cách đó ra
    tối đa — đây là phần "cho người xem dễ chịu", tách khỏi phần "không kề nhau".

    Vẫn xáo theo `rng` (seed = slug + số vòng) nên deterministic → render lại/resume
    ra y hệt, không phá `render-background.md` §2.5.
    """
    groups = {}
    for it in items:
        groups.setdefault(key(it), []).append(it)
    keys = list(groups)
    rng.shuffle(keys)                       # thứ tự clip đổi mỗi vòng
    for k in keys:
        rng.shuffle(groups[k])
    keys.sort(key=lambda k: -len(groups[k]))   # stable → giữ thứ tự vừa xáo trong cùng cỡ
    if prev is not None and len(keys) > 1 and keys[0] == prev:
        keys[0], keys[1] = keys[1], keys[0]    # không nối tiếp phần tử cuối vòng trước
    out = []
    for i in range(max(len(g) for g in groups.values())):
        for k in keys:
            if i < len(groups[k]):
                out.append(groups[k][i])
    return out


def plan_scenes_clip(order, pool_dir, total, scene_max, scene_min, seed=""):
    """Mỗi cảnh = 1 lần chạy XUÔI trọn vẹn của một đoạn clip.

    Clip dài được chia thành nhiều take (0–20s, 20–40s…) → cùng một clip có thể
    xuất hiện lại nhưng là ĐOẠN KHÁC, không phải phát lại y hệt.
    Take của các clip được đan xen (round-robin) để 2 cảnh liền nhau khác clip.
    """
    takes_by_clip, maxrow = [], 0
    for p in order:
        d = probe_dur(pool_dir / p.name)
        if d < scene_min:
            continue
        rows, off = [], 0.0
        while d - off >= scene_min:
            dur = min(scene_max, d - off)
            if 0 < d - off - dur < scene_min:          # đừng để thừa mẩu vụn
                dur = min(d - off, scene_max + scene_min)
            rows.append((p.name, snap(off), snap(dur)))
            off += dur
        if rows:
            takes_by_clip.append(rows)
            maxrow = max(maxrow, len(rows))
        # đủ hàng cho ~1.3× thời lượng thì thôi, khỏi probe cả 235 clip
        if sum(sum(r[2] for r in rs) for rs in takes_by_clip) > total * 1.3:
            break
    if not takes_by_clip:
        sys.exit("[LỖI] không clip nào đủ dài — hạ --scene-min hoặc tải clip mới")
    takes = [rs[i] for i in range(maxrow) for rs in takes_by_clip if i < len(rs)]

    # ước số cảnh cần rồi rút qua cycle_shuffled (vòng lặp lại = đảo thứ tự, không kề nhau)
    avg = sum(t[2] for t in takes) / len(takes)
    need = max(2, math.ceil(total / max(1.0, avg - XF)) + 2)
    seq, cycles = cycle_shuffled(takes, lambda t: t[0], need, seed or "clip")

    scenes, acc, i = [], 0.0, 0
    while acc < total and i < len(seq):
        name, off, dur = seq[i]
        i += 1
        if acc + dur - (XF if scenes else 0) > total:  # cảnh cuối: cắt cho vừa khít
            dur = snap(max(XF + 1.0, total - acc + (XF if scenes else 0)))
        scenes.append({"src": name, "off": off, "dur": dur, "loop": False})
        acc += dur - (XF if len(scenes) > 1 else 0)
    # 🔴 VÁ 2026-08-08 — cảnh CUỐI quá ngắn thì GỘP vào cảnh trước.
    # Nhánh "cắt cho vừa khít" ở trên có sàn XF+1.0 = 1,9s, nên bài nào chia không chẵn
    # cũng kết thúc bằng một cảnh chớp 1,9 giây — đúng vào câu chữ ký đóng bài, và vi
    # phạm `audience-45plus.md` §2 mục 2 ("không entry nào <6 giây"). Đo ở video 20: 1,9s.
    if len(scenes) > 1 and scenes[-1]["dur"] < scene_min:
        tail = scenes.pop()
        prev = scenes[-1]
        prev["dur"] = snap(prev["dur"] + tail["dur"] - XF)   # giữ nguyên tổng thời lượng
        if prev["off"] + prev["dur"] > probe_dur(pool_dir / prev["src"]) + 0.05:
            prev["loop"] = True                              # hết footage thì cho lặp mềm
    reuse = max(0, i - len(takes))
    if reuse:
        print(f"⚠️ pool hết hàng: {reuse}/{i} cảnh là đoạn phát lại — đã ĐẢO thứ tự "
              f"({cycles} vòng) và chặn kề nhau. Muốn hết trùng: fetch_bg query MỚI")
    else:
        print(f"✓ {i} cảnh, KHÔNG cảnh nào phát lại ({len(takes)} take trong pool)")
    return scenes


def plan_scenes_photo(order, total, photo_sec, seed="", inorder=False):
    """inorder=True: MOT anh / MOT canh, DUNG THU TU TEN FILE, khong xao.

    Dung khi anh da duoc gan san cho tung canh cua kich ban (video 38: 289 anh manga
    <-> 289 canh, ban do o IMG_ASSIGN.txt). Mac dinh van la xao nhu cu — khong video
    nao khac bi doi hanh vi.
    """
    if inorder:
        n = len(order)
        L = snap((total + (n - 1) * XF) / n)
        sc, acc = [], 0.0
        for k in range(n):
            dur = L
            if acc + dur - (XF if k else 0) > total:
                dur = snap(max(3.0, total - acc + (XF if k else 0)))
            sc.append({"src": order[k].name, "off": 0.0, "dur": dur,
                       "loop": False, "still": True})
            acc += dur - (XF if k else 0)
        # canh cuoi bu cho khop tron voice
        if acc < total and sc:
            sc[-1]["dur"] = snap(sc[-1]["dur"] + (total - acc))
        return sc
    n = max(2, math.ceil((total - XF) / (photo_sec - XF)))
    seq, cycles = cycle_shuffled(order, lambda p: p.name, n, seed or "photo")
    scenes, acc = [], 0.0
    for k in range(n):
        dur = snap(photo_sec)
        if acc + dur - (XF if k else 0) > total:
            dur = snap(max(3.0, total - acc + (XF if k else 0)))
        scenes.append({"src": seq[k].name, "off": 0.0,
                       "dur": dur, "loop": False, "still": True})
        acc += dur - (XF if k else 0)
        if acc >= total:
            break
    if n > len(order):
        print(f"⚠️ chỉ {len(order)} ảnh cho {n} cảnh — {n - len(order)} lượt dùng lại, "
              f"đã ĐẢO thứ tự ({cycles} vòng) và chặn kề nhau; "
              f"tải thêm: python tools/fetch_bg.py --photos \"<query>\"")
    return scenes


def plan_scenes_boomerang(order, total, n_override):
    n = n_override or max(2, round(total / 3600 * SCENES_PER_HR))
    L = snap((total + (n - 1) * XF) / n)
    return [{"src": order[i % len(order)].name, "off": 0.0, "dur": L, "loop": True}
            for i in range(n)]


# ---------- stages ----------

def stage_segs(vdir, slug, args):
    voice = vdir / "voice.wav"
    subs = vdir / "subs.srt"
    if not voice.exists() or not subs.exists():
        sys.exit(f"[LỖI] thiếu {voice} / {subs} — chạy khâu synth (ambient_render --voice-only) trước")
    # Lớp FX (fx_mix.py, user duyệt 2026-07-22): có <slug>_FX.json → phụ đề màu theo
    # nhân vật (subs_fx.srt) + xuất card PNG + _fx_plan.json cho stage parts/final.
    import fx_mix
    plan_fx = fx_mix.resolve_plan(slug, vdir)
    if plan_fx:
        fx_mix.colorize_srt(plan_fx, subs, vdir / "subs_fx.srt", fx_mix.load_timeline(vdir))
        subs = vdir / "subs_fx.srt"
        cards = fx_mix.render_cards(plan_fx, vdir)
        (vdir / "_fx_plan.json").write_text(json.dumps(
            {"cards": [[str(p), a, b] for p, a, b in cards],
             "vol_expr": plan_fx["vol_expr"],
             "sfx": [[str(f), t, g] for f, t, g in plan_fx["sfx"]]},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"FX: {len(plan_fx['sfx'])} SFX | {len(cards)} card | "
              f"{len(plan_fx['lines'])} câu thoại tô màu")

    total = snap(voice_duration(voice))
    # khung radio: pre-render cột sóng showfreqs thành wave.mp4 MỘT LẦN cho cả video.
    # ⛔ Không đưa showfreqs thẳng vào filtergraph của stage_part — trộn nhánh audio→video
    # với các nhánh video là OOM (đo 2026-08-20: 7GB RAM rồi 'Cannot allocate memory').
    if getattr(args, "frame", "none") == "radio":
        wave = vdir / "wave.mp4"
        if not wave.exists() or wave.stat().st_mtime < voice.stat().st_mtime:
            print("khung radio: dựng wave.mp4 (PIL từ biên độ voice.wav)…")
            # ⛔ KHÔNG dùng ffmpeg showfreqs — leak RAM vô hạn với voice.wav của kênh
            # (đo 2026-08-20: 2,3–7 GB rồi 'Cannot allocate memory', cả khi đứng một mình).
            # make_radio_frame.py wave vẽ PIL theo RMS thật, ghi .tmp rồi rename (chống rác).
            wave_tmp = vdir / "wave.tmp.mp4"
            r = subprocess.run([sys.executable, str(PROJ / "tools" / "make_radio_frame.py"),
                                "wave", str(voice), str(wave_tmp)])
            if r.returncode != 0 or not wave_tmp.exists():
                sys.exit("[LỖI] dựng wave.mp4 fail — xem make_radio_frame.py wave")
            wave_tmp.replace(wave)
    mode = args.motion
    if mode == "photo":
        if args.photo_dir:
            pool_dir = Path(args.photo_dir)
            order = sorted([p for pat in ("*.jpg", "*.jpeg", "*.png")
                            for p in pool_dir.glob(pat)])
            if not order:
                sys.exit(f"[LOI] --photo-dir trong: {pool_dir}")
            print(f"anh tu --photo-dir: {len(order)} file (thu tu TEN, khong xao)")
        else:
            order, pool_dir = pool_files("_bgphotos", ["*.jpg", "*.jpeg", "*.png"], slug,
                                         "ảnh nền", 'python tools/fetch_bg.py --photos "<query>"')
        scenes = plan_scenes_photo(order, total, args.photo_sec, seed=args.slug,
                                   inorder=args.photo_inorder)
    else:
        order, pool_dir = pool_files("_bg", ["*.mp4"], slug,
                                     "clip nền", 'python tools/fetch_bg.py "<query>"')
        order = limit_pool(order, args.bg_only, args.bg_limit)
        if mode == "boomerang":
            scenes = plan_scenes_boomerang(order, total, args.scenes)
        else:
            scenes = plan_scenes_clip(order, pool_dir, total, args.scene_max, args.scene_min, seed=args.slug)

    # chia part (≤PART_MAX_SEGS cảnh và ≤PART_MAX_SEC giây / part)
    parts, cur, cur_dur = [], [], 0.0
    for i, sc in enumerate(scenes):
        add = sc["dur"] - (XF if cur else 0)
        if cur and (len(cur) >= PART_MAX_SEGS or cur_dur + add > PART_MAX_SEC):
            parts.append(cur); cur, cur_dur = [], 0.0
            add = sc["dur"]
        cur.append(i); cur_dur += add
    if cur:
        parts.append(cur)
    # Mối nối GIỮA 2 part là hard-cut (không xfade) → mỗi mối nối cộng thêm XF giây
    # vào timeline so với lúc lập kế hoạch. Bù bằng cách rút cảnh cuối của mỗi part
    # (trừ part cuối) đúng XF giây, để timeline khớp voice thay vì dôi ra.
    for idxs in parts[:-1]:
        sc = scenes[idxs[-1]]
        if sc["dur"] - XF > XF + 1.0:
            sc["dur"] = snap(sc["dur"] - XF)

    seg_dir = vdir / "_seg"
    seg_dir.mkdir(parents=True, exist_ok=True)
    still = mode == "photo"
    print(f"motion={mode} | voice {total:.1f}s → {len(scenes)} cảnh "
          f"({min(s['dur'] for s in scenes):.0f}–{max(s['dur'] for s in scenes):.0f}s/cảnh, "
          f"xfade {XF}s) | {len(parts)} part")

    # ⭐ GHI DANH SÁCH CHỌN NGAY, TRƯỚC KHI CẮT (user bắt lỗi 2026-08-03: "sao không duyệt
    # clip trước khi render đi"). Trước đây `_render_plan.json` chỉ được ghi ở CUỐI stage
    # segs → phải cắt xong 153 segment (~18 phút) mới biết renderer chọn clip nào, mà vòng
    # duyệt bộ CHỌN mới là vòng chặn thật (nó chọn từ CẢ pool, gồm clip cũ chưa ai soi).
    # Ca gốc: video 16 duyệt bộ chọn ra 13 clip phải loại — TẤT CẢ đều là clip tái dùng của
    # video 13/14/15 (két sắt, băng cassette, sóng biển, đan len, bánh mì) → cắt lại từ đầu.
    # Giờ: `--plan-only` dừng ngay sau bước này để duyệt, rồi mới cắt một lần cho sạch.
    #     python tools/scene_render.py <slug> --stage segs --plan-only
    #     python tools/clip_sheet.py picks <slug> -o 06_VIDEO/<slug>/_sheet_picks.jpg
    (vdir / "_picks.json").write_text(json.dumps(
        {"picks": sorted({s["src"] for s in scenes}), "n_scenes": len(scenes),
         "n_parts": len(parts), "total": total, "mode": mode},
        ensure_ascii=False, indent=1), encoding="utf-8")
    if getattr(args, "plan_only", False):
        print(f"--plan-only: DỪNG trước khi cắt. {len({s['src'] for s in scenes})} clip được "
              f"chọn → 06_VIDEO/{vdir.name}/_picks.json\n"
              f"  Duyệt: python tools/clip_sheet.py picks {slug} "
              f"-o 06_VIDEO/{vdir.name}/_sheet_picks.jpg")
        return
    for i, sc in enumerate(scenes):
        # ⚠️ Khoá hash phải mang DANH TÍNH NỘI DUNG, không chỉ tên file (vá 2026-07-29):
        # fetch_bg đặt tên <slug>_<pexels_id>.mp4 và media_lib.link_or_copy coi "cùng size
        # = cùng file" → thay clip cùng tên thì segment cũ vẫn được tái dùng.
        _sp = pool_dir / sc["src"]
        _st = _sp.stat() if _sp.exists() else None
        key = hashlib.md5(
            f"{mode}|{sc['src']}|{sc['off']}|{sc['dur']}"
            f"|{int(_st.st_mtime) if _st else 0}|{_st.st_size if _st else 0}".encode()
        ).hexdigest()[:10]
        sc["seg"] = f"s_{key}.mp4"
        seg = seg_dir / sc["seg"]
        if seg.exists():
            continue
        src = pool_dir / sc["src"]
        frames = max(1, round(sc["dur"] * FPS))
        if sc.get("loop"):        # boomerang legacy: dựng bm 8s xuôi+ngược, part sẽ loop
            vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"fps={FPS},{GRADE},split[a][b];[b]reverse[r];"
                  f"[a][r]concat=n=2:v=1,setpts=PTS-STARTPTS[v]")
            cmd = ["ffmpeg", "-y", "-t", f"{BM_SRC}", "-i", str(src),
                   "-filter_complex", vf, "-map", "[v]"]
        elif still:
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"fps={FPS},{GRADE}")
            cmd = ["ffmpeg", "-y", "-loop", "1", "-i", str(src),
                   "-vf", vf, "-frames:v", str(frames)]
        else:
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"fps={FPS},{GRADE},setpts=PTS-STARTPTS")
            cmd = ["ffmpeg", "-y", "-ss", f"{sc['off']:.3f}", "-i", str(src),
                   "-vf", vf, "-frames:v", str(frames)]
        cmd += ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(args.crf),
                "-pix_fmt", "yuv420p", str(seg), "-loglevel", "error"]
        run(cmd)
        if (i + 1) % 10 == 0 or i + 1 == len(scenes):
            print(f"  segment {i + 1}/{len(scenes)}")

    bounds, t = [0.0], 0.0
    pmeta = []
    for pi, idxs in enumerate(parts):
        pdur = snap(sum(scenes[k]["dur"] for k in idxs) - (len(idxs) - 1) * XF)
        pmeta.append({"i": pi, "idx": idxs, "t0": snap(t), "dur": pdur})
        t = snap(t + pdur)
        bounds.append(t)
    plan = {"mode": mode, "XF": XF, "total": total, "crf": args.crf,
            "frame": getattr(args, "frame", "none"),
            "scenes": scenes, "parts": pmeta,
            "picks": sorted({s["src"] for s in scenes}), "timeline": t}
    (vdir / "_render_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    counts = split_srt_parts(subs, bounds, vdir)
    print(f"segs XONG: {len(scenes)} cảnh | timeline {t/60:.1f} phút (voice {total/60:.1f}) | "
          f"part @ {[f'{b:.0f}s' for b in bounds[1:-1]]} | subs {counts}")


def _xfade_filter(durs, sub_rel, cards=None, card_base_idx=0, sub_style=None, radio=None):
    """Chuỗi xfade cho các input độ dài KHÁC NHAU + burn phụ đề (+ quote card FX).

    radio = {"typing_idx", "static_idx", "audio_idx"} → chèn lớp khung "radio đêm khuya"
    (typing-cam loop + frame_static.png + cột sóng showfreqs từ voice.wav) NGAY SAU lớp
    nền, TRƯỚC phụ đề — để chữ luôn nằm trên cùng, không bị khung đè."""
    m = len(durs)
    parts = [f"[{k}:v]fps={FPS},format=yuv420p,settb=AVTB,setpts=PTS-STARTPTS[v{k}]"
             for k in range(m)]
    if m == 1:
        last = "v0"
    else:
        prev, acc = "v0", durs[0]
        for k in range(1, m):
            out = f"x{k}" if k < m - 1 else "vc"
            parts.append(f"[{prev}][v{k}]xfade=transition=fade:duration={XF}:"
                         f"offset={acc - XF:.3f}[{out}]")
            acc += durs[k] - XF
            prev = out
        last = "vc"
    if radio:
        ti, si, wi = radio["typing_idx"], radio["static_idx"], radio["wave_idx"]
        wx, wy, _, _ = RADIO_WAVE
        # typing-cam: scale về bề ngang khung, crop giữa theo chiều dọc
        parts.append(f"[{ti}:v]scale={RADIO_CAM_W}:-2,"
                     f"crop={RADIO_CAM_W}:{RADIO_CAM_H}:0:(ih-{RADIO_CAM_H})/2,"
                     f"fps={FPS},setpts=PTS-STARTPTS[rcam]")
        parts.append(f"[{last}][rcam]overlay=0:0:eof_action=repeat[rc]")
        # cột sóng: wave.mp4 pre-render ở stage segs (⛔ ĐỪNG đưa showfreqs thẳng vào đây —
        # nhánh audio→video trộn chung filtergraph với các nhánh video là OOM, đo thật
        # 2026-08-20: ffmpeg phình 7GB rồi chết 'Cannot allocate memory'; tách pass thì sạch)
        parts.append(f"[{wi}:v]format=rgba,colorkey=black:0.15:0.05,"
                     f"setpts=PTS-STARTPTS[rwv]")
        parts.append(f"[rc][rwv]overlay={wx}:{wy}:eof_action=pass[rw]")
        # lớp tĩnh (player UI + avatar + viền cam) — 1 PNG, 1 overlay
        parts.append(f"[{si}:v]format=rgba[rst]")
        parts.append(f"[rw][rst]overlay=0:0:eof_action=repeat[rs]")
        last = "rs"
    parts.append(f"[{last}]subtitles={sub_rel}:force_style='{sub_style or SUB_STYLE}'[vs]")
    last = "vs"
    FD = 0.35
    for j, (png, t0, t1) in enumerate(cards or []):
        idx = card_base_idx + j
        parts.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d={FD}:alpha=1,"
                     f"fade=t=out:st={t1 - t0 - FD:.3f}:d={FD}:alpha=1,"
                     f"setpts=PTS-STARTPTS+{t0:.3f}/TB[kc{j}]")
        parts.append(f"[{last}][kc{j}]overlay=0:0:eof_action=pass[vk{j}]")
        last = f"vk{j}"
    parts.append(f"[{last}]null[v]")
    return ";".join(parts)


def stage_part(vdir, pi, crf):
    plan = json.loads((vdir / "_render_plan.json").read_text(encoding="utf-8"))
    if pi >= len(plan["parts"]):
        sys.exit(f"[LỖI] part {pi} không tồn tại (plan có {len(plan['parts'])} part)")
    p = plan["parts"][pi]
    out = vdir / f"v_p{pi}.mp4"
    seg_dir = vdir / "_seg"
    segs = [plan["scenes"][k] for k in p["idx"]]
    # khung radio (đọc từ PLAN, không từ args — một nguồn sự thật; đổi khung → chạy lại segs)
    frame_mode = plan.get("frame", "none")
    r_typing = RADIO_DIR / "typing_loop.mp4"
    r_static = RADIO_DIR / "frame_static.png"
    r_wave = vdir / "wave.mp4"           # pre-render ở stage segs (theo voice của video)
    if frame_mode == "radio":
        missing = [f.name for f in (r_typing, r_static, r_wave) if not f.exists()]
        if missing:
            sys.exit(f"[LỖI] --frame radio nhưng thiếu {missing} — chạy "
                     f"`python tools/make_radio_frame.py assets` + `--stage segs` trước")
    if out.exists():
        # ⚠️ CHỈ exists() LÀ KHÔNG ĐỦ (vá 2026-07-29, cùng họ bẫy chunk ở health).
        # Quy trình trong CLAUDE.md là: clip trượt duyệt mắt → _bg/rejected/ → chạy lại
        # `--stage segs`. Nếu `--stage parts` đã chạy trước đó, v_p<N>.mp4 còn nguyên →
        # skip → clip ĐÃ LOẠI vẫn nằm trong bản final (đúng ca video 09).
        _newer = [s["seg"] for s in segs
                  if (seg_dir / s["seg"]).exists()
                  and (seg_dir / s["seg"]).stat().st_mtime > out.stat().st_mtime]
        # cùng luật cho asset khung radio: đổi avatar/UI/clip typing/sóng → part dựng lại
        if frame_mode == "radio":
            _newer += [f.name for f in (r_typing, r_static, r_wave)
                       if f.stat().st_mtime > out.stat().st_mtime]
        _plan_new = (vdir / "_render_plan.json").stat().st_mtime > out.stat().st_mtime
        if not _newer and not _plan_new:
            print(f"part {pi}: đã có {out.name} — skip (xoá file nếu muốn dựng lại)")
            return
        why = "_render_plan.json mới hơn" if _plan_new else f"{len(_newer)} input mới hơn"
        print(f"part {pi}: {out.name} CŨ ({why}) → dựng lại")
        out.unlink()
    sub_rel = (vdir / f"subs_p{pi}.srt").relative_to(PROJ).as_posix()
    t_off, t_end = p["t0"], p["t0"] + p["dur"]
    cards = []
    fx_plan = vdir / "_fx_plan.json"
    if fx_plan.exists():
        fxp = json.loads(fx_plan.read_text(encoding="utf-8"))
        cards = [(Path(a_p), a - t_off, min(b, t_end) - t_off)
                 for a_p, a, b in fxp.get("cards", []) if t_off <= a < t_end]
    cmd = ["ffmpeg", "-y"]
    for sc in segs:
        if sc.get("loop"):
            cmd += ["-stream_loop", "-1", "-t", f"{sc['dur']:.3f}"]
        cmd += ["-i", str(seg_dir / sc["seg"])]
    for png, a, b in cards:
        cmd += ["-loop", "1", "-t", f"{b - a:.3f}", "-i", str(png)]
    radio = None
    sub_style = SUB_STYLE
    if frame_mode == "radio":
        base = len(segs) + len(cards)
        radio = {"typing_idx": base, "static_idx": base + 1, "wave_idx": base + 2}
        sub_style = SUB_STYLE_RADIO
        cmd += ["-stream_loop", "-1", "-t", f"{p['dur']:.3f}", "-i", str(r_typing),
                "-i", str(r_static),
                "-ss", f"{t_off:.3f}", "-t", f"{p['dur']:.3f}", "-i", str(r_wave)]
    cmd += ["-filter_complex",
            _xfade_filter([s["dur"] for s in segs], sub_rel, cards, card_base_idx=len(segs),
                          sub_style=sub_style, radio=radio),
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
            "-pix_fmt", "yuv420p", str(out), "-loglevel", "error"]
    print(f"part {pi}/{len(plan['parts']) - 1}: {len(segs)} cảnh xfade + {len(cards)} card"
          f"{' + khung radio' if radio else ''} → {out.name} (~{p['dur']/60:.1f} phút)")
    run(cmd)
    print(f"part {pi} XONG → {out}")


def cleanup_tmp(vdir):
    """Xoá file/thư mục trung gian sau khi ra final thành công."""
    import shutil
    tmp = ["video_final.mp4", "audio.m4a", "vlist.txt", "_render_plan.json"]
    tmp += [p.name for p in vdir.glob("v_p*.mp4")]
    tmp += [p.name for p in vdir.glob("subs_p*.srt")]
    tmp += ["vA.mp4", "vB.mp4", "subsA.srt", "subsB.srt"]        # rác bản v2
    freed = 0
    for name in tmp:
        p = vdir / name
        if p.exists():
            freed += p.stat().st_size
            p.unlink()
    for name in ("_seg", "_bm", "_cta"):
        p = vdir / name
        if p.is_dir():
            freed += sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
            shutil.rmtree(p, ignore_errors=True)
    if freed:
        print(f"🧹 dọn file trung gian: giải phóng {freed / 1e9:.2f} GB")


def stage_final(vdir, slug, args):
    plan = json.loads((vdir / "_render_plan.json").read_text(encoding="utf-8"))
    voice = vdir / "voice.wav"
    pfiles = [vdir / f"v_p{p['i']}.mp4" for p in plan["parts"]]
    missing = [f.name for f in pfiles if not f.exists()]
    if missing:
        sys.exit(f"[LỖI] thiếu {', '.join(missing)} — chạy --stage parts trước")
    # 1) audio: voice + BGM -40dB (hoặc no-bgm); có _fx_plan.json → BGM động + SFX
    audio = vdir / "audio.m4a"
    LN = "loudnorm=I=-16:TP=-1.5:LRA=11"   # chuẩn hoá giọng -16 LUFS (user chốt 2026-07-22)
    bgm_sel = pick_bgm(slug, args.bgm)
    fx_plan_p = vdir / "_fx_plan.json"
    if fx_plan_p.exists():
        import fx_mix
        fx_plan = fx_mix.resolve_plan(slug, vdir, args.bgm_gain)
        fx_mix.build_audio(vdir, audio, bgm_sel, args.bgm_gain, fx_plan,
                           no_bgm=args.no_bgm)
        print(f"audio FX: {len(fx_plan['sfx'])} SFX + {len(fx_plan.get('amb', []))} ambience "
              f"+ BGM động")
    elif args.no_bgm:
        run(["ffmpeg", "-y", "-i", str(voice), "-af", LN, "-c:a", "aac", "-b:a", "192k",
             str(audio), "-loglevel", "error"])
    else:
        bgm = bgm_sel
        if not bgm.exists():
            sys.exit(f"[LỖI] không thấy BGM {bgm}")
        fc = (f"[1:a]volume={args.bgm_gain}dB[bg];"
              f"[0:a]{LN}[voc];"
              f"[voc][bg]amix=inputs=2:duration=first:normalize=0[a]")
        run(["ffmpeg", "-y", "-i", str(voice), "-stream_loop", "-1", "-i", str(bgm),
             "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
             "-shortest", str(audio), "-loglevel", "error"])
    # 2) concat các part (-c copy)
    vlist = vdir / "vlist.txt"
    vlist.write_text("".join(f"file '{f.name}'\n" for f in pfiles), encoding="utf-8")
    video_final = vdir / "video_final.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(vlist),
         "-c", "copy", str(video_final), "-loglevel", "error"])
    # 3) mux video + audio
    out = vdir / f"{slug}{args.suffix}.mp4"
    run(["ffmpeg", "-y", "-i", str(video_final), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest",
         str(out), "-loglevel", "error"])
    # 4) hiệu ứng CTA giữa video (rule .claude/rules/cta-midvideo.md)
    if not args.no_cta:
        r = subprocess.run([sys.executable, str(PROJ / "tools" / "cta_inject.py"),
                            str(out), "--srt", str(vdir / "subs.srt"),
                            "--lang", "jp", "--in-place", "--crf", str(args.crf)])
        if r.returncode == 2:
            print("⚠️ script chưa có câu CTA giữa (xem rule cta-midvideo.md) — video giữ nguyên")
        elif r.returncode != 0:
            print("⚠️ cta_inject lỗi — video gốc giữ nguyên, chạy tay: "
                  f"python tools/cta_inject.py {out} --in-place")
    mb = out.stat().st_size / 1e6
    if not args.suffix:
        names = ",".join(plan["picks"])
        # 🔴 VOI --photo-dir, anh KHONG nam trong pool _bgphotos nen thu muc do co the
        #    khong ton tai => FileNotFoundError NEM RA SAU KHI VIDEO DA DUNG XONG:
        #    san pham dung, nhung wrapper tra EXITCODE=1 (da dinh that o video 38).
        #    Ghi so vao DUNG thu muc dang dung, va tao neu thieu.
        log_dir = Path(args.photo_dir) if (plan["mode"] == "photo" and args.photo_dir) \
            else PROJ / "06_VIDEO" / ("_bgphotos" if plan["mode"] == "photo" else "_bg")
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "USAGE.log", "a", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M}\t{slug}\t{names}\n")
        except OSError as e:
            print(f"⚠️ khong ghi duoc USAGE.log ({e}) — video VAN OK, chi mat so sach")
    print(f"DONE {out} ({mb:.0f} MB, {plan['total']/60:.1f} phút, "
          f"{len(plan['scenes'])} cảnh, motion={plan['mode']}+xfade)")
    if not args.suffix and not args.keep_tmp:
        cleanup_tmp(vdir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--stage", choices=["segs", "parts", "final", "A", "B"],
                    help="chạy 1 stage (bỏ = segs→parts→final); A/B = part 0/1 (tương thích cũ)")
    ap.add_argument("--part", type=int, help="chỉ ghép đúng 1 part (dùng với --stage parts)")
    ap.add_argument("--plan-only", action="store_true",
                    help="stage segs: lập kế hoạch + ghi _picks.json rồi DỪNG, chưa cắt "
                         "segment — để duyệt bộ clip ĐƯỢC CHỌN bằng mắt trước (clip_sheet "
                         "picks). Sạch rồi chạy lại không có cờ này.")
    ap.add_argument("--motion", choices=["clip", "photo", "boomerang"], default="clip",
                    help="clip = clip chạy trọn 1 lần xuôi (mặc định) | photo = ảnh tĩnh 100% "
                         "| boomerang = kiểu cũ xuôi-ngược (KHÔNG khuyến nghị)")
    ap.add_argument("--frame", choices=["none", "radio"], default="none",
                    help="radio = khung 'phòng thu đêm khuya' (typing-cam + player UI + "
                         "avatar + cột sóng từ voice.wav, phụ đề xanh outline to — user "
                         "duyệt demo 2026-08-20). Ghi vào _render_plan.json ở stage segs; "
                         "đổi khung thì chạy lại --stage segs")
    ap.add_argument("--scene-max", type=float, default=SCENE_MAX,
                    help=f"trần độ dài 1 cảnh, motion=clip (mặc định {SCENE_MAX}s)")
    ap.add_argument("--scene-min", type=float, default=SCENE_MIN,
                    help=f"sàn độ dài 1 cảnh, motion=clip (mặc định {SCENE_MIN}s)")
    ap.add_argument("--photo-dir", default=None,
                    help="thu muc anh rieng cua video (bo qua pool _bgphotos)")
    ap.add_argument("--photo-inorder", action="store_true",
                    help="1 anh / 1 canh theo DUNG thu tu ten file, khong xao")
    ap.add_argument("--photo-sec", type=float, default=PHOTO_SEC,
                    help=f"mỗi ảnh hiện bao lâu, motion=photo (mặc định {PHOTO_SEC}s)")
    ap.add_argument("--scenes", type=int, help="số cảnh (chỉ dùng cho motion=boomerang)")
    ap.add_argument("--bg-only",
                    help="file danh sách tên clip (1 dòng 1 tên) = KHOÁ pool đúng bộ đó, "
                         "kiểu dựng 'ít clip lặp lại'. Thắng --bg-limit")
    ap.add_argument("--bg-limit", type=int,
                    help="chỉ dùng N clip đầu của pool (đã ưu tiên clip chưa dùng)")
    ap.add_argument("--bgm", default="auto",
                    help="auto = xoay vòng track trong 06_VIDEO/bgm (mặc định từ 2026-07-30); "
                         "hoặc đường dẫn 1 file cụ thể")
    ap.add_argument("--bgm-gain", type=float, default=-40.0)
    ap.add_argument("--no-bgm", action="store_true")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--no-cta", action="store_true",
                    help="bỏ qua bước ghép hiệu ứng CTA giữa video")
    ap.add_argument("--keep-tmp", action="store_true",
                    help="giữ file trung gian (_seg/_cta/v_p*.mp4…); mặc định tự dọn")
    args = ap.parse_args()

    # Hạ priority BELOW_NORMAL (ffmpeg con thừa hưởng) — render nền không giành CPU
    # với UI trên máy 6 nhân; máy rảnh vẫn ăn full tốc độ. Chốt 2026-08-20.
    if sys.platform == "win32":
        try:
            import ctypes
            _k32 = ctypes.windll.kernel32
            _k32.GetCurrentProcess.restype = ctypes.c_void_p  # HANDLE 64-bit — thiếu là fail im lặng
            _h = ctypes.c_void_p(_k32.GetCurrentProcess())
            if _k32.SetPriorityClass(_h, 0x00004000):
                print("priority: BELOW_NORMAL (render nhường CPU cho UI)")
        except Exception:
            pass

    vdir = PROJ / "06_VIDEO" / args.slug
    if not vdir.exists():
        sys.exit(f"[LỖI] không thấy {vdir}")

    stage = args.stage
    if stage in ("A", "B"):                      # wrapper .cmd cũ
        args.part = 0 if stage == "A" else 1
        stage = "parts"

    if stage in (None, "segs"):
        stage_segs(vdir, args.slug, args)
    if stage in (None, "parts"):
        plan = json.loads((vdir / "_render_plan.json").read_text(encoding="utf-8"))
        idxs = [args.part] if args.part is not None else [p["i"] for p in plan["parts"]]
        for pi in idxs:
            stage_part(vdir, pi, args.crf)
    if stage in (None, "final"):
        stage_final(vdir, args.slug, args)


if __name__ == "__main__":
    main()
