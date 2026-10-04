# -*- coding: utf-8 -*-
"""
check_script_formula.py — GATE MAY cho khuon viet script kenh showa.

Do chi so cua mot script (hoac transcript doi thu) roi so voi dai muc tieu duc tu
3 kich ban >100K view (03_SCRIPTS/kichban1-3.md). Luat: 05_SCRIPT_FORMULA.md §5.2

    python tools/check_script_formula.py 03_SCRIPTS/13_natsu_TTS.md --truc A
    python tools/check_script_formula.py 03_SCRIPTS/kichban2.md --raw   # do transcript doi thu

HAI TANG:
  [CHAN]  sai la khong dat khuon  -> exit 1
  [CANH]  chi canh bao, khong chan (thiet bi ma cac ban thang KHONG dung deu)

🔴 LUAT 2 DONG CO (§4 E-LIST vs E-SCENE): mot bai chi can DAT MOT trong hai
   dong co chinh, khong phai ca hai. Ban dau cua gate nay doi ca hai -> danh
   truot ca 3/3 ban thang. K1 = co che/luat day nhung ngu quan 1/2888;
   K3 = ngu quan 1/209 nhung 0 cau 'naze', 2 lan nhac luat. Chung DANH DOI
   nhau, khong cong don.
"""
import argparse
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # §2.0h: gate crash = bao do gia
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NUM = r"[0-9０-９一二三四五六七八九十百千万億]"

PAT = {
    "moc_nam":   r"(?:昭和|平成|令和|明治|大正)" + NUM + r"{1,4}年|1[89]" + NUM + r"{2}年|20" + NUM + r"{2}年",
    "kim_tien":  NUM + r"{1,10}円",
    "phap_che":  r"法|条約|条|基準|規制|禁止|制定|普及率|統計",
    "nay_xua":   r"今では|今は|今なら|現代|いまでは|今の感覚|今じゃ|いまは|令和",
    # nguon: duc tu K2/K3. NOI 2026-09-07 (them mui/vi/xuc giac) + HA nguong 350->250 vi
    # ca 3 mau tham chieu deu day len: K1 1/962 (van LIST) · K2 1/186 · K3 1/134 (van SCENE).
    "ngu_quan":  r"匂い|香り|音|ジュ|カリ|トントン|パラパラ|じゅわ|ふわ|ガサガサ|キュ|ポタ|ドサ|バタバタ|手触り|ぬくもり|ふんわり|ひやり"
                 r"|味|冷た|ぬるい|ぬるく|湿った|煙|舌|肌|ざらざら|ひんやり|ぱき|しゃき|ことん|ぷく|つるり|きしむ|焦げ",
    "dong_mem":  r"かもしれません|気がします|寂しい|のではないでしょうか",
    "nazework":  r"なぜ|最大の理由|理由の一つ|理由の1つ|その背景|背景には",
    "loi_thuat": r"と(?:言わ|言う|言っ|聞く|呼ば|教えて|話して|怒鳴|声をかけ|訴え)|[「『][^」』]{2,}[」』]",
    "chung_nhan": r"私の父|私の母|知人|実話です|代の方",
}

# moc muc: "一点目" "1点目" "二つ目" "まずは" "続いて3つ目"
ITEM = re.compile(r"(?:" + NUM + r"{1,3}点目|" + NUM + r"{1,3}つ目)")   # bo nhanh "まずは" tran: no bat nham


