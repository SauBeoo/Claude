# -*- coding: utf-8 -*-
"""Sinh SLIDES.json + prompt gen anh cho video 03 (kieta-kyoshitsu).

- 12 diem + cac canh khung/anecdote = ~37 entry, 100% anh AI (khong archival footage
  o lot nay - giong video 02 luc moi viet, footage that la mot lop bo sung SAU).
- match lay THANG tu dong trong _TTS.md -> khong bao gio chet cue.
- prompt = [canh] + [preset boi canh 1B] + [style lock 1A] + [Avoid] (04_VIDEOGEN_PROMPTS.md).
"""
import io, sys, re, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
TTS = ROOT / "03_SCRIPTS" / "03_kieta-kyoshitsu_TTS.md"
OUT_JSON = ROOT / "03_SCRIPTS" / "03_kieta-kyoshitsu_SLIDES.json"
OUT_DIR = ROOT / "06_VIDEO" / "03_kieta-kyoshitsu"


def _dur():
    t = re.sub(r"\[[^\]]*\]", "", TTS.read_text(encoding="utf-8"))
    return len(re.sub(r"\s", "", t)) / 3.98  # 3.98 ky/giay = he so do that cua kenh (video 01)


# --- 04_VIDEOGEN_PROMPTS.md §1 ---
LOCK = ("1970s Japan (Showa era, around 1970), shot on 8mm home movie film, "
        "faded warm Fujicolor palette, soft natural light, gentle film grain, "
        "slight vignette, nostalgic documentary photography, muted greens and ochres, "
        "natural imperfect framing, 16:9")
PRESET = {
    # dung san theo 04_VIDEOGEN_PROMPTS.md §1B - video hoc duong dung preset nay
    "school": ("wooden school interior, dark stained wood, sliding glass doors in "
               "wooden frames, waxed wooden floor"),
    # MOI, mo rong theo video nay - canh NGOAI TROI o san truong (tuong Ninomiya Kinjiro).
    # KHONG dung 'school' (noi that) vi mau thuan voi 'dirt schoolyard, outdoor' - cung
    # luat da ghi o 04_VIDEOGEN_PROMPTS.md §1B canh bao ve preset trong-nha vs ngoai-pho.
    "schoolyard": ("Japanese elementary schoolyard, packed dirt ground, a wooden "
                   "school building visible in the background, open sky, morning light"),
}
# 🔴 'no watermark' PHAI CO - thieu no la ca lo anh dinh dau ✦ (media-library.md §2.10 ⑤)
AVOID = ("no watermark, no logo, no signature, no sparkle mark. "
         "Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, "
         "modern clothing, sneakers with logos, readable text or signage, brand logos, "
         "western faces, anime style, oversaturated HDR look, close-up faces.")

