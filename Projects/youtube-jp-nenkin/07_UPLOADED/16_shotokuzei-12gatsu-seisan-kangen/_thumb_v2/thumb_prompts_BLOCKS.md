# Thumbnail v2 — video 16 (12月の所得税精算) · 3 ban A/B

> Viet 2026-08-27 sau khi video 16 dat **5 view / 2 ngay** (video 13/14/15 lien truoc: 49 / 68 / 158).
> Quy trinh: `.claude/rules/ab-3title-3thumb.md` §3.1 (4 buoc). Ban cu: `../_upload/thumbnail.png`.

## 1. CHAN DOAN BAN CU — 4 loi do duoc

| # | Loi | So do / bang chung |
|---|---|---|
| 1 | **Nen TOI** — vi pham gate 6 `audience-45plus.md` §1 (nen sang, chu the tuong phan cao) | sang trung binh toan khung **133/255**, thap nhat trong 5 ban gan nhat (15=153 · 12=161 · 13=165 · 14=139). Goc tren-trai (nen thuc) **131** vs **174** cua ban 15 |
| 2 | **Mat CUOI TUOI, nho, xa** — khong co stake | ban 15 (158 view) va 12 (1.457 view) deu la mat **LO/NHIU MAY**; ban 15 con la **can mat**, chiem **45%W** va cao tron khung |
| 3 | **Hero `+数千円!?` — dau CONG + so MO HO** | ca 4 video an view cua kenh deu la **so CU THE**: `5万2千円` (12) · `-1万6千円` (15) · `13万9千` (13) · `5万4600円` (14). `数千円` khong phai mot con so |
| 4 | **4 khoi chu chong nhau** (bubble do + box navy + hero + dai do) | o 168px thanh tuong chu, khong co diem nhan don le. Ban NO NHAT (12) chi co **3 khoi**. Gate 3 cua §1 doi tong <=3 dong |
| + | **Khong co badge kenh** | ban 12 co `年金研究室` goc duoi-trai |

