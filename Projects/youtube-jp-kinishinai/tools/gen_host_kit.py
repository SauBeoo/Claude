# -*- coding: utf-8 -*-
"""gen_host_kit.py — prompt clip NGUOI DAN NHEP MIENG cho MOT video (anh -> video, Veo/Dola), tieng = VOICEVOX.

Cach dung clip: model noi DUNG cau -> tat tieng no -> tools/lipsync_retime.py co gian tung doan hinh cho
moc tieng trung moc VOICEVOX cua chinh cau do (mieng mo dung luc giong minh noi).
Moi video MOT bo rieng (user 2026-10-01: khong tai su dung).
So luong: ~1 lan / 70-80s (mau ku8qF5wrFxg: 14 lan / 12,6 phut) · cau <= ~7s VOICEVOX · rai deu ca bai,
day hon o mo bai + ket bai (nhu mau).
Moi clip: CUNG anh goc 00_BRAND/host_kit/host_base.png · khung dung yen · <= 8s · cam chu + cam do quay phim.
Bai hoc: chu "tripod" -> model ve chan may vao hinh (test 2026-10-01) — gate chan chu nay.
Hai buoc, CAP THEO SO DONG (dong N anh <-> dong N video):
  1) host_IMG_FLOW.txt — anh khung dau (Image, kem host_base.png lam REFERENCE): doi CO CANH + net mat bat dau,
     cung nguoi / ao / phong / micro. Cau chu tu prompt v2 da qua bo loc (nhan vat HU CAU, mat nhin canh may).
  2) host_V_FLOW.txt  — anh -> video tu CHINH anh dong N, model noi dung cau.
Xuat: 06_VIDEO/<stem>/_plan/host_IMG_FLOW.txt + host_V_FLOW.txt + host_V_TENFILE.txt
Chay: python tools/gen_host_kit.py [--video 01_kuchiguse-hitonome]
"""
import sys, io, argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]

GUARD = ("NO TEXT ON SCREEN AND NO EQUIPMENT: no subtitles, no captions, no letters, no logos at any moment; "
         "no camera, no lights and no filming equipment anywhere in the frame — the only equipment is the small "
         "black desk microphone already in the picture.")
KEEP = ("Animate this exact photograph and keep it exactly as it is: the same fictional Japanese grandmother of "
        "about 68 with short silver hair in a neat bob, pearl earrings, a navy cardigan over a plain cream blouse, "
        "the same bright room with the same wooden bookshelf, plant and files behind her, the same desk. The framing "
        "stays perfectly still for the whole shot, nothing enters or leaves the frame.")
SPEAK = ("{mood} She speaks slowly and clearly in Japanese, in a soft warm voice of an elderly Japanese woman, saying "
         "exactly this and nothing else: {line} Her lips move clearly in sync with every word, with a short natural "
         "pause at each comma. After the last word she closes her lips and {end}")
TAIL = ("Her hands stay resting together on the desk; only her face, head and shoulders move a little, slowly and "
        "gently. Audio: only her voice and a faint quiet room tone, no music, no other voices. "
        "Keep the very bottom-right corner plain. No watermark, no text.")

IMG_HEAD = ("NO TEXT: no letters, no words, no numbers and no logos anywhere in the picture; every book spine, "
            "paper and screen is blank. A 16:9 photorealistic photograph in a natural documentary look of the same "
            "fictional character as in the reference image — same face, same hair, same clothes: a friendly Japanese "
            "grandmother of about 68 who hosts a calm radio talk programme, short soft silver hair in a neat bob, small "
            "pearl earrings, a navy cardigan over a plain cream blouse, no glasses. The same bright tidy room as the "
            "reference: a light wooden desk, a small black desk microphone on a short stand low to her right, below her "
            "chin, a soft-focus wooden bookshelf with plain files and a potted plant behind her, soft daylight from a "
            "window on the left, warm gentle colours, shallow depth of field.")
FRAMES = {   # nguoi luon o NUA PHAI, nua trai trong cho o chu (nhu mau)
    "M": "FRAMING: a medium shot from the chest up, she sits in the RIGHT third of the frame, the LEFT half open soft-focus bookshelf.",
    "C": "FRAMING: a closer shot from the shoulders up, her face larger in the RIGHT third of the frame, the LEFT half open soft-focus bookshelf.",
    "W": "FRAMING: a medium-wide shot from the waist up, the desk edge along the bottom, she sits in the RIGHT third, the LEFT half open bright room with the bookshelf.",
}
IMG_TAIL = ("Her face is turned towards the camera, clearly visible in soft even light, her eyes resting just beside the "
            "camera, lips gently closed, hands resting together on the desk. Evenly exposed into all four corners. "
            "Keep the bottom-right corner plain. No watermark, no signature, no text.")
# co canh tung lan xuat hien: xoay M-C-W, lan dau / lan cuoi = M (nhan dien), cau tam tinh = C
CUT = {"H01": "M", "H02": "M", "H03": "W", "H04": "C", "H05": "M", "H06": "W", "H07": "C", "H08": "M",
       "H09": "C", "H10": "C", "H11": "W", "H12": "M", "H13": "W", "H14": "M", "H15": "C"}

