# -*- coding: utf-8 -*-
"""BIEN DOI ACT VIDEO -> ACT ANH TINH (mot khoanh khac dong cung).

Moi act cua video 38 co dung cau truc:
    [A_XXX: ] b0 , then b1 , then b2 [, while <ambient>] [, as <dam dong>]
      b0 = BO CUC (cai gi lap day khung)      -> GIU, day la thu anh can
      b1 = HANH DONG (dinh cua canh)          -> GIU lam khoanh khac dong cung
      b2 = TRANG THAI KET (sau do)            -> BO, anh khong ke duoc "sau do"
      ambient / dam dong                      -> GIU nhung doi sang the TINH

NGOAI LE: b1 la CAMERA DI CHUYEN ("the view carries/turns/comes down...") thi anh
khong ve duoc => lay b2 (noi may DUNG LAI) lam khoanh khac. Do la ly do ham nay
khong phai mot cai split don gian.
"""
import re

# ── AMBIENT: 36 chuoi thuc te trong bai, doi sang the TINH ──────────────────────
AMB = {
 "the shadows of the roof beams lie across the floor":
   "long shadows of the roof beams lying across the floor",
 "the shadows under the table shift as the fluorescent light flickers overhead":
   "hard fluorescent light from overhead and black shadows under the table",
 "the shadow of the blanket lies still across his knees":
   "the shadow of the blanket lying across his knees",
 "the shadow of the blanket lies still over his knees":
   "the shadow of the blanket lying over his knees",
 "the shadow of his shoulders lies still on the wall":
   "the shadow of his shoulders thrown on the wall",
 "the shadow of his shoulders shifts on the wall beside them":
   "the shadow of his shoulders thrown on the wall beside them",
 "the shadow of his shoulders lies still on the wall and a small old radio rests on his lap under his other hand":
   "the shadow of his shoulders thrown on the wall and a small old radio resting on his lap under his other hand",
 "the shadow of her shoulders moves on the lit wall":
   "the shadow of her shoulders thrown on the lit wall",
 "the shadow of the roof beams moves across them":
   "the shadow of the roof beams lying across them",
 "the shadow of the cylinder shifts at the side of the frame":
   "the shadow of the cylinder lying at the side of the frame",
 "the shadow of the doorframe lies across the boards":
   "the shadow of the doorframe lying across the boards",
 "the shadow of the trolley shifts on the floor":
   "the shadow of the trolley lying on the floor",
 "the shadow from the high windows shifts a little":
   "a hard band of shadow from the high windows across the floor",
 "the wind blows the rain past the doorway beyond":
   "rain slanting past the doorway beyond",
 "the wind blows the rain in through the open doors":
   "rain slanting in through the open doors",
 "the wind blows the rain in behind him":
   "rain slanting in behind him",
 "the wind drives the rain down the high windows":
   "rain streaming down the high windows",
 "the wind drives the rain across the light over the door":
   "rain slanting across the light over the door",
 "the wind drives the rain against the roof outside":
   "rain lashing the roof outside",
 "the wind drives the rain across the roof":
   "rain lashing across the roof",
 "the wind pushes the rain in under the door":
   "a wet fan of rain spread in under the door",
 "the wind moves the bicycles along the kerb":
   "bicycles leaning over along the kerb in the wind",
 "the wind moves the awnings": "the awnings pulled taut in the wind",
 "the wind moves the awnings behind her": "the awnings pulled taut in the wind behind her",
 "the wind moves the puddles": "the puddles ruffled by the wind",
}
_DUST = re.compile(r"^dust turns in\b")


def _amb(t):
    t = t.strip()
    if t in AMB:
        return AMB[t]
    if _DUST.search(t):                      # 8 bien the "dust turns in ..."
        return t.replace("dust turns in", "dust hanging in", 1)
    for a, b in (("lie across", "lying across"), ("lies across", "lying across"),
                 ("lies still", "lying"), ("shifts", "lying"), ("moves", "lying")):
        t = t.replace(a, b)
    return t


# ── DAM DONG: phan lon da tinh san, chi bo ngon ngu MAY QUAY + vai dong tu ──────
_CROWD_FIX = [
 (r"\s+as the view passes", ""),
 (r"\bheads come up\b", "heads up"),
 (r"\bheads turn to follow\b", "heads turned to follow"),
 (r"\bcome up towards\b", "turned up towards"),
 (r"\bbegin(?:s)? to do the same\b", "doing the same"),
 (r"\bbegin(?:s)? (\w+ing)\b", r"\1"),
 (r"\bslows? (?:down )?to (?:look|watch|listen)\b", "stopped to watch"),
 (r"\bstops? to watch\b", "stopped to watch"),
 (r"\bstops? moving\b", "standing still"),
 (r"\bcloses? up\b", "closed up"),
 (r"\bopens? to let\b", "opened to let"),
 (r"\bmoves? (?:up|off|past|away)\b", "standing"),
 (r"\bgoe?s? quiet\b", "quiet"),
 (r"\bgoe?s? (?:completely )?still\b", "still"),
 (r"\bsettles?\b", "settled"),
 (r"\bgathers? round\b", "gathered round"),
 (r"\bstands? back\b", "standing back"),
 (r"\bsits? up\b", "sitting up"),
 (r"\bsit up\b", "sitting up"),
 (r"\bcrosse?s? the car park\b", "out across the car park"),
 (r"\bdraws? back\b", "drawn back"),
 (r"\bdraws? (?:in|their bedding in)\b", "drawn in"),
]


def _crowd(t):
    t = t.strip()
    for a, b in _CROWD_FIX:
        t = re.sub(a, b, t)
    return t


