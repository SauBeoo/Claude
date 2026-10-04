# -*- coding: utf-8 -*-
"""gen_illus_prompts_01.py — prompt anh MINH HOA (khuon kenh thang ngach 【心理学】60代) cho kinishinai bai 1.

Bang chung: 01_SOURCES/CHANNEL_BENCHMARK_shinri60_2026-10-02.md — 4/4 video thang: linh vat tron trang tren nen
minh hoa chi tiet tong AM, khong anh that, khong nguoi dan, chu tren hinh chi co phu de. User chot 2026-10-02:
chuyen sang minh hoa.
Nhan vat: NGUOI VE TRANH TRUYEN 絵本 (user 2026-10-02, bo meo) — moi nhan vat giu MOT bo
"dau hieu" co dinh (TOC + ao + phu kien) de nguoi xem nhan ra xuyen bai (het loi "nhieu mat" cua ban nguoi that).
Hanh dong tung canh lay tu _plan/storyboard_src.py (S) — mot nguon, khong go lai.
Xuat (06_VIDEO/<stem>/_plan/):
  illus_CAST_FLOW.txt   — tam ban mau nhan vat (gen TRUOC, dung lam REFERENCE cho moi canh co nhan vat do)
  illus_FLOW.txt        — 1 prompt / 1 dong, theo thu tu slide
  illus_TENFILE.txt     — dong -> slide_NN.png + nhan vat can kem reference
Gate: guard NO TEXT trong 15% dau · moi ten CAST in hoa trong hanh dong da duoc thay bang mo ta.
Chay: python tools/gen_illus_prompts_01.py 01_kuchiguse-hitonome
"""
import sys, io, re, json, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]

# NGUOI VE TRANH TRUYEN 絵本 (user 2026-10-02: meo "khong hop" -> chon nguoi ve tay). Khac kenh thang (dau tron trang)
# nhung giu cai ho lam dung: minh hoa am, khong anh that. Nhan dien tung nhan vat bang TOC + AO + PHU KIEN co dinh;
# mat giu dong nhat bang ban mau nhan vat lam REFERENCE (Flow Ingredients) o moi canh co nhan vat do.
PERSON = ("a Japanese person drawn in a soft hand-drawn picture-book style: gentle simple facial features, small kind "
          "eyes, soft rosy cheeks, slightly rounded proportions, soft coloured-pencil and watercolour linework")
CAST = {
    "KIEKO": PERSON + ", a 68-year-old woman with short soft silver hair in a neat bob, gentle smile lines, wearing a navy "
             "cardigan over a cream blouse and small pearl earrings, kind and slightly shy posture",
    "YOUNG KIEKO": PERSON + ", the same woman at 38 with neat dark hair in a low bun, wearing a navy department-store uniform "
                   "jacket with a small patterned scarf at the neck",
    "AYUMI": PERSON + ", a woman of about 41 with shoulder-length dark hair, wearing a beige knit sweater (Kieko's daughter)",
    "TAKESHI": PERSON + ", a man of about 44 with short dark hair, wearing a grey knit sweater (Kieko's son)",
    "REN": PERSON + ", a boy of about 8 with a round face and short hair, wearing a bright yellow sweater",
    "NORIKO": PERSON + ", a cheerful woman of about 70 with short curly grey hair, wearing a green quilted vest",
    "SACHIKO": PERSON + ", a woman of about 68 with short dark-grey hair and round glasses, wearing a rust-orange sweater",
    "MICHIKO": PERSON + ", a woman of about 64 with grey hair tied back, wearing a lavender cardigan (Kieko's younger sister)",
    "DAISUKE": PERSON + ", a high-school boy of 17 in a black gakuran school uniform",
    "VIEWER": PERSON + ", an ordinary woman in her sixties with short greying hair, wearing a plain pale-blue blouse",
}
# nguoi khong ten trong hanh dong (A young man, Residents, ...) -> cung net ve tranh truyen
GENERIC = ("Japanese people drawn in a soft hand-drawn picture-book style with gentle simple features and soft "
           "coloured-pencil and watercolour linework")

GUARD = ("NO TEXT: no letters, no numbers, no writing, no signs and no logos anywhere in the picture; every paper, book, "
         "screen, sign and box is blank.")
