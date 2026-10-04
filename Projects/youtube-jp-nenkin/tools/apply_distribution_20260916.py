# -*- coding: utf-8 -*-
r"""apply_distribution_20260916.py — thi hanh muc A + B1 cua ke hoach 2026-09-15.

MUC TIEU: day kenh ra khoi feed lanh "nam 65+ chung chung" bang cach tao chuoi
**年金 -> 年金** trong chinh kenh, va cho YouTube them tin hieu CHU DE.

VI SAO (so do 2026-09-15):
  · 94,7% view den tu feed lanh; AVP browse 15,4% vs RELATED 26,7% (chenh 1,7-2,6x)
  · hang xom RELATED cung ngach chi 8/25, con lai la bong chay/SKE48/drama
  · sub/view = 0,065% (8.000 view gan nhat de ra 1 sub) => NUT THAT CUA YPP LA SUB

⚖️ Tran da biet: o AVP 15% tren video 14', nguoi xem trung binh roi o ~2:06 => RAT IT nguoi
   toi duoc end screen. Nen thu cho duoc nhieu nhat la **link trong mo ta + playlist +
   binh luan ghim**, roi moi toi the/end screen (2 cai do khong co API, phai bam tay).

CHAY:
    python tools/apply_distribution_20260916.py              # dry-run TAT CA
    python tools/apply_distribution_20260916.py --desc       # chi xem phan mo ta
    python tools/apply_distribution_20260916.py --all --apply # ghi that

⛔ KHONG dung toi: trailer (dat 08-31, chua doc ket qua) · tieu de/thumbnail cua video dang
   hut view (lam hong ca phep do M1/M2 lan A/B G17).
"""
import argparse
import io
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[1]
yt = build("youtube", "v3",
           credentials=Credentials.from_authorized_user_file(
               str(ROOT / "credentials" / "token.json")))

# ── BA TRU + VIDEO NEO ─────────────────────────────────────────────────────
# 🔴 GAN LAI TRU: moi video gan day bi don het vao tru C (手取り), ke ca 緑の封筒 (giay den
#    -> tru B) va 60歳繰上げ (cach nhan -> tru A). Playlist-scoped autoplay chi co gia tri
#    khi playlist that su chat chu de.
# ⭐ VIDEO NEO = video co AVP CAO NHAT trong tru -> gui traffic toi noi giu duoc nguoi.
PILLARS = {
    "A": dict(pl="PLSHjlM17Oamc", name="年金はいくら？受け取り方で変わる金額",
              anchors=["pn9Fi9Bx6_U", "20xRYX-ra2U"],
              vids=["bWl2jE9l8z4", "uPlyzkGYfCs", "xWyfoi59uSs", "TTwuFmKa3T8",
                    "zoTNI9KWgCg", "pn9Fi9Bx6_U", "20xRYX-ra2U", "jhRgcIiqd_w",
                    "tsQwDqqreCM"]),
    "B": dict(pl="PLT4QEuxo4MWw", name="届く紙と期限｜給付金・公金受取口座・詐欺",
              anchors=["UzHj5gsqSVY", "cOpzaW2FYXc"],
              vids=["MfEKhbXdTXY", "n1eDEoHbEMM", "cOpzaW2FYXc", "zr9uJbDFaoU",
                    "KmmbwuRHBAg", "UzHj5gsqSVY", "BKKyjwd1WBU", "T69O1_ejplE",
                    "DA1ZO3tQubs"]),
    "C": dict(pl="PLZVtF_edAA5s", name="年金の手取り｜税金・介護保険料・住民税非課税",
              anchors=["ZbEwsPFCcAA", "S0j16selKvs"],
              vids=["H9WisP5rcgI", "KJicjlLpuP4", "S0j16selKvs", "ZbEwsPFCcAA",
                    "Qht_bfNun3s", "8pbdjPxw3ho"]),
}
OF = {v: k for k, p in PILLARS.items() for v in p["vids"]}

# ⭐ 3 hashtag dau hien NGAY TREN TIEU DE -> day la mot loi khai bao chu de, khong phai SEO.
TAGS3 = "#年金 #年金生活 #老後のお金"
MARK = "▼関連する研究ノート"

# ⭐ KEYWORDS — bo DUNG 6 tu NHAN KHAU/LOI SONG chung, GIU het thuc the trong ngach.
# 🔴 Ban dau tao bo ca `給付金` (do duoc **14,81**, tu cao thu HAI cua kenh), `国民年金`,
#    `厚生年金` — sai. Do la thuc the trong ngach, khong phai tu chung. Thu thuc su nuoi
#    bucket "nam 65+ chung chung" chi la 6 tu duoi: chung khong noi gi ve 年金, chung noi
#    ve MOT NHOM TUOI — va nhom tuoi la dung cai YouTube dang phan loai kenh nay theo.
DROP = {"シニア", "60代", "50代", "老後の生活費", "老後資金", "定年後"}
ADD = ("年金生活 老齢基礎年金 老齢厚生年金 加給年金 特別支給の老齢厚生年金 公金受取口座 "
       "年金振込通知書 扶養親族等申告書 住民税非課税 介護保険料 年金支給日").split()


