# -*- coding: utf-8 -*-
r"""Thay VONG KHOANH VU VO bang CALLOUT co so/chu, gan TAY theo nghia cua phu de.

VI SAO (user chot 2026-08-25, chi vao clip_29):
  mode `focus` cua make_shot chi ve MOT VONG DO. Tren anh macro luoi thi vong do
  khoanh vao "mot mat luoi khong khac gi cac mat luoi ben canh" — KHONG cho thong tin.
  User: "khoanh vu vo do cha lam gi ca. Tao muon cho do hien ra text hoac so cho thay
  su nghiem trong... gen ra prompt tu sub de gan vao frame".

🔴 DA THU RUT TOKEN BANG REGEX TRUOC VA BO:
  Regex NUM tren doan phu de cua tung entry tra ra `1本` `1枚` `1種類` `2匹` — tu DEM,
  khong cho "su nghiem trong". Ly do co cau: MOI CON SO NANG cua bai (3ミリ / 1.15ミリ /
  1000匹 / 6週間 / 20度 / 2倍 / 8倍) DA NAM TREN THE VOX (bar/stat/timeline) roi; may
  khung anh giua cac the vox khong con so nao dang dat. => phai gan TAY theo nghia.
  Cung mot bai hoc voi ho anh cua so: may khong phan duoc NGHIA.

⛔ 3 entry CO Y de tran, khong ve gi:
  e27 = khoi CTA · e74 = tease cuoi bai · (e54 da co tag cua add_fx)
  "Khong co gi" TOT HON "mot vong khoanh vo nghia" — do la ca y cua user.

THU TU BAT BUOC:
  gen_slides -> autofocus --apply -> pin_inset24 --apply -> add_fx --apply -> callout24 --apply
"""
import argparse, io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "24_kamemushi-3mm-sukima"
S = PROJ / "03_SCRIPTS" / f"{SLUG}_SLIDES.json"

SHORT = 5     # <=5 ky -> con dau tron (stamp) · dai hon -> nhan giay ghim (tag)

# 🔴 DICH TAY vi tri callout — chi nhung khung DEMO CHO THAY dat sai (2026-08-26).
#    Mac dinh `at` = tam focus, va o phan lon khung do la vung TRONG canh chu the nen
#    dung. Nhung khung nao focus TRUNG chu the thi con dau de len chinh cai dang noi:
#      e45  stamp 「虫の休憩所」 dap len 2 con bo, chu 休憩所 chong than bo mau toi
#           -> dich sang nua trai (vai tron, sang deu) de doc ro va khong che bo
#    ⛔ KHONG doi mac dinh thanh "phia doi dien focus": 4 khung da duyet bang mat
#    (e2 tag · e6 stamp · e47 stamp · e51 tag) dang dat DUNG cho, doi la pha chung.
AT = {
    45: [0.28, 0.50],
}

# entry -> (chu tren callout, ly do lay tu chinh cau thoai)
# None = de tran, khong ve gi
CALLOUT = {
    6:  ("2匹",         "「2匹、落ちてきました」— con so cua chinh nguoi ke"),
    9:  ("1種だけ",      "「三種類のうち、家を選ぶのは1種類だけ」"),
    27: (None,          "khoi CTA — dat dau o day la nhieu"),
    39: ("エアコンの穴", "「エアコンの配管が壁を抜けるところ」=入口 thu 2"),
    40: ("15年",        "「そのパテは10年、15年で縮みます」"),
    45: ("虫の休憩所",   "「いちばん都合のいい休憩所です」"),
    51: ("薄い匂い＝集合", "「薄い匂いのほうが、集まる合図として働く」= cu lat"),
    65: ("線が残る",     "「縦の線が1本、残ったままになります」"),
    74: (None,          "tease cuoi bai — dat dau o day la nhieu"),
}


# 🔴 inset -> soft + callout (them 2026-08-26 sau demo): 4 khung cua so toan canh
#    khong phong duoc khe 3mm. Cung nguyen tac cua user: dung phong/khoanh vao cho
#    khong co gi, hay HIEN CHU. e2 da co tag 「開ける」 nen chi bo inset.
INSET_TO_CALLOUT = {
    2:  (None,          "da co tag 「開ける」 cua add_fx — chi bo inset"),
    35: ("重ならない",   "「枠と枠が、重ならない場所ができます」"),
    36: ("線が消える",   "「枠と枠が重なって、その線が消えます」"),
    63: ("一度で済む",   "「一度やれば、来年の秋も効いています」"),
    64: ("開ける側",     "「いっぱいに開けても、まだ隙間が残る」-> loi la ben mo"),
}