STYLE = ("A 16:9 warm, cosy hand-painted picture-book illustration with a richly detailed Japanese background: soft "
         "golden lamplight or warm daylight, warm amber and cream colours, soft gouache textures, calm and "
         "heart-warming mood, like a Japanese picture book (絵本). Every person in the picture is one of the " + GENERIC + ", never photorealistic.")
TAIL = ("The characters are clearly readable at small size, placed inside the left 85% of the frame; the bottom-right "
        "corner is plain background. No watermark, no signature, no text.")
LOC = {
    "POST": "a small Japanese post office counter, bright daytime",
    "VIEWER_HOME": "a Japanese bedroom with tatami and shoji at night",
    "DEPT": "a 1990s Japanese department-store kimono counter with rolls of fabric",
    "OFFICE80": "a 1980s Japanese office and a traditional living room",
    "HOME": "a warm Japanese home: tatami living room with a kotatsu, kitchen at the back",
    "HOME_K": "a warm Japanese home kitchen",
    "STREET": "a Japanese city street", "ARCADE": "a covered Japanese shopping arcade", "BUS": "inside a city bus in spring",
    "HALL": "a neighbourhood community hall with folding chairs", "DANCHI": "an apartment-complex courtyard",
    "CAFE": "a retro Japanese coffee shop", "PARK": "a park path with trees", "TRAIN": "a train and railway platform in December",
    "LAB": "a calm illustrated scene that explains a psychology study", "SYMBOL": "a quiet tatami room at night",
    "OBJECT": "a close-up still-life on a wooden table", "MEMORY": "a faded nostalgic memory scene, softer sepia colours",
    "SISTER": "a small Japanese kitchen at night",
}


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sp = importlib.util.spec_from_file_location("sb", vd / "_plan" / "storyboard_src.py")
    sb = importlib.util.module_from_spec(sp); sp.loader.exec_module(sb)
    sl = json.loads((PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json").read_text(encoding="utf-8"))
    names = sorted(CAST, key=len, reverse=True)

    cast_lines = []
    for nm, desc in CAST.items():
        cast_lines.append(" ".join([GUARD, "A 16:9 character reference sheet in the same warm hand-painted picture-book illustration "
                                    "style on a plain soft cream background. Show the SAME character three times side by "
                                    "side: front view, three-quarter view and side view, full body, standing calmly.",
                                    f"CHARACTER: {desc}.", "Keep the bottom-right corner plain. No watermark, no text."]))

    rows, ten = [], ["dong | slide | kem reference nhan vat | canh"]
    for i, e in enumerate(sl):
        shot = e.get("_shot")
        if not isinstance(shot, int) or shot not in sb.S or e.get("card") or e.get("reveal") or e.get("_host"):
            continue
        loc, act, _f, _n = sb.S[shot]
        used = []
        for nm in names:
            pat = re.compile(rf"\b{re.escape(nm)}(?:'s)?\b")
            if pat.search(act):
                used.append(nm)
                act = pat.sub(lambda m: f"the {nm.lower().title()} character" + ("'s" if m.group(0).endswith("'s") else ""), act)
        assert not re.search(r"\b[A-Z]{3,}\b", act.replace("NO", "")), f"slide {i}: con ten in hoa: {act}"
        who = " ".join(f"The {nm.lower().title()} character is {CAST[nm]}." for nm in used)
        p = " ".join(x for x in [GUARD, STYLE, f"SETTING: {LOC.get(loc, 'a warm Japanese everyday scene')}.",
                                 f"SCENE: {act}", who, TAIL] if x)
        assert p.find("NO TEXT") * 100 // len(p) <= 15, i
        rows.append(p)
        ten.append(f"{len(rows):3d} | slide_{i:02d}.png | {', '.join(used) or '-'} | {act[:70]}")
    out = vd / "_plan"
    (out / "illus_CAST_FLOW.txt").write_text("\n".join(cast_lines) + "\n", encoding="utf-8")
    (out / "illus_FLOW.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (out / "illus_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
    print(f"ban mau nhan vat: {len(cast_lines)} · canh: {len(rows)} -> {out}")


if __name__ == "__main__":
    main()
