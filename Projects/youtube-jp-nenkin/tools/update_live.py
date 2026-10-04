# -*- coding: utf-8 -*-
"""update_live.py — đổi TITLE / 3 dòng đầu 概要欄 / TAG / THUMBNAIL của video ĐÃ LIVE.

Khác `upload_api.py` (chỉ videos.insert cho video mới). Standalone, mọi kênh gọi được.

Nguyên tắc an toàn (đúc từ bài học ghi lên kênh, `.claude/rules/upload-schedule.md` §1.5):
  • DRY-RUN là mặc định — phải `--apply` mới ghi thật.
  • Đọc snippet HIỆN TẠI trước, in diff cũ→mới, và **gửi lại nguyên categoryId /
    defaultLanguage / defaultAudioLanguage** lấy từ bản đọc về. Thiếu = API xoá trắng field.
  • Sao lưu toàn bộ snippet cũ ra <plan>_backup.json TRƯỚC khi ghi → rollback được
    bằng chính file đó (`--rollback <backup.json>`).
  • Chỉ đổi 3 dòng đầu mô tả (phần trước dòng trống đầu tiên), giữ nguyên đoạn dài,
    目次, disclaimer, credit, hashtag.

Plan JSON:
[
  {"videoId":"xxx", "title":"...", "desc_head":"3 dòng...",
   "tags_add":["..."], "thumb":"đường/dẫn.png"}
]

Dùng:
  python tools/update_live.py <plan.json> --project E:\\...\\youtube-jp-nenkin
  python tools/update_live.py <plan.json> --project ... --apply
  python tools/update_live.py <backup.json> --project ... --rollback --apply
"""
import argparse
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-chouhen\tools")

from googleapiclient.http import MediaFileUpload  # noqa: E402
from upload_api import get_service  # noqa: E402

SEP = "\n\n"
TAG_LIMIT = 480          # YouTube: tổng tag ~500 ký tự
TITLE_LIMIT = 100


def swap_head(desc: str, head: str) -> str:
    """Thay khối trước dòng trống ĐẦU TIÊN. Không có dòng trống → thay cả (hiếm)."""
    if SEP in desc:
        return head.rstrip() + SEP + desc.split(SEP, 1)[1]
    return head.rstrip()