**Ban v2 sua dung 4 cai do:** nen kem gan trang · mat NGAC NHIEN + LO, can mat · hero la so **+2,400円!?** (verified, FACT #3) · **3 khoi chu** + badge kenh.

⚠️ **Cai KHONG the do duoc, phai noi thang:** Analytics API da bi Google rut `impressions`/`CTR`
(`project_api_impressions_bi_rut`), va API tra 400 cho video 16 (chua du tuoi). ⇒ **Khong biet day la
"chua duoc phat" hay "phat ma khong ai bam".** Bang nguong cua kenh (`08_ANALYTICS_LOG.md`) con
**CAM swap thumbnail khi impressions <500**. Doi thumbnail lan nay la **tra no packaging** (4 loi tren
deu la rot gate cua chinh kenh), **khong phai** phep do CTR — CTR sau do KHONG duoc dung lam bang chung.

## 2. SO DO LAY TU BAN THAM CHIEU (ban 15, 158 view — do bang may)

| Khoi | So do ban 15 | Ap vao prompt v2 |
|---|---|---|
| Box navy (chu de) | y 346-572 = **14,8%H** · rong **61,4%W** | banner navy `about one sixth of the frame height`, `left two thirds` |
| Hero vang | y 676-991 = **20,6%H** · rong **61,6%W** | `TALLEST AND WIDEST`, `about two thirds of the frame width` |
| Nguoi (nua phai) | x 1501-2729 = **45,0%W** · cao **tron khung** | `RIGHT 45 PERCENT`, `head almost touching the top edge, cropped by the bottom edge at the waist` |

⭐ Hero cao chi ~21% ma van doc duoc o 120px — xac nhan lai co che da ghi o §3.1 Buoc 2:
**be ngang mua legibility, khong phai chieu cao**. Vi vay prompt ep BE NGANG, khong ep %H.
⚠️ Do hero bang mask mau o khuon nay **khong dang tin** (nen kem/nau cung nga vang -> mask bat ca nen,
tra ve 51-100%). Chi 2 so do dung duoc la **sang trung binh** va **hinh hoc khoi cua ban 15**.

## 3. CHU — GIONG HET o ca 3 ban (bien thu la HINH, §3 muc 6)

| Khoi | Chu | Vai |
|---|---|---|
| banner navy tren | `12月の年金振込だけ` | (1) VE CAI GI + moc thoi gian |
| **hero vang** | `＋2,400円!?` | (2) CHUYEN GI XAY RA — so verified, `!?` de hedge (FACT #4: `還付すべき金額が生じる場合には`) |
| dai do day | `答えは通知書の所得税欄` | (3) PHAI LAM GI / xem o dau — mo loop |
| badge goc duoi-trai | `年金研究室` | nhan dien kenh (nhu ban 12) |

Gate 7 `audience-45plus.md` §1: che anh di van tra loi du **3 cau** ✅ (ve 年金振込 + 所得税 · +2,400円 · xem 通知書の所得税欄).
So `2,400円` la **FACT #3** cua script (vi du chinh thuc cua 日本年金機構: 6,000円 -> 4,600円, qua nap 7,000円, hoan chenh lech 2,400円) -> khong bia, khong misleading.
🔴 **Chua co bang do Trends moi** — phien viet script 08-21 bi `429`, va lan nay cung chua do. `年金振込`/`所得税` la 2 keyword da nam trong title A1 dang live. **Viec con mo:** do lai roi doi chieu top-2 truoc khi coi bo chu nay la chot.
⚖️ **Lech co chu y so `audience-45plus.md` §1.2:** bo **chip 対象** cua khuon nenkin de giu **3 khoi** (loi #4). Chip la thu §1.2 them cho nenkin; 3 khoi la gate 3 cua §1. Chon gate 3 vi day la loi do duoc o ban dang fail.

## 4. BA BAN = BA GIA THUYET (doi dung 1 bien moi ban)

| | Bien doi | Gia thuyet thu |
|---|---|---|
| **T1** `thumb_T1_odoroki-tsucho.png` | baseline khuon kenh: cu ong can mat + **so ngan hang**, nen kem gan trang | sua xong 4 loi thi co len view khong |
| **T2** `thumb_T2_odoroki-kami.png` | doi **1 bien HINH**: so -> **to giay khoanh do** (chu, layout, bieu cam GIU NGUYEN) | lop `紙が届く` vs `通帳` — chinh ranh gioi song-chet do duoc o `CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` |
| **T3** `thumb_T3_kami-shutai.png` | doi **LAYOUT**: bo nguoi han, **to giay lam chu the** giua khung, hero rong 3/4 khung | khuon I `紙が主体` — ban **1,0M view** cua doi thu khong co mat nguoi (`audience-45plus.md` §1.2 mien gate mat cho nenkin) |

## 5. KHUNG KHOI (ban nguoi doc — `FLOW.txt` la ban cung noi dung nen ve 1 dong)

```
<header: 16:9 + tep 55-75 + bright/high-contrast + "bold Japanese text burned into the image">

TEXT, exactly these 3 blocks and nothing else:
navy banner upper left, white bold: 12月の年金振込だけ
hero line, golden yellow with thick black outline and white halo: ＋2,400円!?
bottom red band, white bold: 答えは通知書の所得税欄

LAYOUT:       banner 1/6 H · hero TALLEST AND WIDEST, 2/3 be ngang · dai do 1/6 H · badge goc duoi-trai
BACKGROUND:   tuong kem sang gan trang, evenly lit, flat, no shadows, no dark masses
RIGHT 45%:    cu ong 68, SURPRISED AND UNEASY, eyebrows raised high, cut out white outline,
              head almost touching the top edge, cropped by the bottom edge at the waist
BOTTOM-LEFT:  dao cu + "no characters written anywhere"

<dong chat luong> + bottom-right free of text + No watermark --ar 16:9
```

Bon cau bat buoc co du: `exactly these 3 blocks and nothing else` · `no characters written anywhere` · `Keep the very bottom-right corner free of text` · `No watermark`.
Ep co bang **quan he voi MEP KHUNG** (`head almost touching the top edge` / `cropped by the bottom edge at the waist`), khong ta phan tram — `media-library.md` §2.10 ⑥: model nghe VI TRI, khong nghe TI LE.

## 6. GATE §3.1 — do bang may

| | ky tu | TEXT @ | ket |
|---|---|---|---|
| T1 | 1.468 | 10% | ✅ |
| T2 | 1.483 | 10% | ✅ |
| T3 | 1.373 | 10% | ✅ |

Gate chinh (TEXT trong 15% dau) va gate phu (~1.500 ky) deu sach.

## 7. VIEC SAU KHI USER GEN ANH

1. **Xoa watermark ✦** — `media-library.md` §2.10 ⑤b. Lo 2752x1536 cua chinh video nay do duoc **DUNG MOT dau** o `(0,958W · 0,926H)`; tool cu dung lai duoc: `tools/ingest_thumb_16.py` (cat phai 0,925W + trim day ve 16:9). ⚠️ **Van soi 1:1 ca 4 goc** truoc khi tin hang so — lo moi co the khac.
2. **Soi tung ky tu kanji** — `所得税欄` va `年金振込` la kanji ram, de nat net. Sai mot net = loai, gen lai.
3. Duyet **168px + 120px**, doc duoc hero + bieu cam.
4. Chot ban nao roi moi `thumbnails.set` — **cu ghi len kenh, phai user gat** (`feedback_chot_truoc_khi_dang`).
5. Co du 3 ban thi bat Studio **Test & compare**, va **GIU NGUYEN title** trong luc test (`ab-3title-3thumb.md` §1).
