# -*- coding: utf-8 -*-
"""
storyboard22_doc.py — viết KỊCH BẢN 22 thành một BẢN STORYBOARD (tài liệu người đọc).

Khác `storyboard22.py`: file kia xuất **prompt từng ô** để bơm máy; file này xuất **bản
storyboard** — cảnh, shot, hình, lời đọc, telop, mốc giây — để đọc, để duyệt, và để dán vào
Storyboard Studio ở bước ① Script.

Nguồn (không gõ tay số nào):
  · `_scenes22.py`  — bảng 91 scene (khuôn · telop · mô tả hình · nội dung thẻ số)
  · `timeline.json` — mốc giây THẬT đo từ `voice_full.wav` + lời đọc từng dòng
  · `flow22_full`   — hồ sơ cast (HUSB/WIFE/COUPLE) để viết khối ASSETS cho khớp lô ảnh

⚖️ Bản storyboard KHÔNG chứa khối guard/ánh sáng/negative — mấy thứ đó là việc của lớp
   prompt. Trộn vào đây thì tài liệu không đọc được, mà đó chính là thứ user cần đọc.
"""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")

from _scenes22 import SCENES, GENTEN              # noqa: E402
import flow22_full as F                           # noqa: E402
from flow22_full import classify                  # noqa: E402

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
OUT = os.path.join(VD, "_storyboard", "STORYBOARD_SCRIPT.md")

KIND_VN = {
    "PERSON": "người kể/nhân vật trong phòng", "HOLD": "cận tay giơ giấy/sổ",
    "DESK": "bàn làm việc đầy giấy tờ", "SCREEN": "màn hình hiển thị bảng số",
    "CROWD": "công sở / đám đông người cao tuổi", "SPLIT": "một nửa khung (ghép đôi)",
    "PANEL": "một ô trong ba ô ngang", "VIZ": "trực quan hoá bằng VẬT (cột xu, chồng tiền)",
    "INFOG": "sơ đồ phẳng", "META": "ẩn dụ 3D", "GAUGE": "đồng hồ đo",
}


def mmss(t):
    return f"{int(t)//60}:{int(t)%60:02d}"


def main():
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))["lines"]
    total = tl[-1]["end"]

    rows = []
    for k, (ln, kind, telop, body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        t0, t1 = tl[ln]["start"], (tl[nxt]["start"] if nxt < len(tl) else tl[-1]["end"])
        rows.append(dict(i=k, kind=kind, telop=telop, body=body, t0=t0, t1=t1,
                         says=[x["text"] for x in tl[ln:nxt] if x.get("text")]))

    n_art = sum(1 for r in rows if r["kind"] in ("art", "gfx"))
    o = [f"# STORYBOARD — video 22 「消える三十六万円の謎」",
         "",
         f"**{mmss(total)}** ({total:.0f}s) · **{len(rows)} shot** — {n_art} shot có HÌNH · "
         f"{len(rows)-n_art} shot là THẺ CHỮ (Remotion vẽ bằng font, không gen ảnh).",
         "",
         "Đọc một shot: `SHOT nn · mốc giây (độ dài) · khuôn`, rồi **TELOP** (chữ to đè lên "
         "hình) · **LỜI ĐỌC** (tiếng Nhật, đúng bản đã thu) · **HÌNH** (mô tả để gen).",
         "",
         "Dán vào **Storyboard Studio → ① Script** thì bỏ cột mốc giây, giữ CAST + SCENE + HÌNH.",
         "",
         "---", "",
         "## CAST — cố định xuyên video, không đổi trang phục giữa bài", "",
         f"- **Ông (chủ hộ đã mất / người xem nam)** — {F.HUSB}.",
         f"- **Bà (vợ / お姉さま)** — {F.WIFE}.",
         f"- **Cặp vợ chồng** — {F.COUPLE}.",
         "- **Nhân viên 年金事務所** — nữ hoặc nam mặc đồng phục công sở, sau quầy, thái độ điềm đạm.",
         "",
         "## BỐI CẢNH", "",
         "- **Nhà ở Nhật**: phòng khách/bếp sáng, tường trắng, nắng sớm qua rèm mỏng, đồ gỗ ấm.",
         "- **Công sở/年金事務所**: quầy tiếp dân, hàng ghế chờ, bảng số thứ tự, đèn trần đều.",
         "- **Bàn giấy tờ**: máy tính bỏ túi, sổ tay, phong bì nâu, chồng hồ sơ, chén trà.",
         "",
         "## LUẬT HÌNH (áp cho mọi shot)", "",
         "- Khổ **16:9**. Máy **đứng yên**, không zoom/pan — mỗi shot là **một khoảnh khắc**.",
         "- Chữ đọc được trong khung **chỉ là chữ số** (số tiền, ngày). Chữ Nhật trên giấy/màn "
         "hình để **nhỏ và mờ** — chữ Nhật gen ra là nát nét.",
         "- Giấy tờ và màn hình phải **kín đặc như đồ thật**; hai dòng cần đọc thì in TO: "
         "**180,000** và **360,000**, ngày **4/15** và **6/15**.",
         "- Không quầng đỏ/cảnh báo đỏ (bài nói về tiền ĐƯỢC NHẬN); cảnh báo dùng hổ phách.",
         "",
         "---", ""]

    for r in rows:
        dur = r["t1"] - r["t0"]
        # 🔴 `_scenes22` nay co 4 kind: art · stat · gfx · genten. `gfx` = do hoa 2D/3D
        #    (INFOG/META/GAUGE) — VAN co hinh, chi khac la khong phai anh chup that.
        kd = classify(r["body"]) if r["kind"] in ("art", "gfx") else None
        head = (f"## SHOT {r['i']+1:02d} · {mmss(r['t0'])}–{mmss(r['t1'])} ({dur:.1f}s) · "
                + (f"**{kd}** — {KIND_VN.get(kd, '')}" if kd else
                   {"stat": "**THẺ SỐ LIỆU** (Remotion vẽ bằng font, không gen ảnh)",
                    "formula": "**THẺ CÔNG THỨC** (không gen ảnh)",
                    "genten": "**ẢNH 原典** (screenshot trang thật, không gen ảnh)"}[r["kind"]]))
        o += [head, ""]
        o += [f"**TELOP:** {r['telop'].replace(chr(10), ' / ')}", ""]
        if r["says"]:
            o += ["**LỜI ĐỌC:**", ""] + [f"> {s}" for s in r["says"]] + [""]
        if r["kind"] in ("art", "gfx"):
            body = r["body"].split(":", 1)[1].strip() if ":" in r["body"].split(" ")[0] else r["body"]
            o += [f"**HÌNH:** {body}", ""]
        elif r["kind"] == "genten":
            src = GENTEN.get(r["body"])
            o += [f"**NGUỒN:** `{r['body']}`"
                  + (f" — {src[0]}" if isinstance(src, (tuple, list)) and src else ""), ""]
        else:
            lines = r["body"] if isinstance(r["body"], list) else [str(r["body"])]
            o += ["**BẢNG:**", ""] + [f"| {l.replace('|', ' | ')} |" for l in lines] + [""]

    io.open(OUT, "w", encoding="utf-8").write("\n".join(o))
    print(f"⭐ STORYBOARD -> {OUT}")
    print(f"   {len(rows)} shot · {n_art} có hình · {len(rows)-n_art} thẻ chữ/原典 · "
          f"{mmss(total)}")
    print(f"   {len(o)} dòng markdown")


if __name__ == "__main__":
    main()