# (chi so dong noi dung trong TTS, ten file, preset, mo ta canh)
# ⚠️ Entry "01_toban_asa" (figure unlocking door), "03_kyoshitsu_yoake" (dawn wide) va
# "27_asahi_desks" (sunlight wide) — ca 3 anh AI — đã BỎ 2026-08-22, thay bằng phim tư
# liệu THẬT ở bảng ARCH bên dưới, theo luật mới CLAUDE.md: "mở đầu BẮT BUỘC video thật +
# ghép nhiều video thật càng nhiều càng tốt".
# 🔴 CHI SO DONG DA DOI 2026-08-22 (b): tach dong "今日は…並べます。/いま聞こえた…一点目。"
# thanh 2 dong rieng trong _TTS.md (chong loop clip qua nhieu lan) -> MOI chi so tu dong
# 5 tro di bi +1 so voi ban truoc. Doi tool nay THI PHAI doi ca _TTS.md cung luc.
SCENES = [
    (3, "02_tessitsu_kiru", "school", "extreme close-up of a metal stylus scratching a wax stencil sheet clipped onto a corrugated file board, thin curls of wax shaving, a hand steadying the paper, warm desk lamp light"),
    # STILLFRAME A — trich tu clip_00.mp4 (khong phai AI-gen), chan clip that o day de
    # clip_00 chi can phu 0–10.8s (index0+1) thay vi 0–20.5s (index0+1+2) -> giam loop
    # tu ~2,56x xuong ~1,35x. Dat vao slides_img the ten thuong, KHONG can prompt AI.
    (2, "37_STILL_A_gakuseitachi", "school", "[STILLFRAME — trich tu clip_00.mp4 @4s, KHONG phai prompt AI-gen, dat anh that vao slides_img]"),
    (8, "04_warabanshi", "school", "close-up of a stack of freshly printed rough greyish-yellow mimeograph test paper on a wooden desk, faint blue-purple ink still slightly damp, corners uneven, no readable text"),
    # STILLFRAME C — trich tu clip_02.mp4, chan clip_02 lai o dung 1 cau dau (khoang 7s,
    # gan khop 8s clip, gan nhu khong loop) thay vi phu ca 2 cau (~11,9s).
    (5, "38_STILL_C_lophoc", "school", "[STILLFRAME — trich tu clip_02.mp4 @4s, KHONG phai prompt AI-gen, dat anh that vao slides_img]"),
    (9, "05_surimura", "school", "a hand holding a single sheet of rough mimeograph paper up toward window light, faint uneven purple ink markings blurred and illegible, edges slightly torn"),
    (10, "06_nioi_kagu", "school", "small hands lifting a sheet of rough paper close in front of the face, seen from directly behind the shoulder so the face is fully hidden by the paper and hair, soft morning light, no facial features visible at all"),
    (11, "28_tsukue_narabi", "school", "a long row of empty wooden two-seater desks receding down the classroom, morning light falling across the aisle, cloth bags hanging on desk hooks"),
    (12, "07_ROW_placeholder_unused", "school", "PLACEHOLDER_UNUSED"),
    # STILLFRAME B — trich tu clip_03.mp4, chan clip_03 lai o dung index6 (chi phu index5,
    # ~6,0s, DUOI 8s -> khong loop, chi bi cat ngan nhe) thay vi phu index5+6+7 (~30,2s).
    (7, "39_STILL_B_kakukoseitachi", "school", "[STILLFRAME — trich tu clip_03.mp4 @4s, KHONG phai prompt AI-gen, dat anh that vao slides_img]"),
    (15, "08_futarigake_tsukue", "school", "a pair of old wooden two-seater desks with metal legs, a faint pencil-drawn line scratched down the centre of the shared desktop, cloth bags hanging on the side hooks"),
    (16, "09_keshigomu_sen", "school", "close-up of a pink eraser pushing a faint pencil line across the wood grain of a shared desk, small hands reaching in from both sides"),
    (17, "10_inktsubo_ana", "school", "close-up of an old wooden desk corner with a small round hole where an inkwell once sat, worn smooth with age, a few pencil shavings caught inside"),
    (19, "11_sekiban_sekihitsu", "school", "a small black slate board and a stick of slate pencil resting on a dusty shelf at the back of a classroom, faint chalky scratch marks on the slate surface"),
    (20, "29_sekiban_chalk", "school", "close-up of pale chalky scratch marks on a small slate board, a stick of white slate pencil resting beside it, dim storeroom light"),
    (22, "12_soroban", "school", "close-up of a wooden Japanese abacus on a desk, beads mid-slide, a small hand resting just beside it, morning light"),
    (23, "30_soroban_hikidashi", "school", "a wooden abacus lying inside a half-open desk drawer among pencils and erasers, soft indoor light"),
    (26, "13_daruma_stove", "school", "a round cast-iron potbelly stove in the corner of a classroom, glowing orange coal fire visible through the open grate door, a battered aluminum kettle resting on top"),
    (27, "31_matchi_shinbunshi", "school", "close-up of a match striking beside a twist of newspaper inside the open grate of a potbelly stove, a small flame just catching, warm orange light"),
    (28, "14_uchiwa_aogu", "school", "close-up of small hands holding a paper fan close to the open grate of a potbelly stove, orange firelight flickering across them, thin smoke curling upward"),
    (30, "15_gyunyu_atatame", "school", "glass milk bottles with round paper caps lined up on top of a warm cast-iron stove, condensation beading on the glass, faint steam rising, absolutely no on-screen date stamp, no timecode, no burned-in numbers or letters anywhere in the frame"),
    (32, "16_kinjiro_zou", "schoolyard", "a weathered concrete statue of a boy carrying a bundle of firewood on his back while reading a book, standing in the corner of a dirt schoolyard, morning light, a wooden school building softly blurred in the background"),
    (34, "32_stove_kettle", "school", "close-up of a battered aluminum kettle steaming gently on top of a glowing potbelly stove, warm orange light reflecting off the metal"),
    (36, "17_mokuzou_rouka", "school", "a long empty wooden school corridor with waxed floorboards reflecting soft light, sliding wooden-framed windows along one side, worn wood grain, completely empty with no people, no wall signs, no room number plaques, no notices or papers pinned to any wall or board"),
    (37, "18_gariban_honntai", "school", "close-up of a wooden-framed mimeograph printing frame with a fine wire mesh screen, a blank stencil sheet clipped in place showing only plain grey-brown mesh texture with no writing, design, or pattern of any kind, an ink roller resting beside it, warm desk lamp light, the room and doorway behind it are completely empty with absolutely no students or people of any kind visible anywhere in the frame"),
    (39, "33_tessitsu_yasuri", "school", "close-up of a metal stylus resting on a corrugated file board beside a finished stencil sheet, fine pale wax shavings scattered around it, the stencil surface shows only random abstract scratch texture, not any real letters or organised pattern"),
    (41, "19_genshi_ato", "school", "close-up of a small torn corner of a cut wax stencil sheet held up to soft window light, a few scattered random scratch marks and tiny irregular perforations, deliberately NOT an organised grid or table of characters, not a full alphabet or syllabary chart, just scattered abstract marks, a hand at the edge of frame"),
    (44, "20_enpitsukezuri", "school", "close-up of a hand-crank pencil sharpener mounted on the edge of a teacher's desk, wood shavings scattered beneath it, a short stub pencil resting beside it"),
    (45, "21_kokubankeshi", "school", "two chalkboard erasers suspended mid-clap in front of an open classroom window, held by a pair of hands entering from the bottom edge of frame only, no visible arms or body, no face, a small cloud of white chalk dust catching the sunlight"),
    (48, "22_tsuuchihyou", "school", "a small paper report card lying open on a low wooden table, mostly blank ruled grid with only a few faint illegible pencil smudges, no title text, no kanji, no numbers, a stub pencil resting beside it"),
    (49, "34_tsuuchihyou_hyouka", "school", "close-up of a small paper report card showing a blank ruled grid on aged paper with only a few faint illegible pencil marks, no title, no kanji characters, no name, no readable numbers anywhere, soft indoor light"),
    (51, "35_kyoshitsu_manin", "school", "a packed 1970s Japanese classroom seen strictly from the very back corner of the room, rows of wooden desks placed close together, every student visible only from behind or in silhouette with no faces visible at all, the blackboard and teacher far in the background are soft and out of focus with no legible writing, just vague blurred shapes, overcast window light"),
    (59, "24_soroban_ima", "school", "close-up of a wooden Japanese abacus resting on a plain sunlit desk, one bead mid-slide under a fingertip, soft warm light, a slightly more contemporary plain room suggested by the clean simple background"),
    (61, "25_yubi_kioku", "school", "close-up of fingers making a small pinching motion in mid-air as if flicking an abacus bead, no abacus actually present, soft indoor light, empty desk in the background"),
    (63, "26_shiroi_te", "school", "close-up of an open hand dusted with a mix of white chalk powder and faint dark ink stains, resting on a worn wooden desktop, soft window light, background completely out of focus with no legible blackboard writing and no clearly visible people"),
]
# ⛔ Xoa entry PLACEHOLDER_UNUSED ngay sau khi dinh nghia — chi de giu cho de doc thu tu,
# thuc te khong dung (line 12 = "中でも、九点目は…" da co STILLFRAME B rieng o line 7... )
SCENES = [s for s in SCENES if s[3] != "PLACEHOLDER_UNUSED"]

