# -*- coding: utf-8 -*-
"""XOA ✦ cho lo 289 anh manga cua video 38 (1376x768).

🔴 VI SAO KHONG INPAINT / KHONG TRUNG VI HANG (media-library.md §2.10 ⑤b):
   · trung vi HANG (§3): nen manga la MANG MAU PHANG co NET MUC DEN chay qua
     => trung vi hang keo mau lai, ra vet chu nhat.
   · inpaint (§6b): ✦ hay de len net muc (chan gap, vai nguoi) => inpaint XOA net.
   · morphology (§6c): ✦ o day KHONG phai net manh 2px ma la blob ~43px => opening
     kernel du lon se pha ca vat that.

✅ CACH DUNG O DAY — GO NGUOC PHEP TRON ALPHA, uoc alpha tu CHINH 289 ANH:
   watermark la CUNG MOT hinh, CUNG MOT cho, tren MOI anh  =>  obs = (1-a)·I + a·255
   · uoc nen I cua tung anh bang medianBlur ksize 101 (PHAI lon hon duong kinh sao
     ~43px, neu khong chinh cai sao nang sang nen uoc => a bi danh gia thap, go khong het)
   · a_i = (obs - I) / (255 - I),  bo pixel nen qua sang (mau so ~0)
   · a = TRUNG VI qua 289 anh  => sach noi dung, chi con hinh sao
   · go: I = (obs - a·255) / (1 - a)
   Net muc den van nguyen ven vi phep go la ham cua tung pixel, khong noi suy tu hang xom.
"""
import sys, os, glob, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
import cv2

CX, CY, R = 1280, 666, 46          # tam ✦ chot BANG MAT (zoom 3x, 8 mau), bao du canh sao
PAD = 120                            # vien mo rong de medianBlur co nen that
W, H = 1376, 768


# 🔴 cv2.imread/imwrite TRA None (khong bao loi) khi duong dan co ky tu ngoai ASCII —
#    thu muc nguon ten tieng Viet ("Thang 9 17 - 19_43"). Doc/ghi qua numpy.
def imread(p):
    a = cv2.imdecode(np.fromfile(p, dtype=np.uint8), cv2.IMREAD_COLOR)
    if a is None:
        raise IOError("khong doc duoc: " + p)
    return a


def imwrite(p, a):
    ok, buf = cv2.imencode(os.path.splitext(p)[1], a)
    if not ok:
        raise IOError("khong ma hoa duoc: " + p)
    buf.tofile(p)


def boxes():
    x0, y0 = CX - R - PAD, CY - R - PAD
    x1, y1 = min(W, CX + R + PAD), min(H, CY + R + PAD)
    return x0, y0, x1, y1


def est_alpha(files, sample=289):
    """Uoc alpha map cua ✦ tu CHINH 289 anh.

    🔴 BAN DAU DUNG medianBlur DE UOC NEN -> THAT BAI, con VIEN SAO ro (soi 1:1).
       Ly do dung y §6b cua media-library: kernel median bi CHINH CAI SAO nang sang
       (sao ~43px, ROI chi 212px) => nen uoc CAO hon that => alpha THAP => go khong het.
    ✅ Uoc nen bang cv2.inpaint tren mask hinh sao: inpaint KHONG nhin thay pixel trong
       mask nen khong bi sao keo. Inpaint chi dung de UOC ALPHA — anh cuoi van go bang
       cong thuc tren tung pixel, nen NET MUC khong bi noi suy.
    """
    x0, y0, x1, y1 = boxes()
    h, w = y1 - y0, x1 - x0
    cy, cx = CY - y0, CX - x0
    yy, xx = np.mgrid[0:h, 0:w]
    mask = (((xx - cx) ** 2 + (yy - cy) ** 2) <= (R + 6) ** 2).astype(np.uint8)
    # 🔴 TRUNG VI TI SO (obs-I)/(255-I) qua 289 anh -> VAN CON VIEN SAO o bien:
    #    ti so khong on dinh khi (255-I) nho, va trung vi + lam mut lam nhoe bien sac.
    # ✅ BINH PHUONG TOI THIEU tren cung du lieu: obs-I = a·(255-I)
    #       a = Σ (obs-I)(255-I) / Σ (255-I)²
    #    Moi anh dong gop theo trong so (255-I)², nen anh nen TOI (tin hieu manh) noi
    #    nhieu hon anh nen SANG (tin hieu yeu) — dung chieu, va bien giu duoc do sac.
    num = np.zeros((h, w), np.float64)
    den = np.zeros((h, w), np.float64)
    for f in files[:sample]:
        raw = imread(f)[y0:y1, x0:x1]
        im = raw.astype(np.float32)
        bg = cv2.inpaint(raw, mask, 7, cv2.INPAINT_NS).astype(np.float32)
        d = 255.0 - bg
        num += ((im - bg) * d).mean(axis=2)
        den += (d * d).mean(axis=2)
    A = np.where(den > 1e-6, num / np.maximum(den, 1e-6), 0.0).astype(np.float32)
    A[mask == 0] = 0.0
    A[A < 0.02] = 0.0
    return np.clip(A, 0, 0.95)


