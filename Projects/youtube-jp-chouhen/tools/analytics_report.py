# -*- coding: utf-8 -*-
"""
analytics_report.py — kéo số liệu video đã đăng của kênh về terminal (YouTube Data API).

Chạy được NGAY với token hiện có (scope youtube.readonly) — KHÔNG cần chờ audit
(audit chỉ chặn upload public, không chặn đọc). Quota ~3-5 units/lần chạy.

Số lấy được: ngày đăng · trạng thái · views · likes · comments · duration.
Video mới đăng <72h được đánh dấu 🔥 (cửa sổ vàng cần theo dõi + đúng lúc so giờ vàng).

✅ --video <slug|ID>: kéo cả impressions + CTR (表示回数/クリック率), nguồn traffic
(search/suggested/browse), keyword search dẫn vào, retention theo vị trí — cần token có
scope yt-analytics.readonly. Impressions/CTR trễ ~2-3 ngày (video mới thường trống).

Dùng:
  python tools/analytics_report.py                     # kênh chouhen
  python tools/analytics_report.py --channel shokutaku # kênh khác (cần token của kênh đó)
  python tools/analytics_report.py --all               # mọi kênh đã có token
  python tools/analytics_report.py -n 20               # 20 video gần nhất
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent))

from upload_pack import CHANNELS, PROJECTS_ROOT, find_script, parse_ctr
from upload_api import get_creds, get_service


def _dur_seconds(iso: str) -> int:
    import re as _re
    m = _re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def _resolve_video(yt, proj, ident: str):
    """ident = video ID 11 ký tự HOẶC slug local → tìm trên uploads playlist theo title chốt."""
    import re as _re
    if _re.fullmatch(r"[A-Za-z0-9_-]{11}", ident) and not _re.match(r"^\d\d_", ident):
        return ident
    script = find_script(proj, ident)
    if not script:
        sys.exit(f"❌ Không thấy script {ident} — đưa thẳng video ID 11 ký tự cũng được")
    want = (parse_ctr(script.read_text(encoding="utf-8")).get("title") or "").strip()
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    for it in yt.playlistItems().list(part="snippet,contentDetails", playlistId=pl,
                                      maxResults=50).execute().get("items", []):
        t = it["snippet"]["title"].strip()
        if t == want or (want and t.startswith(want[:30])):
            return it["contentDetails"]["videoId"]
    sys.exit(f"❌ Không thấy video nào trên kênh khớp title chốt của {ident} — video đã đăng chưa?")


def video_report(key: str, ident: str) -> None:
    """Mổ 1 video: số theo ngày + nguồn traffic + keyword search + đường retention."""
    from datetime import date
    from googleapiclient.discovery import build

    cfg = CHANNELS[key]
    proj = PROJECTS_ROOT / cfg["project"]
    creds = get_creds(proj)
    yt = get_service(proj)
    ana = build("youtubeAnalytics", "v2", credentials=creds)

    vid = _resolve_video(yt, proj, ident)
    v = yt.videos().list(part="snippet,statistics,contentDetails", id=vid).execute()["items"][0]
    sn, st = v["snippet"], v.get("statistics", {})
    dur = _dur_seconds(v["contentDetails"]["duration"])
    pub = sn["publishedAt"][:10]
    today = date.today().isoformat()
    print(f"\n══ {sn['title'][:60]}")
    print(f"   https://youtu.be/{vid} · đăng {pub} · {dur//60}'{dur%60:02d}\" · "
          f"views {st.get('viewCount', 0)} · like {st.get('likeCount', 0)} · cmt {st.get('commentCount', 0)}")

    def q(**kw):
        try:
            return ana.reports().query(ids="channel==MINE", startDate=pub, endDate=today,
                                       filters=f"video=={vid}", **kw).execute().get("rows") or []
        except Exception as e:
            print(f"   ⚠️ Analytics API lỗi: {e}")
            print("   → Token cũ chưa có quyền analytics? Xóa credentials/token.json rồi chạy lại auth_test.py")
            sys.exit(1)

    rows = q(metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained",
             dimensions="day", sort="day")
    if rows:
        print("\n   ── Theo ngày ──   views  phút-xem  xem-TB  %video  +sub")
        for d, vw, mw, avd, avp, sub in rows:
            print(f"   {d}      {vw:>5}  {mw:>8}  {int(avd)//60}'{int(avd)%60:02d}\"  {avp:>5.1f}%  {sub:>4}")
        tot_v = sum(r[1] for r in rows)
        tot_m = sum(r[2] for r in rows)
        avg_p = sum(r[4] * r[1] for r in rows) / tot_v if tot_v else 0
        print(f"   TỔNG           {tot_v:>5}  {tot_m:>8}          {avg_p:>5.1f}%")

    try:
        r_imp = ana.reports().query(ids="channel==MINE", startDate=pub, endDate=today,
                                    metrics="impressions,impressionsClickThroughRate",
                                    filters=f"video=={vid}").execute().get("rows") or []
        if r_imp and r_imp[0] and r_imp[0][0]:
            imp, ctr = r_imp[0][0], r_imp[0][1]
            print("\n   ── Impressions (số lần thumbnail được hiển thị) ──")
            print(f"   表示回数 {int(imp):>7}  ·  クリック率(CTR) {ctr:.2f}%")
        else:
            print("\n   ── Impressions ── (chưa có dữ liệu — trễ ~2-3 ngày, video mới thường trống)")
    except Exception:
        pass  # metric impressions có thể chưa bật với token/video quá mới → bỏ qua êm

    rows = q(metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType", sort="-views")
    if rows:
        print("\n   ── Nguồn traffic ──")
        for src, vw, mw in rows:
            print(f"   {src:<22} {vw:>5} views · {mw} phút")

    try:
        rows = ana.reports().query(ids="channel==MINE", startDate=pub, endDate=today,
                                   metrics="views", dimensions="insightTrafficSourceDetail",
                                   filters=f"video=={vid};insightTrafficSourceType==YT_SEARCH",
                                   sort="-views", maxResults=10).execute().get("rows") or []
        if rows:
            print("\n   ── Keyword search dẫn vào ──")
            for kw_, vw in rows:
                print(f"   「{kw_}」 {vw} views")
    except Exception:
        pass  # video chưa có search traffic → YouTube trả lỗi/rỗng, bỏ qua

    rows = q(metrics="audienceWatchRatio", dimensions="elapsedVideoTimeRatio")
    if rows:
        print("\n   ── RETENTION (khán giả còn lại theo vị trí video) ──")
        prev = None
        for ratio, watch in rows:
            pct = int(float(ratio) * 100)
            if pct % 5 == 0:  # in mỗi mốc 5%
                t = int(float(ratio) * dur)
                bar = "█" * max(1, int(watch * 40))
                mark = ""
                if prev is not None and prev - watch > 0.08:
                    mark = "  ⚠️ RỚT MẠNH"
                if abs(float(ratio) - 0.5) < 0.03:
                    mark += "  ← vùng CTA"
                print(f"   {pct:>3}% ({t//60:>2}'{t%60:02d}\") {watch*100:>5.1f}% {bar}{mark}")
                prev = watch
    else:
        print("\n   (Chưa có dữ liệu retention — video ít view/mới đăng, YouTube cần thêm data)")


def report(key: str, n: int) -> None:
    cfg = CHANNELS[key]
    proj = PROJECTS_ROOT / cfg["project"]
    token = proj / "credentials" / "token.json"
    if not token.exists():
        print(f"▶ {cfg['name']} [{key}]: chưa có token API (auth_test.py) — bỏ qua")
        return
    yt = get_service(proj)
    ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
    stats = ch["statistics"]
    print(f"\n▶ {ch['snippet']['title']} [{key}] — sub: {stats.get('subscriberCount', '?')} · "
          f"tổng view: {stats.get('viewCount', '?')} · video: {stats.get('videoCount', '?')}")

    uploads_pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=uploads_pl,
                                    maxResults=min(n, 50)).execute().get("items", [])
    if not items:
        print("   (chưa có video)")
        return
    ids = ",".join(it["contentDetails"]["videoId"] for it in items)
    vids = yt.videos().list(part="snippet,statistics,contentDetails,status", id=ids).execute()["items"]

    now = datetime.now(timezone.utc)
    print(f"   {'Ngày đăng':<12}{'TT':<10}{'Views':>8}{'Like':>6}{'Cmt':>5}{'Dài':>8}  Title")
    for v in vids:
        sn, st, s = v["snippet"], v["status"], v.get("statistics", {})
        pub = sn.get("publishedAt", "")[:10]
        age_h = (now - datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))).total_seconds() / 3600 \
            if sn.get("publishedAt") else 9999
        hot = "🔥" if age_h < 72 else "  "
        dur = v["contentDetails"]["duration"].replace("PT", "").replace("H", "h").replace("M", "'").replace("S", '"').lower()
        privacy = st.get("privacyStatus", "?")
        if st.get("publishAt"):
            privacy = f"hẹn giờ"
        print(f" {hot}{pub:<12}{privacy:<10}{s.get('viewCount', '0'):>8}{s.get('likeCount', '0'):>6}"
              f"{s.get('commentCount', '0'):>5}{dur:>8}  {sn['title'][:48]}")


def main():
    ap = argparse.ArgumentParser(description="Số liệu video đã đăng (Data API)")
    ap.add_argument("--channel", default="chouhen", choices=sorted(CHANNELS))
    ap.add_argument("--all", action="store_true", help="mọi kênh đã có token")
    ap.add_argument("-n", type=int, default=10, help="số video gần nhất (mặc định 10)")
    ap.add_argument("--video", help="mổ 1 video cụ thể: slug local (vd 00_LEGACY_jikyu1350-haken) hoặc video ID")
    a = ap.parse_args()
    if a.video:
        video_report(a.channel, a.video)
        return
    for key in (sorted(CHANNELS) if a.all else [a.channel]):
        report(key, a.n)


if __name__ == "__main__":
    main()
