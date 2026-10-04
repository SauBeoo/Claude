# -*- coding: utf-8 -*-
r"""build_remotion_21b.py — project.json cho video 21 (bản viết lại, footage ≤52%).

Khác `build_remotion_21.py` ở đúng một chỗ, và nó là cả lý do tồn tại:
**scene KHÔNG neo bằng chỉ số dòng gõ tay nữa** — đọc `scenes_plan.json` do
`plan_scenes_21b.py` sinh ra từ `timeline.json` thật. Bản cũ neo `GENTEN = {16: [...]}`,
và khi lời được viết lại (114 → 118 dòng, đảo thứ tự) thì mọi neo **vỡ IM LẶNG**: builder
vẫn chạy, clip vẫn đủ giây, chỉ có hình rơi vào sai câu (`feedback_builder_neo_dong_kiem_timeline_truoc`).

Luật hình thi hành: **footage chỉ đứng ở dòng KHÔNG có số; mọi dòng có số → thẻ.**
Đo trên chính script: v21 cũ footage 74,0% / thẻ 26,0% (bản user chê "ảnh vô nghĩa")
→ bản này **50,1% / 49,9%**. Gate: `_media_library/check_footage_ratio.py`.

⚖️ YMYL: mọi con số trên thẻ đều lấy **từ chính lời đọc**. Phép tính nào có trên thẻ
cũng là phép tính lời đọc nói ra (110万＋95万＝205万 · 39万×5,105％ · 3万2500×2＝6万5000),
không thêm một số nào mới — cùng nguyên tắc LUẬT BA KHỐI của `stage-zu-layout.md` §2.
"""
import io
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
CLIPS = os.path.join(VD, "clips21b")
GENTEN_DIR = os.path.join(VD, "genten")
RV = os.path.join(os.path.dirname(PROJ), "remotion-vox")
OUTP = os.path.join(RV, "projects", "nenkin-21b")
# 🔴 Asset KHONG nam canh project.json — Remotion serve tu
#    `public/projects/<ten>/assets/` (kiem tren nenkin-21). Dat sai cho thi
#    render ra khung TRONG ma khong bao loi nao.
ASSETS = os.path.join(RV, "public", "projects", "nenkin-21b", "assets")

FPS, W, H = 30, 1920, 1080
FADE = 18
SRC_SEC = 8.0
CAP_MAX = 78
STAT_W = 1150

NL = "\n"

