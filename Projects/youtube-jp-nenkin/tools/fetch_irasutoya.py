# -*- coding: utf-8 -*-
"""fetch_irasutoya.py — tải minh họa いらすとや cho bộ cast モニター kênh nenkin.

いらすとや license: miễn phí thương mại ≤20 tác phẩm/1 video (nguồn: irasutoya.com/p/terms).
→ Mỗi video đếm số ảnh いらすとや dùng, KHÔNG vượt 20. Credit 概要欄: イラスト:いらすとや

Cách chạy:  python tools/fetch_irasutoya.py               # tải theo CAST định nghĩa sẵn
            python tools/fetch_irasutoya.py "検索語" out.png   # tải lẻ 1 ảnh

Ảnh lưu assets/cast/<file>.png + tự nhập kho chung _media_library (rule media-library).
Scraper: search blogspot của irasutoya → post đầu tiên → ảnh gốc (=s800).
"""
import re, sys, urllib.request, urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "assets" / "cast"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# file_name -> DANH SÁCH query thử lần lượt (theo từ vựng tiêu đề いらすとや; lấy bài đầu khớp)
CAST = {
    # 田中さん 67 横浜 — tái tuyển dụng văn phòng, tuần 5 buổi
    "tanaka_work":     ["元気に働くお年寄り", "おじいさんの会社員", "働くおじいさん"],
    "tanaka_happy":    ["おじいさんの表情 笑顔"],
    "tanaka_worried":  ["悩むおじいさん", "おじいさんの表情 悩んだ", "困った顔のおじいさん"],
    # 佐藤さん 66 仙台 — part siêu thị, bà
    "sato_work":       ["レジ打ちをする店員", "スーパーのレジ", "働くおばあさん"],
    "sato_happy":      ["おばあさんの表情 笑顔"],
    "sato_relieved":   ["ほっとした顔のおばあさん", "安心するおばあさん", "ホッとしている人"],
    # 鈴木さん 65 名古屋 — 役員
    "suzuki_exec":     ["社長のイラスト", "会社の会長", "重役"],
    "suzuki_shock":    ["ショックを受けるおじいさん", "おじいさんの表情 ショック", "がっかりしたおじいさん"],
    "suzuki_money":    ["年金手帳を持つおじいさん", "年金を受け取る", "お金を持って喜ぶおじいさん"],
    # 高橋さん 64→65 東京 — 部長
    "takahashi_work":  ["中年の会社員", "上司のイラスト", "働くサラリーマン"],
    "takahashi_think": ["腕を組んで考える人", "考える人のイラスト", "考えるサラリーマン"],
    # 山田さんご夫妻 67&65 大阪
    "yamada_worried":  ["老後の不安", "将来が不安な老夫婦", "心配する夫婦"],
    "yamada_happy":    ["仲の良い老夫婦", "老夫婦のイラスト", "笑顔の夫婦"],
    # 伊藤さん 68 福岡 — chủ quán cà phê (script 04)
    "ito_cafe":        ["喫茶店のマスターのイラスト", "コーヒーを入れる人", "カフェの店員"],
    # 研究員 dẫn chuyện
    "kenkyuin":        ["白衣 研究者 男性"],
    "kenkyuin_point":  ["棒で指す人", "解説する人", "説明をする人"],
    # dùng chung cho 勘違い/quiz
    "batsu_ojiisan":   ["マルバツの札を持つ人", "バツを出す人", "不正解 バツ"],
    "maru_ojiisan":    ["マルを出す人", "正解 マル", "マルバツ"],
}


import time


def get(url, tries=4):
    for k in range(tries):
        try:
            time.sleep(1.6)  # lịch sự với irasutoya, tránh 503
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except urllib.error.HTTPError as e:
            if e.code in (503, 429) and k < tries - 1:
                time.sleep(6.0 * (k + 1))
                continue
            raise


