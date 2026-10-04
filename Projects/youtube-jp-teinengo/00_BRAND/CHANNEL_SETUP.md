# Tầng kênh — 定年後のこころ研究室 (setup 2026-09-30, rebrand từ みんなの健康ノート)

- channelId: `UCnoYb7aEKy1NgspYTKwhh1Q` (giữ nguyên của みんなの健康ノート) · Gmail `saubeooo04@gmail.com` · Chrome `Profile 13`
- Trạng thái trước rebrand: 21 video công khai · 903 view · 3 sub · 1 playlist `薬と食べ物｜60代の食卓` (18) · trailer `BQYoaEH_BAQ`. Sao lưu: `old_health_before_rebrand.json` (chỉ phần công khai; token health không vào được kênh).
- ⚠️ `youtube-jp-health/credentials/token.json` KHÔNG thuộc kênh này (`mine=True` trả rỗng) ⇒ mọi thao tác ghi đi Studio.

## Tên / handle
- Tên: `定年後のこころ研究室`
- Handle mong muốn: `@teinengo-kokoro` (dự phòng `@teinengo-kokoro-lab` · `@teinengonokokoro`)

## Mô tả kênh (dán nguyên văn)
```
「定年後のこころ研究室」へ、ようこそ。

このチャンネルでは、定年後の毎日を、心理学や研究の知見をもとに、わかりやすくひもといていきます。

・定年後の暮らし方、一日の過ごし方
・仕事を離れたあとの、生きがいと居場所の見つけ方
・60代・70代から、人生がもう一度楽しくなる考え方

定年は、終わりではなく、二度目のはじまりです。
このチャンネルが、これからの毎日を前向きに過ごすヒントになれば嬉しいです。

・心理学の知見は、出典を確かめたものを使います
・医療・カウンセリングの代わりになるものではありません
・お金や制度の個別のご相談は、専門の窓口をご利用ください

家事をしながら、ラジオのように聞いていただけたら嬉しいです。

#定年後 #心理学 #60代
```

## Keywords
```
定年後のこころ研究室 定年後 定年 定年退職 定年後の暮らし 定年後の過ごし方 定年後の人生 定年後の生き方 第二の人生 生きがい 居場所 心理学 60代 70代 50代 シニア 老後 人生後半 趣味 学び直し 夫婦 前向き 心が軽くなる 生き方 人生
```

## Cài đặt khác
- 国/地域: 日本 · デフォルト言語: 日本語
- Trailer cũ (video health `BQYoaEH_BAQ`) → gỡ
- 21 video health cũ → **限定公開** (không xoá)
- Playlist `薬と食べ物｜60代の食卓` → **riêng tư** (không xoá)
- Mặc định upload: kiểm tag/mô tả trống · danh mục 27 教育 · tiếng Nhật

## ✅ Đã làm 2026-09-30, toàn bộ qua Studio (Chrome), kiểm lại bằng API readonly
- Tên, handle `@teinengo-kokoro`, ảnh đại diện, banner, mô tả, 25 keywords
- Gỡ trailer health `BQYoaEH_BAQ`
- 21/21 video health → 限定公開 (sửa hàng loạt trong Nội dung)
- Playlist `PLPsDzyXJrig8` → riêng tư, không xoá
- Mặc định upload: **xoá 9 tag rác** cũ của health (シニア健康 · 腎臓に良い食べ物…). Danh mục 22 → **27 教育**, ngôn ngữ tiếng Nhật
- ⚠️ Còn mở: `brandingSettings.channel.defaultLanguage` = **`en`**. Studio không có ô sửa; sửa bằng API khi đã có token đúng kênh.
- ⚠️ Banner hiển thị trên TV: hai khối đồi kéo dài xuống đáy ảnh (chỉ thấy ở khung TV, desktop/mobile sạch). Sửa `tools/make_brand.py` nếu cần.