# 🔴 BO INSET (soi still 2026-08-26): 6/13 inset cua autofocus phong vao VUNG TRONG —
#    giay trang mo (e14) · troi/doi (e47) · vach shoji tron (e55) · tuong tran (e68, e75)
#    · goc kho (e24). autofocus do "ty le chi tiet" tren CA ANH, nhung khung crop van
#    roi vao cho phang. Cung loi voi vong khoanh: phong to cho khong co gi.
#    2 khung co so/chu dang noi thi kem callout, 4 khung con lai de tran.
INSET_DROP = {
    14: None,
    24: "1匹ずつ",     # 「暖房のたびに、1匹ずつ、部屋に出てきます」
    47: "日暮れ前",     # 「昔は、日暮れ前に取り込むのが当たり前でした」
    55: None,
    68: None,
    75: None,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    d = json.loads(S.read_text(encoding="utf-8"))
    n_st = n_tg = n_bare = n_skip = 0
    unseen = set(CALLOUT)

    for i, e in enumerate(d):
        s = e.get("shot")
        if not isinstance(s, dict) or s.get("mode") != "focus":
            continue
        unseen.discard(i)
        if s.get("avatar"):
            print(f"  e{i:<3} BO QUA     co avatar"); n_skip += 1; continue
        if s.get("fx"):
            # 🔴 VONG KHOANH VAN PHAI DI, chi GIU lai fx cua add_fx (khieu nai cua user la
            #    ve cai vong, khong phai ve fx). Bo buoc nay thi con sot mode `focus`.
            s["mode"] = "soft"
            s.pop("inset_pos", None)
            print(f"  e{i:<3} giu fx     add_fx da gan {s['fx'][0]['kind']} — bo vong khoanh")
            n_skip += 1
            continue
        if i not in CALLOUT:
            print(f"  e{i:<3} 🔴 CHUA GAN — entry `focus` moi, PHAI doc phu de roi gan tay")
            continue

        txt, why = CALLOUT[i]
        foc = s.get("focus") or [0.54, 0.46, 0.17]
        s["mode"] = "soft"                     # BO vong khoanh
        s.pop("inset_pos", None)
        if txt is None:
            s.pop("focus", None)
            print(f"  e{i:<3} soft tran  {why}"); n_bare += 1; continue
        kind = "stamp" if len(txt) <= SHORT else "tag"
        at = AT.get(i) or [round(foc[0], 2), round(foc[1], 2)]
        fx = {"kind": kind, "text": txt, "at": at, "t": 1.3}
        if kind == "tag":
            fx["size"] = 58
        s["fx"] = [fx]
        n_st += kind == "stamp"
        n_tg += kind == "tag"
        print(f"  e{i:<3} {kind:<9} 「{txt}」  <- {why}")

    for i, (txt, why) in INSET_TO_CALLOUT.items():
        s = d[i].get("shot")
        # nhan ca `soft`: autofocus co the da tu ha may khung nay ve soft (chung chinh la
        # nhom "phang deu") — luc do van phai gan callout, chi khong phai bo inset nua.
        if not isinstance(s, dict) or s.get("mode") not in ("inset", "soft"):
            print(f"  e{i:<3} 🔴 mode={s.get('mode') if isinstance(s,dict) else '?'} — doc lai")
            continue
        was = s.get("mode")
        s["mode"] = "soft"
        s.pop("inset_pos", None)
        if txt is None:
            print(f"  e{i:<3} {was:<9} {why}")
            continue
        if s.get("fx"):
            print(f"  e{i:<3} {was:<9} da co fx {s['fx'][0]['kind']} — khong chen them")
            continue
        foc = s.get("focus") or [0.54, 0.46, 0.17]
        kind = "stamp" if len(txt) <= SHORT else "tag"
        at = AT.get(i) or [round(foc[0], 2), round(foc[1], 2)]
        fx = {"kind": kind, "text": txt, "at": at, "t": 1.3}
        if kind == "tag":
            fx["size"] = 58
        s["fx"] = [fx]
        n_st += kind == "stamp"
        n_tg += kind == "tag"
        print(f"  e{i:<3} {kind:<9} 「{txt}」  <- {why}")

    for i, txt in INSET_DROP.items():
        s = d[i].get("shot")
        if not isinstance(s, dict) or s.get("mode") != "inset":
            print(f"  e{i:<3} bo qua     mode={s.get('mode') if isinstance(s,dict) else '?'}")
            continue
        s["mode"] = "soft"
        s.pop("inset_pos", None)
        if txt and not s.get("fx"):
            foc = s.get("focus") or [0.54, 0.46, 0.17]
            at = AT.get(i) or [round(foc[0], 2), round(foc[1], 2)]
            s["fx"] = [{"kind": "stamp", "text": txt, "at": at, "t": 1.3}]
            n_st += 1
            print(f"  e{i:<3} stamp     「{txt}」  <- bo inset (phong vao vung trong)")
        else:
            print(f"  e{i:<3} soft tran  bo inset (phong vao vung trong)")
            n_bare += 1

    if unseen:
        print(f"\n⚠ bang CALLOUT co entry khong con la `focus`: {sorted(unseen)} "
              "(so entry da doi? doc lai truoc khi tin)")
    print(f"\nstamp {n_st} · tag {n_tg} · soft tran {n_bare} · bo qua {n_skip}")
    if a.apply:
        S.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[OK] da ghi {S.name} — KHONG con entry nao mode `focus`")
    else:
        print("(XEM TRUOC — chua ghi gi)")


if __name__ == "__main__":
    main()