# Phim tu lieu THAT — luat moi CLAUDE.md 2026-08-21/22: "mo dau BAT BUOC video that +
# ghep nhieu video that cang nhieu cang tot". (chi so dong, id, ss, dur) — cat bang
# cut_archival.py voi spec tools/archival_spec_03.json; file = clips/clip_<vi tri>.mp4
# 🔴 Chi so dong da doi cung luat tren (tach dong o index4 cu).
ARCH = [
    (0, "shugaku_ryokou", 816.0, 8.0),       # Japan Today 1959 CC0 — cold open (index0+1, ~10.8s, loop ~1.35x)
    (4, "lophoc_toancanh", 325.0, 8.0),      # Children of Japan 1941 PD — chi phu 1 cau (~7s, gan khong loop)
    (6, "hocsinh_dangviet", 335.0, 8.0),     # Children of Japan 1941 PD — chi phu index5 (~6s, KHONG loop, cat ngan)
]


def content_lines(raw):
    out = []
    for l in raw.split("\n"):
        s = re.sub(r"\[[^\]]*\]", "", l).strip()
        if s:
            out.append(s)
    return out


def main():
    raw = TTS.read_text(encoding="utf-8")
    lines = content_lines(raw)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides, flow, names, rows = [], [], [], []
    err = 0
    merged = sorted([("img", s[0], s) for s in SCENES] + [("vid", a[0], a) for a in ARCH],
                    key=lambda x: x[1])
    for kind, idx, item in merged:
        if idx >= len(lines):
            print(f"[LOI] chi so dong {idx} vuot ngoai file"); err += 1; continue
        line = lines[idx]
        m = line[:14]
        if not any(m in L for L in lines):
            print(f"[LOI] match khong khop: {m}"); err += 1; continue
        if kind == "vid":
            slides.append({"match": m, "video": True})
            names.append(f"CLIP_slide_{len(slides)-1:02d}_{item[1]}.mp4 (da cat san, xem clips/)")
            continue
        _, name, preset, desc = item
        slides.append({"match": m, "photo": True})
        if desc.startswith("[STILLFRAME"):
            # trich tu clip that, KHONG can prompt AI-gen -> khong ghi vao FLOW.txt
            names.append(f"slide_{len(slides)-1:02d}_{name}.jpg  <-- {desc}")
        else:
            flow.append(f"{desc}, {PRESET[preset]}, {LOCK}. {AVOID}")
            names.append(f"slide_{len(slides)-1:02d}_{name}.jpg")
            rows.append((len(rows), name, preset, m, desc))

    # GATE: prompt TU MAU THUAN - mo ta ghi 'no X' ma preset phia sau lai ta X.
    PAIRS = [("no street", "shopping street"), ("no noren", "noren"),
             ("no lettering", "signage"), ("no shop sign", "signage"),
             ("no sky", "sky"), ("no people", "students"),
             ("indoor", "outdoor"), ("no face", "face")]

    def _positive(text, pos):
        t = re.sub(r"\bno\b(?:\s+\w+){0,3}\s+" + re.escape(pos), " ", text)
        return pos in t

    for i, (idx, name, preset, desc) in enumerate(SCENES):
        if desc.startswith("[STILLFRAME"):
            continue
        low = f"{desc}, {PRESET[preset]}, {LOCK}".lower()
        for neg, pos in PAIRS:
            if neg in low and _positive(low, pos):
                print(f"[LOI] prompt {i:02d} TU MAU THUAN: co '{neg}' nhung van ta '{pos}'")
                err += 1

    if err:
        print(f"\n🔴 {err} loi - KHONG ghi file"); sys.exit(1)

    OUT_JSON.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT_DIR / "scene_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (OUT_DIR / "scene_prompts_TENFILE.txt").write_text("\n".join(names) + "\n", encoding="utf-8")

    n = len(slides)
    dur = _dur()
    diem = sum(1 for r in rows)
    print(f"OK {n} entry -> {OUT_JSON.name}")
    print(f"   do dai uoc tinh: {dur:6.1f} giay = {int(dur)//60}:{int(dur)%60:02d}")
    print(f"   {dur/n:5.1f} giay/hinh   (khong duoi 6s)      {'OK' if dur/n >= 6 else 'RỚT'}")
    print(f"   {n/(dur/60):5.2f} doi hinh/phut (tran 6)      {'OK' if n/(dur/60) <= 6 else 'RỚT'}")
    print(f"   {dur/n:5.1f}s max treo    (canh bao >60s)     {'OK' if dur/n <= 60 else 'CANH BAO'}")
    print(f"   preset dung: {sorted(set(r[2] for r in rows))}")
    print(f"   phim that: {sum(1 for e in slides if e.get('video'))} entry (clips/clip_XX.mp4 theo vi tri)")


if __name__ == "__main__":
    main()
