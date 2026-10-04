# -*- coding: utf-8 -*-
"""
prompts_pension.py — viet TAY 66 prompt i2v cho "PENSION RESEARCH LAB: THE TWO PAYMENTS",
roi ghi vao jobs.jsonl (giu nguyen `asset` da ghep bang MD5 + field `pick` neu co).

    python tools/prompts_pension.py <outdir cua story_extract.py>

🔴 VI SAO PHAI VIET TAY: `story_extract.sanitize()` chi BO duoc phan camera cua
   `motionDescription` do Flow soan; phan con lai thuong la MO TA KHUNG
   ("A medium close-up focusing on Katsuo"), khong phai chuyen dong. Do that: 58/66 shot
   bi gan ⚠. Voi i2v thi khung DA BI ANH KHOA — prompt chi con mot viec: noi CAI GI DONG.

🔴🔴 BAN v1 CUA CHINH FILE NAY DA SAI VA USER BAT DUNG (2026-09-10):
   *"tao muon hanh dong va video sinh dong len, chu khong phai may cai hanh dong nhat nheo"*.
   66 prompt cu deu ket bang "then it holds still" / "nothing else moves", va DUOI prompt con
   ghi "once, slowly, and it holds still for the rest of the shot" — tuc chinh cai duoi do EP
   video phai dung yen. Ket qua: 66 clip "ai do tho mot cai".
   ⇒ Sua CA HAI: duoi prompt bo menh de "holds still", va moi head viet lai theo khuon 3 NHIP
     cua `04_VIDEOGEN_PROMPTS.md` §1.1 (cong thuc chong "do do" da co san trong workspace).

📐 LUAT VIET — moi luat co MOT phep kiem trong check():
   ① chi ta CHUYEN DONG, khong ta lai quan ao/boi canh/khung  (anh lo hinh dang)
   ② khong mot tu nao ve MAY QUAY (zoom/pan/dolly/rack focus/camera/close-up)
   ③ ⭐ DUNG 3 NHIP = dung 2 dau ", then"  → mo · trien · KET
   ④ ⭐ nhip KET la CU CHI VUNG hoac THUA (vo tay 2 cai, xoa gay, liec di roi nhin lai,
      chinh lai chong giay von da thang) — day la cho "hon" nam
   ⑤ ⭐ >=1 CHUYEN DONG PHU trong khung (nang xe, bui bay, rem lay, sleeve, glint, la rung)
   ⑥ ⛔ CAM ket bang "holds still / nothing else moves / stops moving"
   ⑦ ⛔ khong bao gio ta CHU trong khung doi/xuat hien (Veo khong viet duoc chu Nhat)

⚖️ DANH DOI DA BIET TRUOC: dong nhieu hon = rui ro Veo lam hong tinh lien tuc cua vat cao hon
   (do that o video 21: 58/73 clip co thao tac tay voi vat nho, soi ky 4/6 hong). Nen "sinh dong"
   o day den tu THAN NGUOI + BOI CANH (tho, xoay vai, liec, nang, bui, tay ao), KHONG den tu
   viec them thao tac doi trang thai vat. Vat van chi doi trang thai DUNG MOT LAN moi shot.
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TAIL = (
    "Keep the framing, composition, characters, clothing, props and colours of the given image "
    "exactly as they are; the camera stays locked off and does not move, no zoom, no pan, no cut "
    "to another shot. The scene stays alive for the whole eight seconds: the motion above plays out "
    "in three unhurried beats and small natural movement continues right to the last frame. "
    "Any printing on paper or screens stays exactly as in the image; no new text appears, "
    "no captions, no watermark, no logo."
)

# ── 66 prompt, viet tay, 3 nhip, khoa theo id job ──────────────────────────────
HEADS = {
 "sb_01_s01sh01": "Katsuo lowers the passbook onto his knee and lets out a slow breath, then he rubs his thumb along its edge, then he glances at the window and back down while dust drifts through the bar of morning light",
 "sb_02_s01sh02": "Katsuo's jaw tightens as he keeps staring, then he swallows and blinks twice, then he tips his head a fraction as if reading it again while the window light shifts on his cheek",
 "sb_03_s01sh03": "the hands tighten on the passbook until the cover flexes, then the thumb smooths the open page flat, then the fingers tap the edge once and stay there as the paper trembles",
 "sb_04_s02sh01": "the hands lift the passbook a little closer and steady it, then the thumb slides along the open page, then the fingers shift their grip while the light in the blurred room behind brightens",
 "sb_05_s02sh02": "the thumb slides down the edge of the page and pauses, then it presses the paper flatter, then it lifts a fraction and hovers as a soft glint moves along the paper",
 "sb_06_s02sh03": "the page shifts a hair as the hands beneath it settle, then the paper flattens out, then a slow warm light moves across it and the fibres of the paper catch the glow",
 "sb_07_s03sh01": "the hands set the passbook down on the table and release it, then they smooth the cover once, then they withdraw to the table edge as Mitsue leans in and her sleeve brushes the wood",
 "sb_08_s03sh02": "Mitsue's finger settles on the entry and taps it once, then she turns her face toward Katsuo, then she looks back down while her cardigan sleeve slips at the wrist",
 "sb_09_s03sh03": "Katsuo shakes his head slowly, then he presses his lips together and looks further down, then he lifts one shoulder in a small shrug while Mitsue's sleeve slips at the wrist",
 "sb_10_s04sh01": "Mitsue leans closer to the calendar and her head tilts, then she raises a hand toward the marked date, then she lets the hand drop again as the page stirs in the draught",
 "sb_11_s04sh02": "the hand lifts the calendar page upward and holds it raised, then the paper bends and crinkles, then the fingers pinch the corner to steady it while the loose edge flutters",
 "sb_12_s04sh03": "the index finger slides across the row of dates and stops, then it taps one square twice, then it drifts back a little and rests as the paper flexes under it",
 "sb_13_s05sh01": "the light crosses both pages from one side and warms them, then a faint shadow drifts over the left page, then the glow evens out again across the desk",
 "sb_14_s05sh02": "the question mark firms up over the amber line, then it drifts a fraction as if breathing, then its edges soften while the light on the pages either side dims a shade",
 "sb_15_s05sh03": "the question mark swells with light, then it eases back and swells again more gently, then the glow spreads a little onto the pages around it",
 "sb_16_s06sh01": "Katsuo turns the calculator over in his hand, then he sets it down on his knee and exhales, then he rubs the back of his neck as the shoji light creeps across the mats",
 "sb_17_s06sh02": "Katsuo turns his head toward the window, then his eyes narrow slightly against the light, then he lets his shoulders drop and breathes out as the light moves on his face",
 "sb_18_s06sh03": "Katsuo shifts his weight where he sits, then he straightens his back a little, then he lets both hands fall into his lap while the light through the shoji screens fades",
 "sb_19_s07sh01": "the clerk gives a small nod, then she folds her hands on the counter, then she straightens a paper that is already straight as the office lights flicker faintly behind her",
 "sb_20_s07sh02": "the clerk pushes the form further forward, then she lets go and draws her hand back, then she turns her palm up in a small offering gesture while her sleeve brushes the counter",
 "sb_21_s07sh03": "the fingertip settles on the box and taps it, then it traces the edge of the box, then it lifts and hovers just above the paper while the page bows slightly",
 "sb_22_s08sh01": "the highlighted band on the page brightens, then it dims a shade, then a soft reflection slides across the glass of the monitor",
 "sb_23_s08sh02": "the cursor slides onto the link and stops, then the link brightens beneath it, then the cursor jitters a fraction while a faint reflection drifts across the glass",
 "sb_24_s08sh03": "the table settles into place on the screen, then its rows brighten one after another, then a faint reflection drifts across the monitor glass",
 "sb_25_s09sh01": "the arrows slide along the timeline toward the first date, then they slow and settle, then they pulse once together as a soft glow spreads under the row of dates",
 "sb_26_s09sh02": "the glow around the date swells, then it eases back, then it swells again more faintly while the arrows around it drift inward",
 "sb_27_s09sh03": "the gold arrow brightens from one end to the other, then the amber band beneath it warms up, then the whole glow breathes once and eases",
 "sb_28_s12sh01": "Katsuo taps the pen on the paper twice, then he slides the sheet toward Mitsue, then he sets the pen down and turns his hand over as Mitsue leans in and her sleeve settles on the table",
 "sb_29_s12sh02": "the pen tip moves under the final figure and stops, then it taps the paper once, then it lifts away while the sheet flexes and settles",
 "sb_30_s12sh03": "Mitsue's eyes widen a little, then she nods twice quickly, then she presses her lips together and looks up as a strand of hair shifts against her cheek",
 "sb_31_s13sh01": "the blurred people behind shift in their seats, then one of them rises and moves off, then the pool of light on the empty chair slides across the seat",
 "sb_32_s13sh02": "the long shadow stretches across the floor, then it slides on and thins, then it slips out of the frame as the light on the linoleum evens out",
 "sb_33_s13sh03": "a blurred figure crosses behind the chair, then the light on the seat brightens as they pass, then a faint draught moves the dust in the sunlit air",
 "sb_34_s14sh01": "the light creeps across the fanned documents, then one page edge lifts a fraction in the draught, then it settles back down and the shadow narrows",
 "sb_35_s14sh02": "the reading glasses lower toward the papers, then they swing gently from the hand that holds them, then they steady as a glint runs across one lens",
 "sb_36_s14sh03": "the glasses settle onto the certificate, then one arm rocks and comes down, then a glint slides along the lens while the paper beneath flattens",
 "sb_37_s15sh01": "Mitsue shifts the phone against her ear, then she looks further out of the window, then she brushes a strand of hair back as the garden greenery stirs behind the glass",
 "sb_38_s15sh02": "Mitsue's smile grows, then she nods slowly twice, then she lowers her eyes and keeps the smile while the light behind her shifts",
 "sb_39_s15sh03": "the bird folds its wings and settles, then it hops once along the stone, then it turns its head sharply while the leaves behind it stir",
 "sb_40_s16sh01": "the hand brings the stamp down toward the page and stops just above it, then it adjusts the angle a fraction, then it hovers and steadies as the passbook flexes",
 "sb_41_s16sh02": "the hand presses the stamp onto the paper, then it rocks the stamp slightly to spread the ink, then it keeps the pressure on while the page dips under it",
 "sb_42_s16sh03": "the hand lifts the stamp away, then it turns the stamp over in the fingers, then it sets it down beside the page as the fresh ink catches the light",
 "sb_43_s17sh01": "the light moves across both forms, then the edge of one sheet lifts slightly, then it eases back down as the shadow between them narrows",
 "sb_44_s17sh02": "the amber arrow grows from the left form toward the right, then its head firms up, then it pulses once as a soft glow spreads under both sheets",
 "sb_45_s17sh03": "the green tone washes across the right side, then it deepens a little, then it breathes once and eases while a soft glow lingers along the divide",
 "sb_46_s18sh01": "the clerk's hands slide the brochure across the counter, then they release it and draw back, then one finger returns to nudge it square as the paper skids to a stop",
 "sb_47_s18sh02": "the finger comes down onto the printed number, then it presses the paper flat, then it lifts a fraction and hovers as the brochure bows under it",
 "sb_48_s18sh03": "the finger taps the number twice, then it drags a short way across the page, then it lifts away as the paper springs back",
 "sb_49_s19sh01": "Katsuo squares one stack of documents, then he lays a second sheet on top of it, then he pats the pile twice while the shoji light shifts across the mats",
 "sb_50_s19sh02": "Katsuo lowers the lid of the wooden box, then he presses it down at one corner, then he rests his palm flat on the lid and leaves it there",
 "sb_51_s19sh03": "Katsuo pushes the box onto the shelf, then he straightens it with two fingers, then he lets his hand fall and shifts his weight back as the shoji light moves on the shelf",
 "sb_52_s20sh01": "the screen brightens in the hand, then the hand tilts the phone a fraction, then the thumb settles at the edge of the screen as the glow spills onto the fingers",
 "sb_53_s20sh02": "the thumb comes down on the login button, then it presses and the button dips, then it lifts a little and hovers while the screen flares",
 "sb_54_s20sh03": "the blue light floods the screen, then it pulses once, then it eases to a steady glow while the reflection brightens on the face above",
 "sb_55_s21sh01": "both of them let out a breath and their shoulders drop, then Katsuo gives a small nod, then Mitsue's hand brushes his sleeve as the room brightens behind them",
 "sb_56_s21sh02": "the two of them turn their heads toward one another, then Mitsue's smile widens, then Katsuo dips his chin once as the light moves across their faces",
 "sb_57_s21sh03": "the two of them shift their weight side by side, then Katsuo turns slightly toward Mitsue, then he raises a hand and lets it fall as the golden light creeps across the floor",
 "sb_58_s22sh01": "the afternoon light creeps across the envelope, then the corner of the paper lifts a hair in the draught, then it eases back down and the shadow lengthens",
 "sb_59_s22sh02": "the light on the envelope dims, then a soft shadow slides over it, then the last warm edge of light slips off the paper",
 "sb_60_s22sh03": "the light drains from the envelope, then its shape dissolves into the dark, then the last faint edge fades out of the frame",
 "sb_61_s10sh01": "Mitsue lifts one folder and sets it on a neighbouring stack, then she squares the pile with both hands, then she pats it once while the shoji light shifts across the mats",
 "sb_62_s10sh02": "the hands slide the document into the clear sleeve, then they push it fully home, then they smooth the sleeve flat as the plastic crackles",
 "sb_63_s10sh03": "Mitsue lays the sleeve on top of the stack, then she squares it with her fingertips, then she draws her hands into her lap and looks down at the pile",
 "sb_64_s11sh01": "the loaded tray dips a fraction lower, then the beam rocks and eases, then the coins shift against one another while dust drifts through the light",
 "sb_65_s11sh02": "the slip of paper flutters down into the empty tray, then the tray drops under its weight, then the beam swings and the paper slides flat",
 "sb_66_s11sh03": "the two trays rock toward level, then they overshoot slightly and swing back, then they come level as the coins settle against the wood",
}

# ── GATE ───────────────────────────────────────────────────────────────────────
# ② may quay. 'tilt' KHONG chan tho: "her head tilts" la chu the nghieng dau, hop le —
#    chi la may quay khi co huong (tilt up/down) hoac chu ngu la camera/shot/frame.
CAM = re.compile(r"\b(camera|zoom|pans?|panning|dolly|dollies|crane|orbit|rack focus|"
                 r"push(?:es)? in|pull(?:s)? back|tracking shot|close[- ]up|wide shot|medium shot|"
                 r"tilt(?:s|ing)?\s+(?:up|down|left|right)|(?:shot|frame)\s+tilt(?:s|ing)?)\b", re.I)
# ⑥ ket dung yen — dung cai da lam 66 clip nhat nheo
DEAD = re.compile(r"(holds? still|stays? (?:still|put)|nothing else (?:moves|in the frame)|"
                  r"stops moving|everything holds|remains? (?:still|motionless))", re.I)
# ⑤ chuyen dong phu / boi canh song
LIFE = re.compile(r"\b(light|sunlight|shadow|dust|draught|breeze|glint|reflection|leaves|glow|"
                  r"steam|flutters?|crackles?|stirs?|sleeve|hair|flexes|bows|springs back|skids|"
                  r"trembles|dips|swings?|rocks?|flicker)\b", re.I)
TEXT_APPEAR = re.compile(r"\b(text|words?|letters?|numbers? (?:appear|change)|caption)\b", re.I)


def check(heads):
    bad = []
    for k, v in heads.items():
        n = v.count(", then")
        if CAM.search(v):
            bad.append((k, "② tu ve MAY QUAY: " + CAM.search(v).group(0)))
        if n != 2:
            bad.append((k, f"③ {n + 1} nhip (phai dung 3 = 2 dau ', then')"))
        if DEAD.search(v):
            bad.append((k, "⑥ ket DUNG YEN: " + DEAD.search(v).group(0)))
        if not LIFE.search(v):
            bad.append((k, "⑤ khong co chuyen dong phu nao (nang/bui/rem/sleeve/glint…)"))
        if TEXT_APPEAR.search(v):
            bad.append((k, "⑦ ta CHU doi/xuat hien: " + TEXT_APPEAR.search(v).group(0)))
        if not (90 <= len(v) <= 230):
            bad.append((k, f"do dai {len(v)} ky (nham 90–230)"))
    return bad


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    out = Path(sys.argv[1])
    jf = out / "jobs.jsonl"
    jobs = [json.loads(l) for l in io.open(jf, encoding="utf-8") if l.strip() and not l.startswith("#")]

    bad = check(HEADS)
    print(f"prompt viet tay: {len(HEADS)} | gate: {'SACH 6/6 lop' if not bad else str(len(bad)) + ' loi'}")
    for k, why in bad:
        print(f"   🔴 {k}: {why}")
    if bad:
        sys.exit(1)

    miss = [j["id"] for j in jobs if j["id"] not in HEADS]
    if miss:
        print(f"   🔴 {len(miss)} job KHONG co prompt viet tay: {miss[:6]}"); sys.exit(1)

    bak = jf.with_suffix(".jsonl.bak_auto")
    if not bak.exists():
        bak.write_bytes(jf.read_bytes()); print(f"   backup -> {bak.name}")

    with io.open(jf, "w", encoding="utf-8", newline="\n") as fh:
        for j in jobs:
            j["prompt"] = HEADS[j["id"]] + ". " + TAIL
            fh.write(json.dumps(j, ensure_ascii=False) + "\n")
    ln = [len(HEADS[j["id"]]) for j in jobs]
    print(f"   -> {len(jobs)} job vao {jf}")
    print(f"   nhip: 3/3 moi shot · phan hanh dong {min(ln)}–{max(ln)} ky · asset+pick giu nguyen")


if __name__ == "__main__":
    main()
