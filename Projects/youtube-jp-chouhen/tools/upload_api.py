# -*- coding: utf-8 -*-
"""
upload_api.py — upload video lên YouTube TỰ ĐỘNG qua YouTube Data API v3.

Làm trọn gói 1 lệnh: đọc gói CTR trong script → upload video (resumable) với
title/description/tags → set thumbnail → upload subs.srt → hẹn giờ công khai
(publishAt) theo .claude/rules/upload-schedule.md.

⚠️ Project Google Cloud CHƯA qua audit → video upload qua API bị KHÓA PRIVATE
   (không công khai được). Chỉ dùng chính thức sau khi audit đậu; trước đó chỉ
   chạy --dry-run hoặc test video nháp.

Chuẩn bị 1 lần / kênh: credentials/client_secret.json + chạy tools/auth_test.py
(tạo credentials/token.json). Mỗi kênh 1 project riêng — token nằm trong folder
project của kênh đó.

Dùng:
  python tools/upload_api.py 07_amamidokoro-saikaihatsu                # kênh chouhen
  python tools/upload_api.py <slug> --channel co-dai --slot "2026-07-20 17:00"
  python tools/upload_api.py <slug> --dry-run                          # kiểm tra, không upload
Quota mỗi lần: videos.insert 1600 + thumbnails.set 50 + captions.insert 400 ≈ 2050 units.
"""
import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent))

from upload_pack import (CHANNELS, PROJECTS_ROOT, append_image_credits, find_script,
                         find_srt, find_video_dir, fmt_slot, next_slot, parse_ctr,
                         scan_banned)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Bổ sung config API theo kênh (CHANNELS bên upload_pack lo lịch + checklist)
API_CFG = {
    "chouhen":   {"categoryId": "24", "lang": "ja", "caption_name": "日本語字幕"},
    # shokutaku: 26 → 27 = Education (SỬA 2026-08-09). ĐO THẬT hôm đó: 3/3 kênh cùng ngách dùng
    # 27 — 高齢者健康の真実 20/20 · 健康長寿の知恵袋TV 13/13 · 健康栄養研究室 9/9. Đồng thời 13 video
    # LIVE của kênh đang là cat 22 (căn cứ cũ: 長生きの秘訣 12/12 — kênh đó đã SỤP 45×, hết hạn)
    # → đã update cả 13 video sang 27 cùng lượt. ⚠️ 27 KHÔNG phải thuốc chữa BROWSE=0, chỉ là bỏ
    # một biến đang lệch so với ngách; xem Projects/youtube-jp-shokutaku/CLAUDE.md §2026-08-09.
    "shokutaku": {"categoryId": "27", "lang": "ja", "caption_name": "日本語字幕"},
    # health: 26 → 27 = Education (SỬA 2026-08-03, mổ lần 5 CHANNEL_DIAGNOSIS_2026-08-03.md).
    # ĐO THẬT: kênh chuẩn MỚI của ngách 高齢者健康の真実 (101 ngày → 13.700 sub / 1,2M view,
    # 6,3 video/tuần, xu hướng PHẲNG không sụp) dùng cat 27 ở 26/26 video. Cả 2 kênh copy
    # (健康長寿の知恵袋TV + 健康栄養研究室) và nagaiki cũng 27. 26 là số cũ chưa từng có kết quả.
    "health":    {"categoryId": "27", "lang": "ja", "caption_name": "日本語字幕"},
    "co-dai":    {"categoryId": "27", "lang": "ja", "caption_name": "日本語字幕"},
    "kr-romfan": {"categoryId": "24", "lang": "ko", "caption_name": "한국어 자막"},
    "stickman":  {"categoryId": "24", "lang": "vi", "caption_name": "Phụ đề tiếng Việt"},
    "nenkin":    {"categoryId": "27", "lang": "ja", "caption_name": "日本語字幕"},  # 27 = Education
    # kaigo: 26 = Howto&Style — ĐÃ ĐO 2026-07-25 qua API: 節約看護師りょう (748K sub, cùng tệp 50–60代 tiền,
    # cùng format long-form giải thích + số, hiệu suất/video cao nhất nhóm) dùng cat 26 ở 20/20 video.
    # KHÔNG dùng 24 (ケアまど đang chết) / 29 (みんなの給付金, lựa chọn lạ) / 27 (nenkin, chưa có kết quả chứng minh).
    # Bằng chứng: Projects/youtube-jp-kaigo/01_KEYWORD_RESEARCH.md §4.
    "kaigo":     {"categoryId": "26", "lang": "ja", "caption_name": "日本語字幕"},
    # akiya: 26 = Howto&Style — ĐÃ ĐO 2026-07-26 qua API: きな子のシニアお金ゼミ (167K sub, faceless VOICEVOX,
    # cùng tệp senior-money, view/video 146K = kênh duy nhất chứng minh được format ở ngách này) dùng cat 26 ở 12/12 video.
    # KHÔNG dùng 27 (あまおう — 1 video/ngày mà view 1,3–32K) / 22 (勝部 — đang sụt).
    # Bằng chứng: Projects/youtube-jp-akiya/01_KEYWORD_RESEARCH.md §3–4.
    "akiya":     {"categoryId": "26", "lang": "ja", "caption_name": "日本語字幕"},
    # nagaiki: 27 = Education — ĐÃ ĐO 2026-08-01 qua API: cả 2 kênh benchmark ngách 食べ合わせ
    # (健康栄養研究室 + 健康長寿の知恵袋TV — network đang nổ view, BENCHMARK_RIVALS_2026-07-29.md)
    # dùng cat 27 ở 5/5 video mới nhất mỗi kênh. KHÔNG copy 26 của health (đo ngách khác thời khác).
    "nagaiki":   {"categoryId": "27", "lang": "ja", "caption_name": "日本語字幕"},
}
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def get_creds(proj: Path):
    token = proj / "credentials" / "token.json"
    if not token.exists():
        sys.exit(f"❌ Chưa có {token} — chạy: python tools/auth_test.py --channel-dir {proj}")
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token.write_text(creds.to_json(), encoding="utf-8")
        else:
            sys.exit("❌ Token hết hạn không refresh được — xóa credentials/token.json rồi chạy lại auth_test.py")
    return creds