def extract_entry_image(post_html):
    """URL ảnh minh họa trong VÙNG ENTRY của post (né icon share/nút Tweet)."""
    ent = post_html
    if 'class="entry"' in ent:
        ent = ent.split('class="entry"', 1)[1]
    for stop in ('class="post-footer"', 'class="sns-buttons"'):
        if stop in ent:
            ent = ent.split(stop, 1)[0]
    m = re.search(r'(https://blogger\.googleusercontent\.com/img/[^"\']+?=s\d+)', ent)
    if m:
        return re.sub(r"=s\d+$", "=s800", m.group(1))
    m = re.search(r'(https://blogger\.googleusercontent\.com/img/[^"\']+)', ent)
    if m:
        return m.group(1) + "=s800"
    m = re.search(r'(https://\d\.bp\.blogspot\.com/[^"\']+?/s\d+(?:-c)?/[^"\']+?\.(?:png|jpg))', ent)
    if m:
        return re.sub(r"/s\d+(-c)?/", "/s800/", m.group(1))
    return None


def search_first_image(query):
    """Search irasutoya → post có TIÊU ĐỀ khớp từ khóa nhất → URL ảnh gốc + link post."""
    q = urllib.parse.quote(query)
    html = get(f"https://www.irasutoya.com/search?q={q}").decode("utf-8", "replace")
    pairs = re.findall(
        r"href='(https://www\.irasutoya\.com/\d{4}/\d{2}/[^']+\.html)'[^>]*>([^<]+)<", html)
    pairs += re.findall(
        r'href="(https://www\.irasutoya\.com/\d{4}/\d{2}/[^"]+\.html)"[^>]*>([^<]+)<', html)
    best = {}
    for url, title in pairs:
        title = title.strip()
        if not title:
            continue
        if url not in best or len(title) > len(best[url]):
            best[url] = title
    if not best:
        return None, None
    import html as _html
    toks = [t for t in re.split(r"\s+", query) if t]
    def score(item):
        url, title = item
        title = _html.unescape(title)
        s = 0
        for t in toks:
            if t in title:
                s += 2
            elif len(t) >= 4 and t[:-1] in title:  # khớp mềm đuôi động từ (抱える/抱えて)
                s += 1
        return s
    ranked = sorted(best.items(), key=lambda it: -score(it))
    post, title = ranked[0]
    if score((post, title)) == 0:
        return None, post  # không post nào khớp từ khóa — báo fail cho đổi query
    img = extract_entry_image(get(post).decode("utf-8", "replace"))
    return img, post


def ingest_media_lib(path, query, url):
    try:
        sys.path.insert(0, r"E:\Claude\Projects\_media_library")
        import media_lib
        media_lib.add_file(path, kind="photo", source="irasutoya",
                           source_id=Path(path).stem, url=url or "",
                           query=query, tags=["irasutoya", "illustration", "nenkin-cast"],
                           license="いらすとや規約 (miễn phí thương mại ≤20点/作品)")
    except Exception as e:
        print(f"  ⚠️ nhập kho lỗi (bỏ qua): {e}")


def fetch(name, queries):
    if isinstance(queries, str):
        queries = [queries]
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{name}.png"
    if dest.exists():
        print(f"SKIP {name} (đã có)")
        return True
    for query in queries:
        try:
            img, post = search_first_image(query)
        except Exception as e:
            print(f"  lỗi 「{query}」: {e}")
            continue
        if img:
            dest.write_bytes(get(img))
            ingest_media_lib(dest, query, post)
            print(f"OK   {name:18s} ← 「{query}」")
            return True
    print(f"FAIL {name} — thử {len(queries)} query đều trượt")
    return False


if __name__ == "__main__":
    if len(sys.argv) == 3:
        ok = fetch(Path(sys.argv[2]).stem, sys.argv[1])
        sys.exit(0 if ok else 1)
    fails = [n for n, q in CAST.items() if not fetch(n, q)]
    print(f"\nXong: {len(CAST) - len(fails)}/{len(CAST)}" + (f" | FAIL: {fails}" if fails else ""))
