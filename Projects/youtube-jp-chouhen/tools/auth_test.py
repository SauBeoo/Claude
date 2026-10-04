# -*- coding: utf-8 -*-
"""
auth_test.py — chạy thử OAuth cho kênh, dùng để:
  1. Chụp màn hình consent (bằng chứng audit: "màn hình xin phép, phạm vi")
  2. Tạo token lần đầu cho uploader (lưu credentials/token.json)

Dùng:  python tools/auth_test.py [--channel-dir E:\\Claude\\Projects\\<project>]
Browser sẽ mở → chọn ĐÚNG tài khoản/kênh → (app chưa verify: bấm Advanced →
Go to ... (unsafe) → Continue) → Allow. Console in tên kênh đã cấp quyền.
"""
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",   # captions.insert
    "https://www.googleapis.com/auth/yt-analytics.readonly",  # retention/traffic per video
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel-dir", default=r"E:\Claude\Projects\youtube-jp-chouhen",
                    help="folder project của kênh (chứa credentials/client_secret.json)")
    a = ap.parse_args()

    cred_dir = Path(a.channel_dir) / "credentials"
    secret = cred_dir / "client_secret.json"
    token = cred_dir / "token.json"
    if not secret.exists():
        sys.exit(f"❌ Không thấy {secret} — tải OAuth client JSON về đúng chỗ trước (API_SETUP_GUIDE.md Bước 4)")

    creds = None
    if token.exists():
        creds = Credentials.from_authorized_user_file(str(token), SCOPES)
        print(f"ℹ️ Đã có token sẵn: {token}")
    if not creds or not creds.valid:
        print("→ Mở browser để cấp quyền… chọn ĐÚNG tài khoản/kênh của project này!")
        flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent")
        token.write_text(creds.to_json(), encoding="utf-8")
        print(f"✅ Token đã lưu: {token}")

    yt = build("youtube", "v3", credentials=creds)
    resp = yt.channels().list(part="snippet,statistics", mine=True).execute()
    items = resp.get("items", [])
    if not items:
        sys.exit("❌ Token hợp lệ nhưng không thấy kênh nào — lúc Allow có thể chọn nhầm tài khoản (không phải brand account của kênh). Xóa credentials/token.json rồi chạy lại, chọn đúng kênh.")
    ch = items[0]["snippet"]
    st = items[0]["statistics"]
    print("=" * 50)
    print(f"✅ ĐÃ CẤP QUYỀN CHO KÊNH: {ch['title']}")
    print(f"   channel id : {items[0]['id']}")
    print(f"   subscriber : {st.get('subscriberCount', '?')} · videos: {st.get('videoCount', '?')}")
    print("=" * 50)
    print("→ Chụp màn hình console này + màn hình consent lúc nãy làm bằng chứng audit.")


if __name__ == "__main__":
    main()