def _titles():
    """videoId -> title, lay tu uploads playlist (KHONG tin so thu muc — no khong phai
    thu tu dang)."""
    up = yt.channels().list(part="contentDetails", mine=True).execute()[
        "items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    out, tok = {}, None
    while True:
        r = yt.playlistItems().list(part="snippet", playlistId=up, maxResults=50,
                                    pageToken=tok).execute()
        for i in r["items"]:
            out[i["snippet"]["resourceId"]["videoId"]] = i["snippet"]["title"]
        tok = r.get("nextPageToken")
        if not tok:
            return out


def block_for(vid, titles):
    """Khoi 関連 cua mot video: 2 video NEO cung tru + chinh playlist.

    🔴 Link phai co tham so `&list=` — cu bam se roi VAO TRONG playlist, nen cu autoplay
       KE TIEP cung nam trong ngach. Link tran thi autoplay tra ve feed chung.
    """
    k = OF.get(vid)
    if not k:
        return None
    p = PILLARS[k]
    picks = [a for a in p["anchors"] if a != vid]
    if len(picks) < 2:                       # video NEO thi lay ban cung tru khac
        picks += [v for v in p["vids"] if v != vid and v not in picks][:2 - len(picks)]
    lines = [MARK]
    for v in picks[:2]:
        lines.append(f"・{titles.get(v, v)[:38]}")
        lines.append(f"　https://www.youtube.com/watch?v={v}&list={p['pl']}")
    lines.append(f"・再生リスト「{p['name']}」")
    lines.append(f"　https://www.youtube.com/playlist?list={p['pl']}")
    return "\n".join(lines)


def new_desc(old, blk):
    """Chen khoi 関連 TRUOC khoi hashtag, va chuan hoa 3 hashtag dau.

    Giu nguyen moi thu khac cua mo ta (doc-sua-ghi ca snippet nhu `apply_channel_fix_20260830`).
    """
    d = old
    if MARK in d:                            # da co -> thay the khoi cu, khong nhan doi
        i = d.index(MARK)
        j = d.find("\n\n", i)
        d = d[:i] + blk + (d[j:] if j > 0 else "")
    else:
        i = d.rfind("\n#")
        d = (d[:i].rstrip() + "\n\n" + blk + "\n" + d[i:]) if i > 0 else d + "\n\n" + blk
    i = d.rfind("\n#")                       # chuan hoa 3 hashtag dau
    if i > 0:
        tail = d[i + 1:].split()
        keep = [t for t in tail if t.startswith("#") and t not in TAGS3.split()]
        d = d[:i + 1] + TAGS3 + (" " + " ".join(keep[:3]) if keep else "")
    return d


def do_desc(apply, titles):
    n = 0
    for vid in sorted(OF, key=lambda v: titles.get(v, "")):
        blk = block_for(vid, titles)
        sn = yt.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]
        body = {"id": vid, "snippet": {k: sn[k] for k in
                ("title", "description", "categoryId", "tags",
                 "defaultLanguage", "defaultAudioLanguage") if k in sn}}
        nd = new_desc(sn["description"], blk)
        if nd == sn["description"]:
            print(f"  = {vid} {sn['title'][:34]} — mo ta da dung")
            continue
        body["snippet"]["description"] = nd
        print(f"  {'APPLY' if apply else 'DRY  '} {vid} tru {OF[vid]} {sn['title'][:34]}")
        if apply:
            yt.videos().update(part="snippet", body=body).execute()
        n += 1
    print(f"  -> {n} video doi mo ta")


def do_playlists(apply):
    """Gan lai video vao dung tru. Doi tru = xoa item cu + chen moi."""
    for k, p in PILLARS.items():
        cur, tok = {}, None
        while True:
            r = yt.playlistItems().list(part="snippet", playlistId=p["pl"],
                                        maxResults=50, pageToken=tok).execute()
            for i in r["items"]:
                cur[i["snippet"]["resourceId"]["videoId"]] = i["id"]
            tok = r.get("nextPageToken")
            if not tok:
                break
        add = [v for v in p["vids"] if v not in cur]
        rem = [v for v in cur if v not in p["vids"]]
        print(f"  tru {k} {p['name'][:26]}: co {len(cur)} · them {len(add)} · bo {len(rem)}")
        for v in add:
            print(f"     + {v}")
            if apply:
                yt.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": p["pl"],
                    "resourceId": {"kind": "youtube#video", "videoId": v}}}).execute()
        for v in rem:
            print(f"     - {v}  (sang tru khac)")
            if apply:
                yt.playlistItems().delete(id=cur[v]).execute()