def show(label, old, new):
    if old == new:
        print(f"   {label}: (giữ nguyên)")
        return False
    print(f"   {label}:")
    print(f"      CŨ  │ {old}")
    print(f"      MỚI │ {new}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--project", required=True)
    ap.add_argument("--apply", action="store_true", help="ghi thật (mặc định chỉ dry-run)")
    ap.add_argument("--rollback", action="store_true", help="plan là file backup → trả về nguyên trạng")
    ap.add_argument("--no-thumb", action="store_true")
    ap.add_argument("--only-thumb", action="store_true",
                    help="CHỈ đổi thumbnail — không đụng title/mô tả/tag (giữ 1 biến để đọc được kết quả)")
    a = ap.parse_args()

    proj = Path(a.project)
    plan_p = Path(a.plan)
    items = json.loads(plan_p.read_text(encoding="utf-8"))
    yt = get_service(proj)

    ids = [it["videoId"] for it in items]
    cur = {v["id"]: v["snippet"]
           for v in yt.videos().list(part="snippet", id=",".join(ids)).execute()["items"]}
    missing = [i for i in ids if i not in cur]
    if missing:
        sys.exit(f"❌ Không đọc được videoId: {missing} — sai ID hoặc sai kênh/token.")

    backup = []
    payloads = []
    print(f"{'=' * 74}\n{'ROLLBACK' if a.rollback else 'CẬP NHẬT'} {len(items)} video "
          f"— {'GHI THẬT' if a.apply else 'DRY-RUN (chưa ghi gì)'}\n{'=' * 74}")

    for it in items:
        vid = it["videoId"]
        s = cur[vid]
        backup.append({"videoId": vid, "title": s["title"], "description": s["description"],
                       "tags": s.get("tags", []), "categoryId": s.get("categoryId"),
                       "defaultLanguage": s.get("defaultLanguage"),
                       "defaultAudioLanguage": s.get("defaultAudioLanguage")})

        if a.rollback:
            new_title = it["title"]
            new_desc = it["description"]
            new_tags = it.get("tags", [])
        elif a.only_thumb:
            new_title, new_desc, new_tags = s["title"], s["description"], list(s.get("tags", []))
        else:
            new_title = it.get("title", s["title"])
            new_desc = swap_head(s["description"], it["desc_head"]) if it.get("desc_head") else s["description"]
            new_tags = list(s.get("tags", []))
            for t in it.get("tags_add", []):
                if t not in new_tags:
                    new_tags.append(t)

        if len(new_title) > TITLE_LIMIT:
            sys.exit(f"❌ {vid}: title {len(new_title)} ký > {TITLE_LIMIT}.")
        tlen = sum(len(t) + 1 for t in new_tags)
        if tlen > TAG_LIMIT:
            print(f"   ⚠️ {vid}: tag tổng {tlen} ký (trần ~500) — YouTube có thể cắt bớt.")

        print(f"\n── {vid}  https://youtu.be/{vid}")
        show("TITLE", s["title"], new_title)
        oh = s["description"].split(SEP)[0].replace("\n", " ⏎ ")
        nh = new_desc.split(SEP)[0].replace("\n", " ⏎ ")
        show("3 DÒNG ĐẦU", oh[:160] + ("…" if len(oh) > 160 else ""),
             nh[:160] + ("…" if len(nh) > 160 else ""))
        add = [t for t in new_tags if t not in s.get("tags", [])]
        print(f"   TAG: {len(s.get('tags', []))} → {len(new_tags)}" + (f"  (+{add})" if add else "  (giữ nguyên)"))
        th = it.get("thumb")
        if th and not a.no_thumb:
            p = Path(th)
            if not p.exists():
                sys.exit(f"❌ {vid}: không thấy thumbnail {p}")
            mb = p.stat().st_size / 1048576
            if mb > 2:
                sys.exit(f"❌ {vid}: thumbnail {mb:.2f} MB > trần 2 MB của YouTube.")
            print(f"   THUMB: {p.name} ({mb:.2f} MB)")

        payloads.append((vid, {
            "id": vid,
            "snippet": {
                "title": new_title,
                "description": new_desc,
                "tags": new_tags,
                # BẮT BUỘC gửi lại — thiếu là API xoá trắng
                "categoryId": s.get("categoryId"),
                "defaultLanguage": s.get("defaultLanguage"),
                "defaultAudioLanguage": s.get("defaultAudioLanguage"),
            },
        }, it.get("thumb")))

    if not a.rollback:
        bp = plan_p.with_name(plan_p.stem + "_backup.json")
        bp.write_text(json.dumps(backup, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n💾 Backup snippet CŨ → {bp}")
        print(f"   rollback: python tools/update_live.py {bp.name} --project <proj> --rollback --apply")

    if not a.apply:
        print("\n🟡 DRY-RUN — chưa ghi gì lên kênh. Thêm --apply để ghi thật.")
        return

    print("\n▶ ĐANG GHI…")
    for vid, body, thumb in payloads:
        if a.only_thumb:
            print(f"   … {vid} snippet: BỎ QUA (--only-thumb)")
        else:
            yt.videos().update(part="snippet", body=body).execute()
            print(f"   ✅ {vid} snippet")
        if thumb and not a.no_thumb:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb)).execute()
            print(f"   ✅ {vid} thumbnail")
    print("\n✅ XONG. Kiểm lại bằng videos.list, và mở URL xem thumbnail (YouTube cache vài phút).")


if __name__ == "__main__":
    main()
