# -*- coding: utf-8 -*-
"""
auth.py — cấp lại token YouTube cho kênh 地形と地名の日本史.

VÌ SAO PHẢI CHẠY (chẩn đoán 2026-09-16):
Token kế thừa từ kr-romfan gọi `channels.list(mine=True)` trả **totalResults: 0** — nghĩa là
lúc OAuth lần đầu đã chọn **Google account cá nhân**, KHÔNG chọn **brand channel** 사우 오디오.
Đọc thì được (đọc bằng `id=`), nhưng mọi lệnh GHI đều `403`:
    · channels.update    → 403 PERMISSION_DENIED   (thiếu cả scope `.../auth/youtube`)
    · videos.update      → 403 forbidden (youtube.video)
Token mới xin thêm scope `youtube` và phải được cấp ĐÚNG brand channel.

🔴 HAI CHỖ DỄ BẤM SAI KHI TRÌNH DUYỆT MỞ RA:
  1. Chọn Gmail **ladykiller301096@gmail.com**.
  2. Màn hình kế hỏi "chọn kênh" → **CHỌN KÊNH 사우 오디오 / 地形と地名の日本史**,
     KHÔNG chọn dòng tên người. Bấm nhầm ở đây là lặp lại đúng lỗi cũ.
Xong thì `python tools/auth.py --check` phải in ra đúng tên kênh.

    python tools/auth.py            # mở trình duyệt, cấp token mới
    python tools/auth.py --check    # chỉ kiểm token hiện có
"""
import io, sys, argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
CRED = ROOT / "credentials"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",             # <- MỚI: cần cho channels.update
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def check():
    p = CRED / "token.json"
    if not p.exists():
        print("chua co token.json"); return False
    c = Credentials.from_authorized_user_file(str(p))
    if not c.valid:
        c.refresh(Request())
    yt = build("youtube", "v3", credentials=c)
    r = yt.channels().list(part="snippet,statistics", mine=True).execute()
    n = r.get("pageInfo", {}).get("totalResults", 0)
    print("scopes :", c.scopes)
    print("mine=True -> totalResults =", n)
    if n == 0:
        print("🔴 TOKEN KHONG GAN VOI KENH NAO — moi lenh GHI se 403.")
        print("   Chay lai: python tools/auth.py   va nho CHON DUNG KENH o man hinh thu hai.")
        return False
    for it in r["items"]:
        print("✅ token dai dien cho:", it["snippet"]["title"], it["id"],
              "| sub", it["statistics"].get("subscriberCount"))
    return True


def login():
    CRED.mkdir(parents=True, exist_ok=True)
    cs = CRED / "client_secret.json"
    if not cs.exists():
        sys.exit("thieu credentials/client_secret.json")
    flow = InstalledAppFlow.from_client_secrets_file(str(cs), SCOPES)
    print("Trinh duyet se mo. NHO: chon Gmail ladykiller301096@gmail.com,")
    print("roi o man hinh ke tiep CHON KENH (사우 오디오 / 地形と地名の日本史), khong chon ten nguoi.")
    creds = flow.run_local_server(port=0, prompt="consent")
    (CRED / "token.json").write_text(creds.to_json(), encoding="utf-8")
    print("da ghi", CRED / "token.json")
    check()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    g = ap.parse_args()
    check() if g.check else login()