def get_service(proj: Path):
    return build("youtube", "v3", credentials=get_creds(proj))


def find_on_channel(yt, ch, title):
    """Có video nào trên kênh cùng tiêu đề chưa? (kể cả private/unlisted)

    So tiêu đề đã chuẩn hoá (bỏ khoảng trắng + hạ chữ) để không bị lệch vì 1 dấu cách.
    Quét uploads playlist = thấy cả video private, khác hẳn search.list (chỉ thấy public).
    """
    def norm(s):
        return "".join(s.split()).lower()
    want = norm(title)
    pl = yt.channels().list(part="contentDetails", id=ch["id"]).execute()
    pl = pl["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pl,
                                    maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    for i in range(0, len(ids), 50):
        v = yt.videos().list(part="snippet,status", id=",".join(ids[i:i + 50])).execute()
        for it in v["items"]:
            if norm(it["snippet"]["title"]) == want:
                return {"id": it["id"], "privacy": it["status"]["privacyStatus"],
                        "published": it["snippet"]["publishedAt"]}
    return None


def move_to_kho(proj, vdir, slug, channel):
    """06_VIDEO/<slug> → 07_UPLOADED/<slug> rồi prune.

    Dùng copytree + rmtree BEST-EFFORT thay cho shutil.move: file đang bị process khác
    giữ (log của chính wrapper, ffmpeg/VLC còn mở mp4) không được phép làm gãy cả khâu.
    shutil.move cũ fail giữa đường để lại NỬA folder ở 06 + NỬA ở 07 mà không nói gì.
    """
    import shutil
    dest_root = proj / "07_UPLOADED"
    dest_root.mkdir(exist_ok=True)
    dest = dest_root / slug
    if dest.exists():
        print(f"⚠️ {dest} đã tồn tại — KHÔNG move, xử lý tay.")
        return
    shutil.copytree(str(vdir), str(dest))          # bản kho ĐẦY ĐỦ trước, rồi mới xoá nguồn
    stuck = []
    shutil.rmtree(str(vdir), onexc=lambda fn, path, exc: stuck.append(path))
    print(f"— Đã chuyển kho: {dest}")
    if stuck:
        names = ", ".join(sorted({p.rsplit("\\", 1)[-1] for p in stuck}))
        print(f"⚠️ Còn sót ở {vdir} (file đang bị mở): {names}")
        print(f"   → Bản kho đã đủ. Xoá phần sót bằng tay khi đóng chương trình đang giữ file.")
    from upload_pack import finish_kho, move_related
    move_related(proj, slug, dest)   # script -> _scripts/ (giữ) + voice kr -> _voice/ (prune dọn)
    finish_kho(dest, channel)        # cắt video nặng, chỉ giữ metadata+subs+ảnh (+_scripts)


def main():
    ap = argparse.ArgumentParser(description="Upload YouTube full-auto qua Data API")
    ap.add_argument("slug")
    ap.add_argument("--channel", default="chouhen", choices=sorted(CHANNELS))
    ap.add_argument("--slot", help='giờ công khai "YYYY-MM-DD HH:MM" (giờ địa phương kênh); mặc định tự tính theo rule')
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"],
                    help="private + publishAt = hẹn giờ (mặc định); public = công khai ngay")
    ap.add_argument("--no-publish", action="store_true", help="KHÔNG hẹn giờ — để private trơn (video test)")
    ap.add_argument("--no-thumb", action="store_true")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--again", action="store_true", help="cho phép upload lại video đã có UPLOADED.txt")
    ap.add_argument("--allow-duplicate", action="store_true",
                    help="bỏ qua chặn 'kênh đã có video cùng tiêu đề' (thêm 2026-07-30 sau ca "
                         "upload trùng video 14 co-dai). Chỉ dùng khi CỐ Ý muốn 2 bản.")
    ap.add_argument("--dry-run", action="store_true", help="kiểm tra auth + metadata + file, không upload")
    a = ap.parse_args()

    cfg, api = CHANNELS[a.channel], API_CFG[a.channel]
    proj = PROJECTS_ROOT / cfg["project"]

    # --- metadata từ script (đúng nguồn với upload_pack) ---
    script = find_script(proj, a.slug)
    if not script:
        sys.exit(f"❌ Không thấy script {a.slug}.md trong {proj} (đã quét mọi 0N_SCRIPTS/)")
    text = script.read_text(encoding="utf-8")
    ctr = parse_ctr(text)
    title, description, tags = ctr["title"], ctr["description"], ctr["tags"]

    # --- assets ---
    vdir = find_video_dir(proj, a.slug)
    if not vdir:
        sys.exit(f"❌ Không thấy folder video {a.slug} trong {proj} (đã quét mọi 0N_VIDEO/)")
    marker = vdir / "UPLOADED.txt"
    if marker.exists() and not a.again and not a.dry_run:
        sys.exit(f"❌ Video này ĐÃ upload rồi:\n{marker.read_text(encoding='utf-8')}→ muốn đăng lại thật sự thì thêm --again")

    desc_file = vdir / "description_youtube.txt"
    if not description and desc_file.exists():  # format health: mô tả ở file riêng
        description = desc_file.read_text(encoding="utf-8").strip()
        ctr["desc3"] = "\n".join(description.splitlines()[:3])
        ctr["descf"] = description
    if not (title and ctr["descf"]):
        sys.exit("❌ Script thiếu title chốt / mô tả đầy đủ — đóng gói CTR trước.")

    hot = scan_banned(title, ctr["desc3"] or "")
    if hot:
        sys.exit(f"❌ TỪ NHẠY trong title/3 dòng đầu: {', '.join(hot)} — sửa script trước (youtube-compliance.md mục 3).")

    # ƯU TIÊN bản đã rename SEO trong _upload/ (youtube-upload-seo.md §1.1: YouTube quét
    # TÊN FILE GỐC làm tín hiệu ngữ cảnh đầu tiên). Trước 2026-07-30 tool lấy thẳng
    # <slug>.mp4 = tên thô "14_ka-hakko-trap" → mất tín hiệu mà upload_pack đã dựng sẵn.
    seo = sorted((vdir / "_upload").glob("*.mp4")) if (vdir / "_upload").is_dir() else []
    if seo:
        mp4 = max(seo, key=lambda p: p.stat().st_size)
        print(f"  (dùng tên file SEO: {mp4.name})")
    else:
        mp4 = vdir / f"{a.slug}.mp4"
        if not mp4.exists():
            cands = [p for p in vdir.glob("*.mp4") if "_test" not in p.name]
            if not cands:
                sys.exit(f"❌ Không thấy .mp4 trong {vdir}")
            mp4 = max(cands, key=lambda p: p.stat().st_size)
    srt = find_srt(proj, vdir, a.slug)
    thumb = next((p for p in (vdir / "thumbnail_scene.png", vdir / "thumbnail.png") if p.exists()), None)
    description, n_credit = append_image_credits(description, vdir)
    if n_credit:
        print(f"  (tự thêm credit {n_credit} ảnh CC BY vào 概要欄)")

    # --- validate giới hạn API (fail SỚM, trước khi tốn quota/băng thông) ---
    if len(title) > 100:
        sys.exit(f"❌ Title {len(title)} ký tự — YouTube max 100. Rút gọn trong script trước.")
    if len(description) > 5000:
        sys.exit(f"❌ Description {len(description)} ký tự — YouTube max 5000.")
    while tags and sum(len(t) + 2 for t in tags) > 460:  # +2 ~ quote/phẩy; API reject nếu quá ~500
        tags.pop()

    # --- giờ công khai ---
    tz = timezone(timedelta(hours=cfg["tz"]))
    if a.slot:
        slot = datetime.strptime(a.slot, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    else:
        slot = next_slot(cfg, datetime.now(timezone.utc))
        if slot is None:
            sys.exit("❌ Không tính được giờ công khai — dùng --slot \"YYYY-MM-DD HH:MM\"")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": api["categoryId"],
            "defaultLanguage": api["lang"],
            "defaultAudioLanguage": api["lang"],
        },
        "status": {
            "privacyStatus": a.privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    if a.privacy == "private" and not a.no_publish:
        body["status"]["publishAt"] = slot.isoformat()

    print(f"── UPLOAD PLAN — {a.slug} → {cfg['name']} ──")
    print(f"  video    : {mp4.name} ({mp4.stat().st_size/1024/1024:.0f} MB)")
    print(f"  title    : {title[:70]}…" if len(title) > 70 else f"  title    : {title}")
    print(f"  tags     : {len(tags)} tag · category {api['categoryId']} · lang {api['lang']}")
    print(f"  srt      : {'có' if srt.exists() and not a.no_captions else 'KHÔNG'}   thumbnail: {'có' if thumb and not a.no_thumb else 'KHÔNG'}")
    if "publishAt" in body["status"]:
        print(f"  công khai: {fmt_slot(slot, cfg)}  (upload xong nằm private chờ tới giờ)")
    else:
        print(f"  privacy  : {a.privacy} (không hẹn giờ)")

    yt = get_service(proj)
    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print(f"  kênh auth: {ch['snippet']['title']} ({ch['id']})")
    expected = cfg.get("channel_id")
    if expected and ch["id"] != expected:
        sys.exit(f"❌ TOKEN SAI KÊNH! Token này của kênh {ch['snippet']['title']} ({ch['id']}), "
                 f"config kênh {a.channel} yêu cầu {expected}.\n"
                 f"→ Xóa {proj / 'credentials' / 'token.json'} rồi chạy lại auth_test.py, chọn đúng tài khoản/kênh.")
    if not expected:
        print(f"  ⚠️ Config kênh {a.channel} chưa có channel_id — thêm \"channel_id\": \"{ch['id']}\" vào CHANNELS (upload_pack.py) để khóa an toàn.")

    # ⛔ CHỐNG UPLOAD TRÙNG — kiểm KÊNH THẬT, không tin UPLOADED.txt (thêm 2026-07-30).
    # Ca gốc: user đã tự đăng video 14 co-dai bằng tay → không có UPLOADED.txt →
    # pipeline_status báo "GÓI SẴN" → upload lần 2, kênh có 2 video giống hệt cách 1 ngày
    # (đúng profile inauthentic content §1, và chia đôi traffic của bản gốc).
    # UPLOADED.txt chỉ biết những lần đăng QUA TOOL — nó không phải nguồn sự thật của kênh.
    dup = find_on_channel(yt, ch, title)
    if dup:
        msg = (f"⛔ TRÊN KÊNH ĐÃ CÓ video cùng tiêu đề — KHÔNG upload (tránh trùng):\n"
               f"   {dup['id']}  [{dup['privacy']}]  đăng {dup['published'][:10]}  "
               f"https://youtu.be/{dup['id']}\n"
               f"   → Muốn ĐỔI THUMBNAIL/metadata của bản đó thì dùng thumbnails.set / videos.update,\n"
               f"     KHÔNG upload lại. Thật sự cần bản thứ hai: thêm --allow-duplicate.")
        if not a.allow_duplicate:
            sys.exit(msg)
        print(msg.replace("⛔", "⚠️ (--allow-duplicate)"))

    if a.dry_run:
        print("✅ DRY-RUN OK — auth + metadata + file đều sẵn sàng. Bỏ --dry-run để upload thật.")
        return

    print("→ Uploading… (resumable, video dài cứ để nó chạy)")
    media = MediaFileUpload(str(mp4), chunksize=16 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp, last, retries = None, -1, 0
    while resp is None:
        try:
            status, resp = req.next_chunk()
            retries = 0
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and retries < 10:
                retries += 1
                print(f"   … lỗi server {e.resp.status}, thử lại {retries}/10")
                time.sleep(min(2 ** retries, 60))
                continue
            raise
        except (OSError, ConnectionError) as e:
            if retries < 10:  # đứt mạng/wifi — upload resumable, nối lại được
                retries += 1
                print(f"   … lỗi mạng ({e.__class__.__name__}), thử lại {retries}/10")
                time.sleep(min(2 ** retries, 60))
                continue
            raise
        if status:
            pct = int(status.progress() * 100)
            if pct // 10 > last // 10:
                print(f"   … {pct}%")
                last = pct
    vid = resp["id"]
    print(f"✅ Video ID: {vid}  →  https://youtu.be/{vid}")

    if thumb and not a.no_thumb:
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb))).execute()
            print("✅ Thumbnail OK")
        except HttpError as e:
            print(f"⚠️ Thumbnail lỗi ({e.resp.status}) — set tay trong Studio. (Kênh cần xác minh SĐT mới được custom thumbnail)")
    if srt.exists() and not a.no_captions:
        try:
            yt.captions().insert(
                part="snippet",
                body={"snippet": {"videoId": vid, "language": api["lang"], "name": api["caption_name"], "isDraft": False}},
                media_body=MediaFileUpload(str(srt), mimetype="application/octet-stream"),
            ).execute()
            print("✅ Phụ đề subs.srt OK")
        except HttpError as e:
            print(f"⚠️ Caption lỗi ({e.resp.status}) — upload tay subs.srt trong Studio.")

    (vdir / "UPLOADED.txt").write_text(
        f"video_id: {vid}\nurl: https://youtu.be/{vid}\nuploaded: {datetime.now():%Y-%m-%d %H:%M}\n"
        f"publishAt: {body['status'].get('publishAt', '(none)')}\nchannel: {cfg['name']}\n",
        encoding="utf-8")
    print(f"— Ghi sổ: UPLOADED.txt")
    # Chuyển kho theo convention: video đã upload → 07_UPLOADED/
    #
    # ⚠️ 2026-07-30: TOÀN BỘ khâu dọn kho bọc try/except và KHÔNG BAO GIỜ được làm
    # process exit != 0 khi VIDEO ĐÃ UPLOAD XONG. Ca gốc: wrapper .cmd redirect log vào
    # chính 06_VIDEO/<slug>/upload.log → shutil.move không xoá nổi file đang mở →
    # traceback + EXITCODE=1 trên một lần upload THÀNH CÔNG. Exit 1 ở đây cực nguy hiểm:
    # người/agent đọc "failed" rồi chạy lại = UPLOAD TRÙNG lên kênh.
    try:
        move_to_kho(proj, vdir, a.slug, a.channel)
    except Exception as e:
        print(f"⚠️ Upload XONG nhưng dọn kho lỗi: {type(e).__name__}: {e}")
        print(f"   → Video an toàn trên kênh. Dọn tay: python tools/upload_pack.py {a.slug} "
              f"--channel {a.channel} --done")
    print(f"— Kiểm tra/sửa trong Studio: https://studio.youtube.com/video/{vid}/edit")
    if "publishAt" in body["status"]:
        print(f"— Video tự CÔNG KHAI lúc {fmt_slot(slot, cfg)}.")


if __name__ == "__main__":
    main()