# ── NỘI DUNG THẺ ── khoá = chỉ số scene trong `scenes_plan.json`
# ("stat", body)   body = dòng `nhãn|số`, `*` đầu dòng = dòng được NHẤN
# ("formula", s)   toán tử để trần, hạng sau ＝ tự nhấn
# ("genten", [tên ảnh])
CARDS = {
 1:  ("stat", "1年で|2万円" + NL + "*20年で|40万円" + NL + "分けるのは|紙 1枚"),
 2:  ("stat", "暮らしは|年金だけ" + NL + "払っている所得税|0円" + NL + "*それでも|届きます"),
 4:  ("stat", "紙を|出し忘れた" + NL + "差は|年 2万円" + NL + "*戻ってくるのか|答えは後半で"),
 6:  ("stat", "いまの対象|年金を受け取るかた" + NL + "とくに|ご家族を扶養のかた"
              + NL + "*来年分から|148万円以上"),
 8:  ("stat", "年金の税金の線|覚えていますか" + NL + "*多くのかたの記憶|158万円から"
              + NL + "いまも同じか|確かめます"),
 10: ("genten", ["genten21_01", "genten21_02", "genten21_03"]),
 11: ("formula", "205万円 − 158万円 ＝ 47万円"),
 12: ("formula", "基礎控除 48万円 → 95万円"),
 13: ("formula", "110万円 ＋ 95万円 ＝ 205万円"),
 14: ("stat", "令和8年分|205万円" + NL + "令和9年分|214万円" + NL + "*1年で上がる分|9万円"),
 16: ("formula", "20万円 × 12か月 ＝ 240万円"),
 17: ("stat", "高橋さんの年金|240万円" + NL + "線|205万円" + NL + "*超えるので|所得税がかかる"),
 19: ("stat", "① 支給額から|社会保険料を引く" + NL + "② そこから|各種控除額を引く"
              + NL + "*③ 残った額に|5.105％"),
 20: ("formula", "39万円 × 5.105％ ≒ 1万9900円"),
 22: ("formula", "3万2500円 ＋ 3万2500円 ＝ 月 6万5000円"),
 23: ("formula", "78万円 × 5.105％ ≒ 3万9800円"),
 25: ("formula", "5％ ＋ 2.1％分 ＝ 5.105％"),
 27: ("genten", ["genten21_04", "genten21_05"]),
 30: ("stat", "*高橋さんの差|年 2万円" + NL + "月にすると|約 1700円" + NL + "20年で|40万円"),
 34: ("genten", ["genten21_06", "genten21_07"]),
 36: ("stat", "還付の申告|翌年1月1日から" + NL + "*できる期間|5年間"
              + NL + "5年前の分まで|いまからでも"),
 38: ("stat", "年金の収入|400万円以下" + NL + "それ以外の所得|20万円以下"
              + NL + "*両方みたすと|申告しなくてよい"),
 39: ("genten", ["genten21_08", "genten21_09", "genten21_10"]),
 41: ("stat", "*出し忘れた2万円|戻ってきます" + NL + "ただし|自分から確定申告"
              + NL + "黙っていると|そのまま"),
 43: ("stat", "配偶者|月 3万2500円" + NL + "70歳以上の配偶者|月 4万円"
              + NL + "扶養しているご家族|月 3万2500円" + NL + "*障害のあるかた|月 2万2500円〜"),
 45: ("formula", "線は 205万円　158万円は古い"),
 46: ("stat", "二 来年分|214万円に上がる" + NL + "*三 税率|5.105％ で同じ"
              + NL + "変わるのは|引ける控除"),
 47: ("formula", "年 2万円 × 20年 ＝ 40万円"),
 48: ("stat", "五 出し忘れても|5年以内なら戻る" + NL + "方法は|確定申告"
              + NL + "*ただし|自分から出したときだけ"),
 49: ("stat", "みっつ目の確認|出し忘れた年は？" + NL + "*5年以内なら|いまからでも"
              + NL + "取り戻せるのは|年 2万円 × 年数"),
}


def _wide(s, size):
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s) * size * 1.02


def _stat_ink(body, size):
    m = 0.0
    for row in body.split(NL):
        row = row.strip().lstrip("*")
        if row:
            m = max(m, _wide(row.replace("|", "  "), size) + 90)
    return m


def stat_size(body):
    rows = len([r for r in body.split(NL) if r.strip()])
    size = {1: 60, 2: 58, 3: 56, 4: 50}.get(rows, 48)
    while size > 40 and _stat_ink(body, size) * 1.06 > STAT_W:
        size -= 2
    return size


def formula_size(s):
    size = 80
    while size > 44 and _wide(s, size) * 1.06 > 1150:
        size -= 4
    return size


def split_caption(text, t0, t1):
    if len(text) <= CAP_MAX:
        return [(text, t0, t1)]
    parts, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。、」）" and len(cur) >= CAP_MAX * 0.55:
            parts.append(cur); cur = ""
        elif len(cur) >= CAP_MAX:
            parts.append(cur); cur = ""
    if cur:
        parts.append(cur)
    tot = sum(len(p) for p in parts) or 1
    out, t = [], t0
    for p in parts:
        d = (t1 - t0) * len(p) / tot
        out.append((p, t, t + d)); t += d
    return out


def link(src, dst):
    if os.path.exists(dst):
        if os.path.getmtime(dst) >= os.path.getmtime(src):
            return
        os.remove(dst)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def f(sec):
    return int(round(sec * FPS))