# (ma, moc trong video, cau — NGUYEN VAN nhu _TTS.md, cam xuc truoc khi noi, nhip ket sau cau)
V = {
    "01_kuchiguse-hitonome": [
        ("H01", "0:24", "「そんな夜に、心当たりはありませんか。」",
         "She looks towards the viewer with a quiet, understanding expression.", "gives one slow, knowing nod."),
        ("H02", "0:27", "「私は、ずっと、そうでした。デパートの売り場で三十四年、一日に何十回も、頭を下げてきた人間です。」",
         "She looks towards the viewer with a calm, slightly rueful smile.", "lowers her eyes for a moment, then looks up again."),
        ("H03", "1:46", "「家事をしながら、ラジオのように、気楽に聞いてくださいね。」",
         "She looks towards the viewer with a relaxed, friendly smile.", "gives one small easy nod, still smiling."),
        ("H04", "2:14", "「私が立っていたのは、デパートの呉服売り場です。今年、六十八になります。」",
         "She looks towards the viewer with a modest, fond smile, as if remembering.", "gives a small humble nod."),
        ("H05", "5:56", "「誰も、見ていませんでした。ちょっと、がっかりしたくらいです。」",
         "She looks towards the viewer, holding back a little laugh at herself.",
         "lets a small laugh escape through her nose and looks down with an embarrassed smile."),
        ("H06", "8:17", "「ご近所の次は、もっと近い人です。」",
         "She looks towards the viewer with a gentle, slightly more serious face.", "gives one small nod, as if to say: listen."),
        ("H07", "11:57", "「弱音を一つ言えた人には、弱音を言ってくれる人が、一人、増えます。」",
         "She looks towards the viewer with soft, kind eyes.", "holds a warm, reassuring smile."),
        ("H08", "12:03", "「ここまでで、いくつ当てはまりましたか。」",
         "She looks towards the viewer with a gentle, curious expression.", "tilts her head slightly, waiting kindly for an answer."),
        ("H09", "13:47", "「でも、七つ目だけは、どうしても、やめられなかったんです。」",
         "Her smile fades into a quieter, more serious look.", "keeps her eyes on the viewer, lips pressed gently together."),
        ("H10", "15:30", "「今日、ひとつだけ、我慢していることを、正直に言ってみてください。」",
         "She leans very slightly towards the viewer with a sincere, encouraging face.", "gives one slow encouraging nod."),
        ("H11", "15:49", "「では最後に、私の、今年のお正月の話をさせてください。」",
         "She settles in her chair with a fond, faraway smile.", "takes a small breath, as if the memory is coming back."),
        ("H12", "18:12", "「いかがでしたでしょうか。」",
         "She looks towards the viewer with a warm, calm face.", "holds a soft smile and nods once."),
        ("H13", "18:55", "「よろしければ、コメントで、そっと教えてください。」",
         "She leans very slightly towards the viewer with a gentle, inviting look.", "smiles softly and nods once."),
        ("H14", "19:00", "「よろしければ、チャンネル登録をして、また聞きにいらしてください。」",
         "She looks towards the viewer with a friendly, unhurried smile.", "gives a small polite bow of the head."),
        ("H15", "19:05", "「あなたが、あなたのままで、今日より少しだけ、楽に過ごせますように。」",
         "She looks towards the viewer with deep warmth, her eyes soft.", "holds a tender smile, eyes creasing, and nods slowly."),
    ],
}
DONE = {"01_kuchiguse-hitonome": {"H02": "Downloads/動画生成.mp4 (2026-10-01)"}}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--video", default="01_kuchiguse-hitonome")
    a = ap.parse_args()
    done = DONE.get(a.video, {})
    rows = []
    for code, at, line, mood, end in V[a.video]:
        p = " ".join([GUARD, KEEP, SPEAK.format(mood=mood, line=line, end=end), TAIL])
        assert p.find("NO TEXT") * 100 // len(p) <= 15, code
        assert "tripod" not in p.lower(), code
        assert p.count("「") == 1, code
        img = " ".join([IMG_HEAD, f"EXPRESSION: {mood}", FRAMES[CUT[code]], IMG_TAIL])
        assert img.find("NO TEXT") * 100 // len(img) <= 15 and "tripod" not in img.lower(), code
        rows.append((code, at, line, p, img))
    todo = [r for r in rows if r[0] not in done]
    vd = PROJ / "06_VIDEO" / a.video / "_plan"
    (vd / "host_V_FLOW.txt").write_text("\n".join(r[3] for r in todo) + "\n", encoding="utf-8")
    (vd / "host_IMG_FLOW.txt").write_text("\n".join(r[4] for r in todo) + "\n", encoding="utf-8")
    (vd / "host_V_TENFILE.txt").write_text(
        "dong | anh khung dau | clip tra ve | co canh | moc | cau\n" +
        "\n".join(f"{i:2d} | host_{c}.png | host_{c}.mp4 | {CUT[c]} | {at} | {l}"
                  for i, (c, at, l, _, _) in enumerate(todo, 1)) + "\n" +
        "".join(f"(da co) host_{k}: {x}\n" for k, x in done.items()), encoding="utf-8")
    print(f"{a.video}: {len(rows)} lan nguoi dan · can gen {len(todo)} (da co {len(done)}) -> {vd / 'host_V_FLOW.txt'}")


if __name__ == "__main__":
    main()