def do_keywords(apply):
    """🔴🔴 CHI IN RA DE CHEP TAY — `channels.update` KHONG ghi duoc keywords.

    Do ngay 2026-09-16: goi `channels().update(part="brandingSettings")` tra ve HTTP 200 va
    **response echo dung gia tri moi**, nhung `channels().list` doc lai ngay sau do van tra
    ve gia tri CU. YouTube nuot lenh ghi ma khong bao loi.
    ⇒ Neu tin response thi da ghi vao so la "xong" trong khi khong co gi doi.
       Cung ho voi bay da ghi o `media-library.md` §2.10 ⑤: **so do va exit code khong chung
       minh da ghi** — phai DOC LAI tu nguon.
    ⇒ Keywords phai sua TAY: Studio -> 設定 -> チャンネル -> 基本情報 -> キーワード.
    """
    ch = yt.channels().list(part="brandingSettings", mine=True).execute()["items"][0]
    old = ch["brandingSettings"]["channel"].get("keywords", "")
    kept = [w for w in old.split() if w not in DROP]
    new = kept + [w for w in ADD if w not in kept]
    s = " ".join(new)
    if len(s) > 500:
        print(f"  🔴 {len(s)} ky > tran 500 — cat bot ADD")
        return
    if s == old.strip():
        print("  ✅ keywords da dung")
        return
    print("  🔴 API KHONG GHI DUOC KEYWORDS (da do: response echo gia tri moi, doc lai van cu)")
    print("     -> SUA TAY: Studio > 設定 > チャンネル > 基本情報 > キーワード")
    print(f"     BO   ({len(DROP & set(old.split()))}): "
          f"{' '.join(sorted(DROP & set(old.split())))}")
    print(f"     THEM ({len([w for w in ADD if w not in kept])}): "
          f"{' '.join(w for w in ADD if w not in kept)}")
    print("\n     ===== CHEP NGUYEN KHOI DUOI DAY VAO O KEYWORDS =====")
    print("     " + s)
    print("     ====================================================")


def do_captions(apply):
    """Phu de la tin hieu chu de day nhat, va mien phi. Chi BAO CAO video thieu track `ja`
    — upload caption can file goc, de lam rieng sau khi biet thieu bao nhieu."""
    miss = []
    for vid in OF:
        try:
            it = yt.captions().list(part="snippet", videoId=vid).execute().get("items", [])
        except Exception as e:
            print(f"  ? {vid} khong doc duoc caption ({type(e).__name__})")
            continue
        if not any(c["snippet"]["language"].startswith("ja") for c in it):
            miss.append(vid)
    print(f"  thieu track `ja`: {len(miss)}/{len(OF)}")
    for v in miss:
        print(f"     {v}   srt: 07_UPLOADED/*/_upload/subs.srt")


def main():
    ap = argparse.ArgumentParser()
    for f in ("desc", "playlists", "keywords", "captions", "all"):
        ap.add_argument(f"--{f}", action="store_true")
    ap.add_argument("--apply", action="store_true", help="ghi that (mac dinh dry-run)")
    a = ap.parse_args()
    sel = {f: getattr(a, f) or a.all or not any(
        getattr(a, x) for x in ("desc", "playlists", "keywords", "captions", "all"))
        for f in ("desc", "playlists", "keywords", "captions")}

    print(f"=== {'APPLY — GHI THAT' if a.apply else 'DRY-RUN (them --apply de ghi)'} ===")
    titles = _titles()
    print(f"kenh co {len(titles)} video · bang tru phu {len(OF)}")
    orphan = [v for v in titles if v not in OF]
    if orphan:
        print(f"⚠️ {len(orphan)} video CHUA gan tru: {orphan}")

    if sel["playlists"]:
        print("\n[1] PLAYLIST theo tru")
        do_playlists(a.apply)
    if sel["desc"]:
        print("\n[2] MO TA — khoi 関連 (link co &list=) + 3 hashtag dau")
        do_desc(a.apply, titles)
    if sel["keywords"]:
        print("\n[3] CHANNEL KEYWORDS")
        do_keywords(a.apply)
    if sel["captions"]:
        print("\n[4] PHU DE `ja`")
        do_captions(a.apply)
    print("\nDONE", "(APPLY)" if a.apply else "(dry-run)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
