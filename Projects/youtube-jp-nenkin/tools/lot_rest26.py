# -*- coding: utf-8 -*-
r"""lot_rest26.py — chẻ 61 prompt của video 26 thành các LÔ CHƯA GEN.

Vì sao tách khỏi `beats26.py`: sync() của beats chỉ biết LOT1 (lô duyệt, ghim cứng).
Sau khi LOT1 được user duyệt thì phần còn lại cần chia nhỏ để bơm từng đợt — và danh
sách "đã gen" sẽ còn đổi theo từng vòng, nên nó là việc của một tool riêng, không phải
của bộ sinh prompt.

🔴 LOẠI THEO **KHOÁ SHOT**, KHÔNG THEO CHỈ SỐ SCENE: LOT1 chỉ gen shot `a` của 10 scene;
   scene 38 có `38a` (đã gen) và `38b` (CHƯA) — bỏ cả scene là mất một khe hình.

CHẠY:  python tools/lot_rest26.py [--done 0a,1a,5a,...] [--size 17]
  · không truyền `--done` thì mặc định = 10 shot của LOT1.
  · đọc `vox26_FLOW.txt` + `vox26_TENFILE.txt` (do `beats26.py` sinh), ghi ra
    `vox26_REST.txt` · `vox26_REST_TENFILE.txt` · `vox26_LOT2..N(.._TENFILE).txt`
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai")
DONE_DEF = ["0a", "1a", "5a", "6a", "10a", "12a", "26a", "35a", "38a", "46a"]


def main() -> int:
    done = DONE_DEF
    size = 17
    if "--done" in sys.argv:
        done = [x.strip() for x in sys.argv[sys.argv.index("--done") + 1].split(",") if x.strip()]
    if "--size" in sys.argv:
        size = int(sys.argv[sys.argv.index("--size") + 1])

    flow = [l.rstrip("\n") for l in io.open(os.path.join(VD, "vox26_FLOW.txt"),
                                            encoding="utf-8") if l.strip()]
    ten = [l.rstrip("\n") for l in io.open(os.path.join(VD, "vox26_TENFILE.txt"),
                                           encoding="utf-8") if l.strip()]
    if len(flow) != len(ten):
        print(f"🔴 FLOW {len(flow)} dòng nhưng TENFILE {len(ten)} dòng — chạy lại beats26.py")
        return 1

    keys = [re.search(r"clips/clip_([0-9a-z]+)\.mp4", t).group(1) for t in ten]
    miss = [d for d in done if d not in keys]
    if miss:
        print(f"🔴 khoá không có trong TENFILE: {miss} — sổ `--done` sai, dừng")
        return 1

    rest = [(k, flow[i], ten[i]) for i, k in enumerate(keys) if k not in done]
    print(f"tổng {len(flow)} shot · đã gen {len(done)} · CÒN LẠI {len(rest)}")

    def dump(name, rows):
        io.open(os.path.join(VD, name + ".txt"), "w", encoding="utf-8").write(
            "\n".join(p for _k, p, _t in rows) + "\n")
        io.open(os.path.join(VD, name + "_TENFILE.txt"), "w", encoding="utf-8").write(
            "\n".join(f"dong {j + 1:>3} -> " + t.split("-> ", 1)[1]
                      for j, (_k, _p, t) in enumerate(rows)) + "\n")

    dump("vox26_REST", rest)
    print(f"   vox26_REST.txt            {len(rest)} shot")
    for n in range(0, len(rest), size):
        ch = rest[n:n + size]
        tag = n // size + 2
        dump(f"vox26_LOT{tag}", ch)
        print(f"   vox26_LOT{tag}.txt            {len(ch):>2} shot  "
              f"({ch[0][0]} … {ch[-1][0]})")
    print(f"\n📁 {VD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