def main():
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]
    scenes = json.load(io.open(os.path.join(VD, "scenes_plan.json"), encoding="utf-8"))
    os.makedirs(ASSETS, exist_ok=True)
    A = ASSETS

    # ── clip footage theo THỨ TỰ shot A01..A54 ──
    shots = sorted(x for x in os.listdir(CLIPS) if x.endswith(".mp4"))
    assert shots, "chưa ingest clip vào clips21b"
    for s in shots:
        link(os.path.join(CLIPS, s), os.path.join(A, s))
    link(os.path.join(VD, "voice_full.wav"), os.path.join(A, "voice.wav"))
    for g in os.listdir(GENTEN_DIR):
        if g.endswith(".png"):
            link(os.path.join(GENTEN_DIR, g), os.path.join(A, g))

    vid, gen, stat_c, form_c = [], [], [], []
    si = 0                                  # con trỏ shot footage
    n_missing_card = []
    for idx, sc in enumerate(scenes):
        t0 = sc["start"]
        # 🔴 Ranh scene tinh den DAU SCENE SAU, khong den `end` cua chinh no. Giua hai
        #    dong loi co khoang NGHI (0,4-0,6s); lay `end` thi khoang do khong ai phu
        #    va no nhap vao khe "frame dung yen" cua gate. Do duoc: scene 26 dai 26,5s
        #    -> 3 shot (seg 8,83s) nhung khe THAT tu shot cuoi den su kien ke tiep la
        #    **9,43s** => gate do dung 0,4s. Tinh den 27,1s thi ra 4 shot, het.
        t1 = scenes[idx + 1]["start"] if idx + 1 < len(scenes) else sc["end"]
        dur = t1 - t0
        if sc["kind"] == "art":
            # ⭐ sàn 9,0s/ảnh chính (audience-45plus §2.0b): scene dài chia nhiều shot
            n = max(1, int(dur // 9) + 1)
            seg = dur / n
            # 🔴🔴 SHOT CUOI CUA SCENE CUNG CAN KEO DAI, neu SCENE KE TIEP la footage
            #    (bat 2026-09-07, soi frame 800s cua ban render 21b lan 1).
            #    Ban dau `nxt_foot = (k < n-1)` chi dung cho shot NAM TRONG cung scene
            #    => 5 moi noi o RANH GIOI hai scene `art` lien nhau co overlap = 0:
            #    v-25@441,6s · v-30@483,5s · v-33@507,9s · v-51@774,1s · v-54@799,9s.
            #    O do `fadeInFrames` mot minh chi lam clip hien dan LEN TU NEN KEM
            #    => 0,6s rua trang giua hai canh (dung bay da ghi o CLAUDE.md §②).
            #    Moi nao khe truoc la THE CHU thi fade len tu kem la DUNG thiet ke,
            #    nen chi xet scene ke tiep, khong keo bua.
            nxt_scene_art = (idx + 1 < len(scenes)
                             and scenes[idx + 1]["kind"] == "art")
            for k in range(n):
                if si >= len(shots):
                    break
                a = t0 + k * seg
                b = a + seg
                nxt_foot = (k < n - 1) or (k == n - 1 and nxt_scene_art)
                # 🔴 tinh bang FRAME da lam tron, dung tinh bang giay roi moi lam tron:
                #    `f(a) + f((b-a)+fade)` lech `f(b)+fade` toi 1 frame => 6 moi ra
                #    overlap 17 thay vi 18. Lay hieu hai moc da lam tron thi khop tuyet doi.
                fa, fb = f(a), f(b)
                dfr = (fb - fa) + (FADE if nxt_foot else 0)
                # 🔴 clip nguồn 8,0s: khe dài hơn thì LÀM CHẬM (cấm làm nhanh —
                #    speed>1 đẩy người xem tới phần "AI hết đà")
                d = dfr / FPS
                sp = min(1.0, SRC_SEC / d) if d > 0 else 1.0
                vid.append({"id": f"v-{si:02d}", "kind": "video",
                            "asset": f"assets/{shots[si]}",
                            "from": fa, "durationInFrames": max(2, dfr),
                            "fit": "cover", "volume": 0, "speed": round(sp, 3),
                            **({"fadeInFrames": FADE} if si else {})})
                si += 1
        else:
            card = CARDS.get(idx)
            if not card:
                n_missing_card.append((idx, sc["kind"], sc["lines"][0][:30]))
                continue
            kind, payload = card
            if kind == "genten":
                seg = dur / len(payload)
                for k, nm in enumerate(payload):
                    gen.append({"id": f"g-{idx}-{k}", "kind": "video",
                                "asset": f"assets/{nm}.png",
                                "from": f(t0 + k * seg),
                                "durationInFrames": max(2, f(seg)),
                                "fit": "cover", "volume": 0, "fadeInFrames": 18})
            elif kind == "stat":
                stat_c.append({"id": f"t-{idx}", "kind": "text", "from": f(t0),
                               "durationInFrames": max(2, f(dur)),
                               "content": payload, "preset": "papercut-stat",
                               "color": "#E0A32A", "animation": "pop",
                               "animationParams": {"restDeg": -1.5},
                               "layout": {"x": 455, "y": 409, "w": STAT_W},
                               "fontSize": stat_size(payload)})
            else:
                form_c.append({"id": f"t-{idx}", "kind": "text", "from": f(t0),
                               "durationInFrames": max(2, f(dur)),
                               "content": payload, "preset": "papercut-formula",
                               "color": "#E0A32A", "animation": "pop",
                               "animationParams": {"restDeg": -1.5},
                               "layout": {"x": 441, "y": 478, "w": 1150},
                               "fontSize": formula_size(payload)})

    # ── phụ đề: chẻ ≤78 ký (Remotion KHÔNG tự chẻ như video_render) ──
    cap = []
    over = 0
    for l in lines:
        for txt, a, b in split_caption(l["text"], l["start"], l["end"]):
            if len(txt) > CAP_MAX:
                over += 1
            # 聞き手 bọc 「」 để tách vai bằng MẮT, không chỉ bằng tai (49% mobile)
            t = f"「{txt}」" if l.get("spk") == "s2" and not txt.startswith("「") else txt
            cap.append({"text": t, "startMs": int(a * 1000), "endMs": int(b * 1000)})

    # 🔴 CLONE project MẪU, đừng tự dựng JSON từ đầu. CLAUDE.md §② đã cảnh báo:
    #    *"Đọc `remotion-vox/src/schema/project.ts` trước khi sinh JSON, đừng suy từ
    #    project mẫu"* — tao vừa dính đúng lỗi đó: dựng theo trí nhớ ra `{fps, width,
    #    durationInFrames, tracks}` phẳng, trong khi schema thật là
    #    `{version, meta, timeline, sceneMarkers, tracks, captions, theme}` với clip
    #    dùng `kind`+`asset` (không phải `src`). Gate `check_frame_pace` nổ KeyError,
    #    và Remotion cũng sẽ không đọc nổi. Clone mẫu là cách duy nhất chắc đúng schema.
    # 🔴 Suy đường dẫn từ OUTP, KHÔNG gõ literal có backslash: chuỗi
    #    `...\remotion-vox...` trong heredoc biến `\r` thành CARRIAGE RETURN
    #    và cắt đứt dòng code. Cùng họ bẫy escape đã dính ở `\n`.
    TPL = os.path.join(os.path.dirname(OUTP), "nenkin-21", "project.json")
    proj = json.load(io.open(TPL, encoding="utf-8"))
    proj["meta"]["name"] = "nenkin-21b"
    proj["timeline"]["durationInFrames"] = f(total) + 6
    proj["sceneMarkers"] = [
        {"id": f"sc-{i}", "atFrame": f(sc["start"]),
         "label": sc["lines"][0][:22]} for i, sc in enumerate(scenes)]
    by_id = {t["id"]: t for t in proj["tracks"]}
    by_id["trk-bg"]["clips"][0]["durationInFrames"] = f(total) + 6
    by_id["trk-video"]["clips"] = vid
    by_id["trk-genten"]["clips"] = gen
    by_id["trk-stat"]["clips"] = stat_c
    by_id["trk-formula"]["clips"] = form_c
    by_id["trk-voice"]["clips"] = [{"id": "v", "kind": "audio", "from": 0,
                                    "durationInFrames": f(total),
                                    "asset": "assets/voice.wav", "volume": 1,
                                    "trimStartFrames": 0}]
    if "trk-bgm" in by_id:
        by_id["trk-bgm"]["clips"] = []          # BGM gắn sau ở khâu mux
    proj["captions"]["lines"] = cap
    proj["captions"]["words"] = []
    os.makedirs(OUTP, exist_ok=True)
    io.open(os.path.join(OUTP, "project.json"), "w", encoding="utf-8").write(
        json.dumps(proj, ensure_ascii=False, indent=1))

    fs = sum(c["durationInFrames"] for c in vid)
    cs = sum(c["durationInFrames"] for c in gen + stat_c + form_c)
    print(f"── build 21b ── {total/60:.2f}′ · {len(scenes)} scene")
    print(f"   footage {len(vid)} clip ({fs/FPS:.0f}s) · 原典 {len(gen)} · "
          f"bảng {len(stat_c)} · công thức {len(form_c)}")
    print(f"   tỉ lệ hình: footage {fs/(fs+cs)*100:.1f}% / thẻ {cs/(fs+cs)*100:.1f}%")
    print(f"   phụ đề {len(cap)} khối · vượt {CAP_MAX} ký: {over}")
    if over:
        print(f"  🔴 {over} khối phụ đề vượt {CAP_MAX} ký")
    if n_missing_card:
        print(f"  🔴 {len(n_missing_card)} scene THẺ chưa có nội dung trong CARDS:")
        for i, k, t in n_missing_card:
            print(f"       scene {i:02d} ({k}) {t}")
    if si < len(shots):
        print(f"  ⚠️  còn {len(shots)-si} clip footage chưa dùng")

    # ── GATE A: LUẬT BA KHỐI cho bảng số (audience-45plus §2.0c) ─────────────
    # Bảng 1–2 dòng thì hai dòng chữ trôi giữa khung kem trống = đúng cái user
    # kết án là "nói với nền trống". Gate ③ của check_frame_pace KHÔNG thấy: nó
    # chỉ hỏi "scene có gì ở vùng giữa không" — có, nên báo sạch.
    # ⚠️ Dòng thêm vào phải CHỞ NGHĨA THẬT: số học từ chính số đã có trên thẻ,
    #    hoặc mặt còn lại của điều vừa nói. CẤM bịa số/chế độ để lấp chỗ (YMYL).
    thin = [(c["id"], len([r for r in c["content"].split(NL) if r.strip()]))
            for c in stat_c
            if len([r for r in c["content"].split(NL) if r.strip()]) < 3]
    if thin:
        print(f"  🔴 GATE BA KHỐI: {len(thin)}/{len(stat_c)} bảng <3 dòng "
              f"— thêm dòng chốt chở nghĩa thật (audience-45plus §2.0c)")
        for i, r in thin:
            print(f"       {i}: {r} dòng")

    # ── GATE B: mối cross-dissolve giữa hai clip footage phải CÓ OVERLAP ─────
    vs = sorted(vid, key=lambda c: c["from"])
    seam = []
    for i in range(1, len(vs)):
        pv, cu = vs[i - 1], vs[i]
        fi = cu.get("fadeInFrames", 0)
        ov = (pv["from"] + pv["durationInFrames"]) - cu["from"]
        # ov < 0 = có khe (thẻ chữ chen giữa) ⇒ fade lên từ kem là ĐÚNG, bỏ qua
        if fi and 0 <= ov < fi:
            seam.append((cu["id"], round(cu["from"] / FPS, 1), ov, fi))
    if seam:
        print(f"  🔴 GATE DISSOLVE: {len(seam)} mối footage→footage thiếu overlap "
              f"⇒ {FADE/FPS:.1f}s rửa trắng lên nền kem")
        for i, t, ov, fi in seam:
            print(f"       {i} @{t}s  overlap {ov}/{fi}")

    # ── GATE C: cỡ chữ bảng (tệp 45+) ───────────────────────────────────────
    small = [(c["id"], c["fontSize"]) for c in stat_c if c["fontSize"] < 48]
    if small:
        print(f"  ⚠️  {len(small)} bảng có cỡ chữ <48 sau khi tự co: {small}")

    print(f"→ {os.path.join(OUTP, 'project.json')}")
    return 1 if (over or n_missing_card or thin or seam) else 0


if __name__ == "__main__":
    sys.exit(main())
