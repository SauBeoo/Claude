# -*- coding: utf-8 -*-
"""make_thumb_khuonA.py — thumbnail nenkin theo KHUÔN A (3-tầng stack) bóc từ đối thủ thắng
(年金・給付金完全攻略 / 速報): banner thời điểm trên + điều kiện + SỐ hero đỏ + nhân vật いらすとや phải
+ banner dọc trái. Giữ trần YMYL (số thật, không 絶対/必ず). Test: python tools/make_thumb_khuonA.py
"""
import sys, io, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FONT = "C:/Windows/Fonts/YuGothB.ttc"
WHITE=(255,255,255); BLACK=(10,10,10); RED=(226,26,26); YEL=(255,214,0)
def font(s): return ImageFont.truetype(FONT, s)

def grad_bg(c_top,c_bot):
    seed=Image.new("RGB",(1,8))
    for i in range(8):
        t=i/7
        seed.putpixel((0,i),tuple(int(c_top[k]+(c_bot[k]-c_top[k])*t) for k in range(3)))
    return seed.resize((W,H),Image.BICUBIC)

def cover(src,focus="right"):
    im=Image.open(src).convert("RGB")
    s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x0={"left":0,"right":im.width-W,"center":(im.width-W)//2}[focus]
    return im.crop((x0,(im.height-H)//2,x0+W,(im.height-H)//2+H))

def left_scrim(img,wfrac=0.66,strength=205):
    gw=int(W*wfrac); seed=Image.new("L",(5,1),0)
    vals=[strength,int(strength*0.85),int(strength*0.5),int(strength*0.16),0]
    for i,v in enumerate(vals): seed.putpixel((i,0),v)
    img.paste(Image.new("RGB",(gw,H),(0,0,0)),(0,0),seed.resize((gw,H),Image.BICUBIC))
    return img

def outline(d,xy,text,f,fill,stroke,sfill=BLACK):
    d.text(xy,text,font=f,fill=fill,stroke_width=stroke,stroke_fill=sfill)

def fit(d,text,size,maxw,floor=90):
    while size>floor:
        f=font(size); st=max(12,size//9)
        bb=d.textbbox((0,0),text,font=f,stroke_width=st)
        if bb[2]-bb[0]<=maxw: return f,st,bb
        size-=6
    f=font(size); st=max(12,size//9)
    return f,st,d.textbbox((0,0),text,font=f,stroke_width=st)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--bg", default="")
    ap.add_argument("--char", default="assets/irasutoya/takahashi_businessman.png")
    ap.add_argument("--banner1", default="2026年4月")
    ap.add_argument("--banner2", default="制度激変")
    ap.add_argument("--l1", default="働きながら年金")
    ap.add_argument("--l2", default="65万円の壁")
    ap.add_argument("--tag", default="どこまでセーフ？")
    ap.add_argument("--vban", default="60代は要確認")
    ap.add_argument("--cx", type=float, default=0.62, help="right edge of text area (frac of W)")
    args=ap.parse_args()
    out=args.out; bg=args.bg or None; char_path=args.char
    BANNER=(args.banner1,args.banner2); LINE1=args.l1; LINE2=args.l2; TAG=args.tag; VBAN=args.vban

    if bg:  # ảnh AI full-bleed (nhân vật đã nằm trong ảnh, bên phải) + scrim tối trái cho chữ
        img = cover(bg, focus="right")
        img = left_scrim(img, wfrac=max(0.5,args.cx+0.04))
        cx = int(W*args.cx)       # biên phải vùng chữ (chừa chủ thể ảnh bên phải)
    else:   # nền gradient + nhân vật いらすとや (bản test cũ)
        img = grad_bg((232,235,240),(196,201,209))
        ch = Image.open(char_path).convert("RGBA")
        chh=720; s=chh/ch.height
        ch=ch.resize((int(ch.width*s),chh),Image.LANCZOS)
        cx = W-ch.width-40
        img.paste(ch,(cx,H-chh+6),ch)
    d = ImageDraw.Draw(img)

    # banner trên (đen full width)
    BH=168
    d.rectangle((0,0,W,BH),fill=BLACK)
    f1,st1,bb1=fit(d,BANNER[0]+"　"+BANNER[1],118,W-90,floor=90)
    tx=54; ty=(BH-(bb1[3]-bb1[1]))//2-bb1[1]
    w0=d.textbbox((0,0),BANNER[0]+"　",font=f1,stroke_width=st1)[2]
    outline(d,(tx,ty),BANNER[0]+"　",f1,YEL,st1,BLACK)
    outline(d,(tx+w0,ty),BANNER[1],f1,RED,st1,WHITE)

    # banner dọc trái (đỏ)
    VW=96
    d.rectangle((0,BH,VW,H),fill=RED)
    fv=font(64); vy=BH+40
    for chr_ in VBAN:
        vb=d.textbbox((0,0),chr_,font=fv)
        outline(d,(VW//2-(vb[2]-vb[0])//2-vb[0],vy),chr_,fv,WHITE,6,BLACK); vy+=78

    # body: line1 (điều kiện) + line2 (số hero) — vùng giữa banner dọc và nhân vật
    left=VW+40; maxw=cx-left-20
    fL1,sL1,bL1=fit(d,LINE1,150,maxw,floor=90)
    fL2,sL2,bL2=fit(d,LINE2,250,maxw,floor=110)
    fTag=font(78)
    h1=bL1[3]-bL1[1]; h2=bL2[3]-bL2[1]; ht=90
    block=h1+40+h2+30+ht
    y=BH+((H-BH-block)//2)
    outline(d,(left,y-bL1[1]),LINE1,fL1,WHITE,sL1,BLACK)
    y2=y+h1+40
    outline(d,(left,y2-bL2[1]),LINE2,fL2,RED,sL2,WHITE)
    # tag vàng bo góc
    tb=d.textbbox((0,0),TAG,font=fTag,stroke_width=6)
    ty2=y2+h2+34; tw=tb[2]-tb[0]
    d.rounded_rectangle((left-16,ty2-12,left+tw+28,ty2+(tb[3]-tb[1])+24),radius=16,fill=YEL,outline=BLACK,width=5)
    d.text((left,ty2-tb[1]),TAG,font=fTag,fill=BLACK)

    from pathlib import Path
    o=Path(out); o.parent.mkdir(parents=True,exist_ok=True)
    img.save(o)
    img.resize((480,270),Image.LANCZOS).save(o.parent/(o.stem+"_preview480.png"))
    img.resize((120,68),Image.LANCZOS).save(o.parent/(o.stem+"_preview120.png"))
    print("OK",o,"+ preview480/120")

if __name__=="__main__":
    main()