def tune(files, A, n=30):
    """Do he so k cho alpha.

    🔴 BAN DAU DO BANG NANG LUONG GRADIENT -> SAI CHIEU, va no chon k=2,30 = MEP LUOI:
       go qua tay thi vung sao bi kep ve 0 (den kit) nen gradient lai THAP => thuoc do
       thuong cho cai no phai phat. `k cham bien luoi` chinh la dau hieu thuoc hong
       (cung ho voi bai hoc "gate bao do hang loat thi nghi chinh gate").
    ✅ Thuoc dung: so voi NEN uoc bang inpaint, va CHI do tren pixel NEN PHANG (noi
       inpaint dang tin). Sai so nho nhat = vet sao hoa vao nen, khong den khong trang.
    """
    x0, y0, x1, y1 = boxes()
    h, w = y1 - y0, x1 - x0
    cy, cx = CY - y0, CX - x0
    yy, xx = np.mgrid[0:h, 0:w]
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    inner = d2 <= (R + 2) ** 2
    ks = [round(0.8 + 0.1 * i, 2) for i in range(23)]        # 0,8 .. 3,0
    tot = {k: 0.0 for k in ks}
    cnt = 0
    for f in files[:n]:
        raw = imread(f)[y0:y1, x0:x1]
        mask = inner.astype(np.uint8)
        ref = cv2.inpaint(raw, mask, 7, cv2.INPAINT_NS).astype(np.float32)
        # chi giu pixel NEN PHANG: inpaint chi dang tin o do
        lap = np.abs(cv2.Laplacian(cv2.cvtColor(ref.astype(np.uint8), cv2.COLOR_BGR2GRAY),
                                   cv2.CV_32F))
        flat = inner & (lap < 6)
        if flat.sum() < 200:
            continue
        cnt += 1
        roi = raw.astype(np.float32)
        for k in ks:
            a = np.clip(A * k, 0, 0.95)[..., None]
            fx = np.clip((roi - a * 255.0) / np.maximum(1.0 - a, 1e-3), 0, 255)
            tot[k] += float(np.abs(fx - ref).mean(axis=2)[flat].mean())
    bk = min(ks, key=lambda k: tot[k])
    print("   tune tren %d anh | k=1.0:%.2f  k=%.1f:%.2f (chon)  k=3.0:%.2f"
          % (cnt, tot[1.0] / max(cnt, 1), bk, tot[bk] / max(cnt, 1), tot[3.0] / max(cnt, 1)))
    if bk in (ks[0], ks[-1]):
        print("   ⚠️ k cham MEP luoi — nghi thuoc do, dung tin ngay")
    return bk, tot[bk]


def strip(f, A, outdir):
    x0, y0, x1, y1 = boxes()
    im = imread(f).astype(np.float32)
    roi = im[y0:y1, x0:x1]
    a = A[..., None]
    fixed = (roi - a * 255.0) / np.maximum(1.0 - a, 1e-3)
    im[y0:y1, x0:x1] = np.clip(fixed, 0, 255)
    out = os.path.join(outdir, os.path.splitext(os.path.basename(f))[0] + ".png")
    imwrite(out, im.astype(np.uint8))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=r"C:\Users\tuana\Downloads\Tháng 9 17 - 19_43")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", type=int, default=0, help="chi xu ly N anh dau (thu nghiem)")
    a = ap.parse_args()
    fs = sorted(glob.glob(os.path.join(a.src, "*.jpeg")), key=lambda p: os.path.getmtime(p))
    print("anh:", len(fs))
    os.makedirs(a.out, exist_ok=True)
    A = est_alpha(fs)
    k, sc = tune(fs, A)
    print('he so alpha toi uu k = %.2f' % k)
    A = np.clip(A * k, 0, 0.95)
    np.save(os.path.join(a.out, "_alpha.npy"), A)
    print("alpha: max %.3f | so pixel >0.05: %d | tam alpha %.3f"
          % (A.max(), int((A > 0.05).sum()), A[A.shape[0] // 2, A.shape[1] // 2]))
    tgt = fs[:a.only] if a.only else fs
    for i, f in enumerate(tgt, 1):
        strip(f, A, a.out)
        if i % 50 == 0:
            print("  ", i, "/", len(tgt))
    print("xong:", len(tgt), "->", a.out)