CAMMOVE = re.compile(
    r"\bthe view (?:carries|turns|moves|comes down|comes back|goes|dips|rises|follows|"
    r"swings|travels|holds|settles|stops)\b|\bthe whole view\b", re.I)

# ── cac cum CHUYEN TIEP -> the GIU NGUYEN TU THE ───────────────────────────────
_FREEZE = [
 (r"\b(?:it|the view) (?:stops|settles|holds) (?:on|where|at|short of|with) ",
  "the frame is held on "),
 (r"\b(?:it|the view) (?:stops|settles|holds)\b", "the frame is held there"),
 (r"\bthe view (?:carries|moves|travels) (?:along|towards|between|back along|down|up) ",
  "the frame looks along "),
 (r"\bthe view (?:turns|swings)(?: slowly)? (?:away from|towards|along|right to left|left to right) ",
  "the frame is turned towards "),
 (r"\bthe view comes (?:down|back|up)(?: the wall| along| to)? ", "the frame is on "),
 (r"\bcomes? into the frame and ", "is in the frame and "),
 (r"\bcomes? into the (?:far |near )?edge of the frame and ",
  "is at the edge of the frame and "),
 (r"\bcomes? into the frame\b", "is in the frame"),
 (r"\bcomes? into the (bottom|top|middle) of the (?:frame|view)\b",
  r"is in the \1 of the frame"),
 (r"\bgoes? out of (?:the frame|sight)\b", "is at the very edge of the frame"),
 (r"\bis gone past\b", "is at the far edge past"),
 (r"\bleaves? the frame\b", "is at the very edge of the frame"),
 (r"\bwithdraws? to\b", "held back at"),
 (r"\bdraws? back\b", "drawn back"),
 (r"\bsteps? back from\b", "standing back from"),
 (r"\bstraightens? and\b", "straightened up and"),
 (r"\bwalks? away from the camera\b", "caught mid-step with their back to us"),
 (r"\bwalks? towards the camera\b", "caught mid-step facing us"),
 (r"\bwalks? (?:the length of|along|down|up|across) ", "caught mid-step along "),
 (r"\bwalks? (from|into|towards|away|back|out|on|up|down|past) ", r"caught mid-step \1 "),
 (r"\bthey walk past\b", "they stand caught mid-step past"),
 (r"\bwalks?\b", "caught mid-step"),
 (r"\bcrosse?s? the (\w+) (?:outside )?left to right across the frame\b",
  r"caught mid-step across the \1"),
 (r"\bleft to right across the frame\b", "across the frame"),
 (r"\bright to left across the frame\b", "across the frame"),
 (r"\bfilmed from behind the whole time\b", "drawn from behind"),
 (r"\bfilmed over the shoulder\b", "drawn over the shoulder"),
 (r"\bfilmed\b", "drawn"),
 (r"\bseen from behind the whole time\b", "seen from behind"),
 (r"\bthe camera side\b", "the near side"),
 (r"\bwithout moving\b", "quite still"),
]


def freeze(t):
    for a, b in _FREEZE:
        t = re.sub(a, b, t, flags=re.I)
    t = re.sub(r"\s{2,}", " ", t).replace(" ,", ",")
    t = re.sub(r",\s*,", ",", t)
    return t.strip().strip(",").strip()


_HEAD = re.compile(r"^\s*(A_[A-Z0-9]+)\s*:\s*")


def to_still(act):
    """act video -> act anh tinh. Tra ve (act_moi, da_phai_dung_b2)."""
    m = _HEAD.match(act)
    head, body = (m.group(0), act[m.end():]) if m else ("", act)

    amb = crowd = ""
    mw = re.search(r",\s*while\s", body)
    if mw:
        tail = body[mw.end():]
        body = body[:mw.start()]
        ma = re.search(r",\s*as\s", tail)
        if ma:
            crowd = _crowd(tail[ma.end():])
            tail = tail[:ma.start()]
        amb = _amb(tail)

    b = body.split(", then ")
    b0 = b[0]
    b1 = b[1] if len(b) > 1 else ""
    b2 = b[2] if len(b) > 2 else ""

    used_b2 = False
    peak = b1
    if not peak or CAMMOVE.search(b1):
        if b2:
            peak, used_b2 = b2, True

    # b2 hay bi LUOC CHU NGU ("stops where...", "settles on...") — do la cu dat khung
    if used_b2:
        peak = re.sub(r"^(?:stops|settles|holds)(?:\s+(?:on|where|at|with))?\s+",
                      "the frame is held on ", peak, flags=re.I)
        peak = re.sub(r"^(?:stops|holds)\s+short of\s+",
                      "the frame stops just short of ", peak, flags=re.I)
    # "stops ..." trong canh CO BUOC CHAN: day moi la trang thai that cua khung hinh
    peak = re.sub(r"^stops\s+(at|in|beside|by|before|halfway|short)\b",
                  r"stands quite still \1", peak, flags=re.I)

    b0f, peakf = freeze(b0), freeze(peak)
    out = b0f
    if peakf and peakf.lower() not in b0f.lower():
        joiner = ", and " if re.match(
            r"^(?:the frame|he |she |they |it |a |an |the )", peakf, re.I) else " and "
        out = b0f + joiner + peakf
    # mot nguoi khong the vua DANG BUOC vua DUNG YEN — bo cai buoc chan di
    if re.search(r"stands quite still|the frame is held on|the frame stops just short", out):
        out = re.sub(r"caught mid-step (?:along|from|into|towards|away|back|out|on|up|down|past) ",
                     "", out)
        out = out.replace("caught mid-step ", "")
    if amb:
        out += ", with " + amb
    if crowd:
        out += ", and " + crowd
    return head + out, used_b2
