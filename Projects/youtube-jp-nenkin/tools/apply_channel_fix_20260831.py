# -*- coding: utf-8 -*-
"""Thi hành action item ⑦ của CHANNEL_DIAGNOSIS_2026-08-29.md (kế hoạch user duyệt 2026-08-31):
  Đổi trailer kênh (unsubscribedTrailer) v12 zr9uJbDFaoU (AVP 16,0%) -> v13 pn9Fi9Bx6_U (AVP 27,5%, AVD 4:40).
Chạy: python tools/apply_channel_fix_20260831.py          (dry-run, chỉ in)
      python tools/apply_channel_fix_20260831.py --apply  (ghi thật)
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

APPLY = "--apply" in sys.argv
ROOT = Path(__file__).resolve().parents[1]
creds = Credentials.from_authorized_user_file(str(ROOT / "credentials" / "token.json"))
yt = build("youtube", "v3", credentials=creds)

NEW_TRAILER = "pn9Fi9Bx6_U"  # v13 遺族年金 — AVP cao nhất nhóm có mẫu

ch = yt.channels().list(part="brandingSettings", mine=True).execute()["items"][0]
bs = ch["brandingSettings"]
cur = bs.get("channel", {}).get("unsubscribedTrailer", "")
print(f"trailer hiện tại: {cur}")
if cur == NEW_TRAILER:
    print("đã đúng v13, bỏ qua")
else:
    bs["channel"]["unsubscribedTrailer"] = NEW_TRAILER
    print(f"{'APPLY' if APPLY else 'DRY  '} unsubscribedTrailer {cur} -> {NEW_TRAILER}")
    if APPLY:
        yt.channels().update(part="brandingSettings",
                             body={"id": ch["id"], "brandingSettings": bs}).execute()
        print("DONE (APPLY)")
    else:
        print("dry-run — thêm --apply để ghi")