def load(path, raw):
    t = io.open(path, encoding="utf-8").read().replace("[音楽]", "")
    if not raw:                                  # file _TTS.md cua minh
        t = re.sub(r"^#.*$", "", t, flags=re.M)  # heading
        t = re.sub(r"^>.*$", "", t, flags=re.M)  # blockquote ghi chu
        t = re.sub(r"\[[^\]]*\]", "", t)         # tag nhan nha
    return re.sub(r"\s+", "", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--truc", default="A", choices=["A", "B", "C"], help="B = truc tien, mien tran kim tien")
    ap.add_argument("--rate", type=float, default=None,   # None -> suy tu --truc (A 4.485 / B 4.93)
                    help="ky/giay. Bo trong = suy tu --truc. DO TU BAN RENDER, KHONG DOAN "
                         "(he so nay da sai 4 lan — xem CLAUDE.md §San xuat)")
    ap.add_argument("--raw", action="store_true", help="transcript doi thu: mien gate do dai + moc muc")
    a = ap.parse_args()
    # He so doc do tu ban render that, theo TUNG truc (CLAUDE.md §San xuat):
    #   A = 東北イタコ/ノーマル/0,90 (VOICEVOX)  -> video 12: 3.801 ky / 847,5s
    #   B = 阿井田茂/Calm/0,90 (AivisSpeech)     -> video 09: 4.565 ky / 926,8s
    RATE_TRUC = {"A": 4.485, "B": 4.93, "C": 4.485}
    if a.rate is None:
        a.rate = RATE_TRUC[a.truc]
        print("[rate] chua gõ --rate -> dung he so do duoc cua truc %s: %.3f ky/s"
              % (a.truc, a.rate))

    t = load(a.path, a.raw)
    N = len(t)
    if N < 200:
        print("!! File chi con %d ky sau khi lam sach — sai duong dan hoac thieu/thua co --raw?" % N)
        sys.exit(2)

    c = {k: len(re.findall(rx, t)) for k, rx in PAT.items()}
    d = lambda k: (N // c[k]) if c[k] else 0

    marks = [m.start() for m in ITEM.finditer(t)]
    n_muc = len(marks)
    first_s = marks[0] / a.rate if marks else None

    # --- nhan dien DONG CO ---
    eng_scene = 0 < d("ngu_quan") <= 250                       # E-SCENE: tai hien bang ngu quan
    eng_list = c["phap_che"] >= 8 and 0 < d("moc_nam") <= 500   # E-LIST: co che + moc nam + luat
    engine = ("SCENE+LIST" if (eng_scene and eng_list)
              else "SCENE" if eng_scene else "LIST" if eng_list else "KHONG CO")

    print("\n=== CHECK SCRIPT FORMULA — %s (truc %s) ===" % (a.path, a.truc))
    print("    %d ky sach -> %.1f phut @ %.2f ky/s   |   DONG CO nhan dien: %s\n"
          % (N, N / a.rate / 60, a.rate, engine))

    hard, soft = [], []
    # ---- CHAN ----
    hard.append(("DONG CO chinh (>=1 trong 2)", engine, engine != "KHONG CO",
                 "SCENE: ngu quan 1/<=250  |  LIST: phap>=8 va moc nam 1/<=500"))
    hard.append(("dong mem (かもしれません…)", "%d" % c["dong_mem"], c["dong_mem"] >= 5, ">=5 (K1 5 · K2 7 · K3 11)"))
    hard.append(("moc nam", "%d (1/%d ky)" % (c["moc_nam"], d("moc_nam")),
                 c["moc_nam"] >= 8 and 0 < d("moc_nam") <= 500, ">=8 lan va 1/<=500"))
    if not a.raw:
        lo, hi = int(14.5 * 60 * a.rate), int(18.0 * 60 * a.rate)
        hard.append(("so ky", "%d (%.1f phut)" % (N, N / a.rate / 60), lo <= N <= hi,
                     "%d-%d ky = 14,5-18,0 phut @ %.2f ky/s" % (lo, hi, a.rate)))
        if first_s is not None:
            hard.append(("vao muc 1", "%.1fs" % first_s, first_s <= 60.5, "<=60s (nham 40-50)"))
        else:
            hard.append(("vao muc 1", "khong thay moc 点目/つ目", False, "phai co moc muc de do"))
    if a.truc == "A":
        hard.append(("kim tien (tran truc A)", "%d" % c["kim_tien"], c["kim_tien"] <= 6,
                     "<=6 — 3 ban thang: 0-1"))

    # ---- CANH BAO ----
    soft.append(("ngu quan", "%d (1/%d ky)" % (c["ngu_quan"], d("ngu_quan")), 0 < d("ngu_quan") <= 250, "1/<=250 (bat buoc voi E-SCENE; K2 1/186 K3 1/134)"))
    soft.append(("nay-xua (今では)", "%d (1/%d ky)" % (c["nay_xua"], d("nay_xua")), 0 < d("nay_xua") <= 600, "1/<=600 (K3 chi 1/1341)"))
    # nguong 'naze' theo DONG CO: E-SCENE (5 o) doi 1 cau/muc; E-LIST 20 muc thi K1
    # — ban thang duy nhat cua khuon do — chi co 3 cau naze ca bai. Doi 1/muc o day
    # la doi thu chinh mau khong co (cung ho §5.2 luat 2 dong co).
    _naze_need = 3 if n_muc >= 8 else max(n_muc, 1)
    soft.append(("'naze' noi thanh loi", "%d" % c["nazework"], c["nazework"] >= _naze_need,
                 ">=%d (E-LIST: K1 20 muc = 3 · E-SCENE: 1/muc · K3 = 0)" % _naze_need))
    soft.append(("phap/che do (khe luat-thuc te)", "%d" % c["phap_che"], c["phap_che"] >= 3, ">=3 (K1 19 · K3 2)"))
    soft.append(("loi thuat lai / thoai", "%d" % c["loi_thuat"], c["loi_thuat"] >= 4, ">=4"))
    soft.append(("nguoi lam chung (証人)", "%d" % c["chung_nhan"], c["chung_nhan"] >= 1, ">=1 (chi K1 co)"))

    nbad = 0
    for tag, rows in (("CHAN", hard), ("CANH", soft)):
        print("  -- %s --" % ("GATE CHAN (sai = chua dat khuon)" if tag == "CHAN" else "CANH BAO (khong chan)"))
        for name, val, ok, exp in rows:
            print("  [%s] %-30s %-20s %s" % ("OK  " if ok else ("DO  " if tag == "CHAN" else "warn"),
                                             name, val, exp))
            if tag == "CHAN" and not ok:
                nbad += 1
        print("")

    if n_muc >= 2:
        lens = [(marks + [N])[i + 1] - marks[i] for i in range(n_muc)]
        mx, mn = max(lens), min(lens)
        ipk = lens.index(mx)
        pos = marks[ipk] * 100.0 / N
        # SONG chi la luat cua E-LIST (K1, 20 muc, 5,6x). E-SCENE 5 muc thi cac ban thang
        # deu PHANG: K2 1,43x · K3 1,23x -> doi song o day la doi thu chinh mau khong co.
        wave = ("OK" if mx / mn >= 2.5 else "warn: can >=2,5x (K1 5,6x)") if n_muc >= 8                else "-- mien: khuon <8 muc (K2 1,43x · K3 1,23x)"
        print("  -- SONG DO DAI MUC (%d muc) --" % n_muc)
        print("     ngan nhat %d ky (%.0fs) | dai nhat %d ky (%.0fs) | ti so %.1fx   %s"
              % (mn, mn / a.rate, mx, mx / a.rate, mx / mn, wave))
        print("     muc dai nhat = #%d o %.0f%% bai   %s\n"
              % (ipk + 1, pos, "OK" if pos >= 65 else "warn: nen dat o ~80%"))
    elif not a.raw:
        print("  -- SONG DO DAI MUC: khong do duoc (thieu moc 点目/つ目) --\n")

    print("=" * 66)
    if nbad:
        print("KET QUA: %d gate CHAN do -> chua dat khuon (05_SCRIPT_FORMULA.md §5.2)" % nbad)
        sys.exit(1)
    print("KET QUA: SACH toan bo gate CHAN. Doc lai cot 'warn' truoc khi giao.")


if __name__ == "__main__":
    main()
