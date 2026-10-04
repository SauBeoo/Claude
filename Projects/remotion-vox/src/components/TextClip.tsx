// TextClip.tsx — tag chips / punch boxes / plain text, animation from registry.
// Presets carry the OkuraDemo look; layout fields override preset positions.

import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {TextClipSchema, ThemeSchema} from '../schema/project';
import {resolveTextAnimation} from '../effects/textAnimations';
import {KinText} from './KinText';
import {TeiText} from './TeiText';
import {YawaText} from './YawaText';

type TextClipT = z.infer<typeof TextClipSchema>;
type Theme = z.infer<typeof ThemeSchema>;

/** Mực đọc được trên nền `bg`: nền tối → trắng, nền sáng → đen mềm.
 *  Dùng cho ô giá trị của `papercut-stat` — xem ghi chú tại chỗ gọi. */
const inkOn = (bg?: string): string => {
	const m = /^#([0-9a-fA-F]{6})$/.exec((bg ?? '').trim());
	if (!m) return '#1A1A18';
	const n = parseInt(m[1], 16);
	// luminance tương đối (sRGB xấp xỉ tuyến tính — đủ để chọn trắng/đen)
	const lum =
		(0.2126 * ((n >> 16) & 255) +
			0.7152 * ((n >> 8) & 255) +
			0.0722 * (n & 255)) /
		255;
	return lum < 0.55 ? '#FFFFFF' : '#1A1A18';
};

export const TextClip: React.FC<{clip: TextClipT; theme: Theme}> = ({
  clip,
  theme,
}) => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();

  const anim = resolveTextAnimation(clip.animation)({
    frame,
    fps,
    params: clip.animationParams,
  });

  // yawa-*: preset riêng kênh 人生哲学の夜話 (chữ 明朝 hiện dần), xem YawaText.tsx
  if (clip.preset.startsWith('yawa-')) return <YawaText clip={clip} />;
  // kin-*: preset rieng kenh kinishinai (chip chuong / o chu / 出典 / the so), xem KinText.tsx
  if (clip.preset.startsWith('kin-')) return <KinText clip={clip} />;
  // tei-*: preset rieng kenh teinengo (chu hien theo loi doc, nhan mem), xem TeiText.tsx
  if (clip.preset.startsWith('tei-')) return <TeiText clip={clip} />;

  const font = theme.fontFamily;
  const base: React.CSSProperties = {
    position: 'absolute',
    fontFamily: font,
    fontWeight: 900,
    transform: anim.transform,
    opacity: anim.opacity ?? 1,
  };

  // ── TELOP: 1–2 dòng CỰC TO, chữ trần trên footage, viền đen dày (袋文字) ──
  // Khuôn nenkin từ video 22 (user chốt 2026-09-07 theo video mẫu cùng ngách 年金).
  // Cụm bọc `{}` được đổi màu nhấn: "翌年は\n{対象}かも" -> 対象 xanh, còn lại trắng.
  //
  // 🔴 VIỀN vẽ bằng `paintOrder: 'stroke fill'`, KHÔNG bằng `text-shadow` xếp lớp.
  //    `-webkit-text-stroke` một mình thì viền vẽ ĐÈ VÀO TRONG nét chữ (stroke căn giữa
  //    đường biên) nên chữ Nhật nét mảnh bị ăn mất ~nửa viền => kanji rậm (額・確認) bết
  //    thành cục đen. `paint-order: stroke fill` vẽ viền TRƯỚC rồi phủ fill lên, nên
  //    glyph giữ nguyên hình dù viền dày 14px.
  // 🔴 Cỡ chữ mặc định suy từ CHIỀU CAO KHUNG, không phải hằng số px: bản mẫu đo được
  //    glyph box ~7,8–8,7% chiều cao khung (1280×716) => 0.085*H. Hằng số px sẽ sai
  //    ngay khi đổi khổ render.
  if (clip.preset === 'telop') {
    const size = clip.fontSize ?? Math.round(height * 0.085);
    const lines = clip.content.split('\n');
    const stroke = Math.max(6, Math.round(size * 0.15));
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? Math.round(height * 0.055),
          top: clip.layout.y ?? Math.round(height * 0.05),
          maxWidth: clip.layout.w ?? undefined,
          transformOrigin: 'left top',
          display: 'flex',
          flexDirection: 'column',
          gap: Math.round(size * 0.06),
          lineHeight: 1.12,
          letterSpacing: '0.01em',
        }}
      >
        {lines.map((ln, li) => (
          <div key={li} style={{whiteSpace: 'nowrap'}}>
            {/* cụm trong {} = nhấn màu; phần còn lại trắng */}
            {ln.split(/(\{[^}]*\})/g)
              .filter((t) => t !== '')
              .map((tok, ti) => {
                const hot = tok.startsWith('{') && tok.endsWith('}');
                return (
                  <span
                    key={ti}
                    style={{
                      fontSize: size,
                      fontWeight: 900,
                      color: hot ? clip.color : '#FFFFFF',
                      WebkitTextStrokeWidth: `${stroke}px`,
                      WebkitTextStrokeColor: '#14100C',
                      paintOrder: 'stroke fill',
                      // bóng nhẹ tách chữ khỏi footage sáng (bản mẫu có, rất mảnh)
                      filter: `drop-shadow(0 ${Math.round(
                        size * 0.05
                      )}px ${Math.round(size * 0.05)}px rgba(0,0,0,0.45))`,
                    }}
                  >
                    {hot ? tok.slice(1, -1) : tok}
                  </span>
                );
              })}
          </div>
        ))}
      </div>
    );
  }

  // ── TELOP-GOLD: chữ GRADIENT VÀNG + viền đỏ-nâu + halo ───────────────────
  // Đo từ bản mẫu khung 240s (「月額5,620円へ増額」). Đây là biến thể "hoa lá cành"
  // của `telop` — dùng cho scene ĐẮT nhất (con số, tin vui).
  // 🔴 Gradient chữ phải làm bằng `background-clip: text`, KHÔNG dùng `fill` —
  //    và khi đó `-webkit-text-stroke` sẽ bị gradient phủ lên, nên viền phải vẽ
  //    bằng một lớp chữ THỨ HAI nằm dưới (cùng chữ, chỉ có stroke). Một lớp thì
  //    hoặc mất gradient, hoặc mất viền.
  if (clip.preset === 'telop-gold') {
    const size = clip.fontSize ?? Math.round(height * 0.095);
    const lines = clip.content.split('\n');
    const stroke = Math.max(8, Math.round(size * 0.17));
    // 🔴 `{...}` = cụm NHẤN. Bản đầu quên parse ở preset này ⇒ dấu ngoặc nhọn
    //    HIỆN NGUYÊN trên khung (bắt được ở still demo, scene 「片方は{返金}」).
    //    Cụm nhấn đổi sang gradient ĐỎ-CAM để tách khỏi vàng của phần còn lại.
    const GOLD =
      'linear-gradient(180deg,#FFF6C0 0%,#FFD34E 38%,#F0A81C 62%,#FFE98A 100%)';
    const HOT =
      'linear-gradient(180deg,#FFE2A0 0%,#FF8A2B 34%,#E4321E 70%,#FF9A4A 100%)';
    const Layer: React.FC<{ln: string; top: boolean}> = ({ln, top}) => (
      <div
        style={{
          whiteSpace: 'nowrap',
          fontSize: size,
          fontWeight: 900,
          letterSpacing: '0.01em',
          ...(top
            ? {}
            : {
                // lớp DƯỚI: chỉ viền + halo
                color: 'transparent',
                WebkitTextStrokeWidth: `${stroke}px`,
                WebkitTextStrokeColor: '#8C1410',
                paintOrder: 'stroke fill',
                filter:
                  `drop-shadow(0 0 ${Math.round(size * 0.10)}px rgba(255,196,60,0.55)) ` +
                  `drop-shadow(0 ${Math.round(size * 0.06)}px ${Math.round(size * 0.05)}px rgba(0,0,0,0.5))`,
              }),
        }}
      >
        {ln
          .split(/(\{[^}]*\})/g)
          .filter((t) => t !== '')
          .map((tok, ti) => {
            const hot = tok.startsWith('{') && tok.endsWith('}');
            return (
              <span
                key={ti}
                style={
                  top
                    ? {
                        background: hot ? HOT : GOLD,
                        WebkitBackgroundClip: 'text',
                        backgroundClip: 'text',
                        color: 'transparent',
                      }
                    : undefined
                }
              >
                {hot ? tok.slice(1, -1) : tok}
              </span>
            );
          })}
      </div>
    );
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? Math.round(height * 0.055),
          top: clip.layout.y ?? Math.round(height * 0.045),
          maxWidth: clip.layout.w ?? undefined,
          transformOrigin: 'left top',
          display: 'flex',
          flexDirection: 'column',
          gap: Math.round(size * 0.05),
          lineHeight: 1.1,
        }}
      >
        {lines.map((ln, li) => (
          <div key={li} style={{position: 'relative'}}>
            <Layer ln={ln} top={false} />
            <div style={{position: 'absolute', left: 0, top: 0}}>
              <Layer ln={ln} top />
            </div>
          </div>
        ))}
      </div>
    );
  }

  // ── TELOP-BAND: banner TRẮNG hết bề ngang ở đỉnh + chữ đen ───────────────
  // Đo từ bản mẫu khung 25s. Dùng khi footage bên dưới nhiều chi tiết quá, chữ
  // trần đọc không nổi. Banner cao ~17% khung như mẫu.
  if (clip.preset === 'telop-band') {
    const bandH = Math.round(height * 0.17);
    const size = clip.fontSize ?? Math.round(bandH * 0.55);
    return (
      <div
        style={{
          ...base,
          left: 0,
          top: 0,
          width: '100%',
          height: bandH,
          background: '#FFFFFF',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 14px rgba(0,0,0,0.28)',
        }}
      >
        <div
          style={{
            fontSize: size,
            fontWeight: 900,
            color: '#111111',
            letterSpacing: '0.03em',
            whiteSpace: 'nowrap',
          }}
        >
          {clip.content.split(/(\{[^}]*\})/g)
            .filter((t) => t !== '')
            .map((tok, ti) => {
              const hot = tok.startsWith('{') && tok.endsWith('}');
              return (
                <span key={ti} style={{color: hot ? clip.color : '#111111'}}>
                  {hot ? tok.slice(1, -1) : tok}
                </span>
              );
            })}
        </div>
      </div>
    );
  }

  // ── PAPERCUT-BANNER: MỘT dải giấy xé LIỀN + chữ navy đậm ─────────────────
  // Khuôn user chốt 2026-08-26 (lần 7) theo ảnh mẫu: chữ **liền mạch** in trên một băng
  // giấy kem, mép trên và dưới xé răng cưa. Khác `papercut` (mỗi ký tự một ô rời) — ô rời
  // đọc ra "ransom note", còn cái này đọc ra "băng giấy cắt từ báo rồi dán lên".
  // 🔴 Răng cưa vẽ bằng `clip-path: polygon` với các điểm TIỀN ĐỊNH theo hash — không
  // `random()`, vì Remotion render từng frame độc lập nên random = mép giấy rung mỗi frame.
  if (clip.preset === 'papercut-banner') {
    const size = clip.fontSize ?? 86;
    const seed = clip.id.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
    const N = 26; // số răng mỗi mép — thưa quá thì ra hình thang, dày quá thì ra rìa nhung
    const pts: string[] = [];
    for (let i = 0; i <= N; i++) {
      const h = ((seed + i * 7919) * 2654435761) % 1000;
      pts.push(`${(i / N) * 100}% ${(h % 5) * 0.9}%`); // mép TRÊN
    }
    for (let i = N; i >= 0; i--) {
      const h = ((seed + i * 104729) * 2654435761) % 1000;
      pts.push(`${(i / N) * 100}% ${100 - (h % 5) * 0.9}%`); // mép DƯỚI
    }
    const tilt = ((seed % 5) - 2) * 0.5;
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? 90,
          top: clip.layout.y ?? undefined,
          bottom: clip.layout.y == null ? 150 : undefined,
          maxWidth: clip.layout.w,
          transformOrigin: 'left center',
          // bóng giấy: dùng filter drop-shadow vì clip-path cắt mất box-shadow
          filter: 'drop-shadow(4px 6px 0 rgba(0,0,0,0.26))',
        }}
      >
        <div
          style={{
            transform: `rotate(${tilt}deg)`,
            clipPath: `polygon(${pts.join(', ')})`,
            background: '#F4EFE2',
            padding: `${Math.round(size * 0.30)}px ${Math.round(size * 0.42)}px`,
            whiteSpace: 'nowrap',
          }}
        >
          <span
            style={{
              color: clip.color,
              fontSize: size,
              fontWeight: 900,
              letterSpacing: `${Math.round(size * 0.02)}px`,
              lineHeight: 1,
            }}
          >
            {clip.content}
          </span>
        </div>
      </div>
    );
  }

  // ── PAPERCUT-FORMULA: công thức tính, mỗi HẠNG là một ô giấy ──────────────
  // "1,816億円 ÷ 182日 = 10億円/日" → [ô giấy] ÷ [ô giấy] = [ô NHẤN]
  // Toán tử (÷ × − ＋ = ≒ →) để TRẦN, không có nền — nếu bọc giấy hết thì đọc ra một
  // hàng ô rời rạc, mất cảm giác "một phép tính". Hạng sau `=` là ĐÁP SỐ nên nhấn.
  if (clip.preset === 'papercut-formula') {
    const size = clip.fontSize ?? 64;
    const parts = clip.content.split(/\s+/).filter(Boolean);
    const eq = parts.findIndex((p) => p === '=' || p === '≒');
    // 🔴 XUỐNG DÒNG TẠI `=` LÀ CÓ CHỦ Ý, không phải wrap tuỳ tiện.
    // Đo thật: "1,816億円 ÷ 182日 ≒ 10億円" @font 64 rộng **~1.207px**, còn dải sân khấu
    // (sau khi cast ăn 2×506) chỉ **852px** ⇒ flexWrap tự ngắt ở chỗ ngẫu nhiên và khối
    // 2 dòng đó tụt xuống sát phụ đề (user chỉ đúng lỗi này). Ép ngắt tại `=` cho ra bố
    // cục công thức viết tay — hàng trên là phép tính, hàng dưới là đáp số — và khối cao
    // ổn định nên `y` canh giữa được.
    // ⛔ Không hạ font để nhồi 1 dòng: cần font 44 mới vừa 830px, quá nhỏ cho tệp 45+.
    const rows: string[][] =
      eq >= 0 ? [parts.slice(0, eq + 1), parts.slice(eq + 1)] : [parts];
    const cell = (p: string, i: number) => {
          const isOp = /^[÷×−+＋\-=≒→]$/.test(p);
          const isAns = eq >= 0 && i > eq;
          if (isOp) {
            return (
              <span
                key={i}
                style={{color: '#1C2A4A', fontSize: size * 0.92, opacity: 0.85}}
              >
                {p}
              </span>
            );
          }
          const h = (i * 2654435761) % 1000;
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                transform: `rotate(${((h % 5) - 2) * 0.8}deg)`,
                background: isAns ? clip.color : '#F7F2E6',
                // 🔴 Cùng lỗi với `papercut-stat` (sửa cùng ngày 2026-09-13): ô ĐÁP ÁN tô
                // nền bằng `clip.color`, mà nenkin truyền navy #1C2A4A ⇒ navy-trên-navy,
                // không đọc được. Bắt ở bản render nenkin-23 t=212s (三万二千円).
                // Mực chọn theo độ sáng ô ⇒ chỉ đụng ô đang tối, ô kem giữ nguyên.
                color: isAns ? inkOn(clip.color) : '#1C2A4A',
                fontSize: isAns ? size * 1.16 : size,
                padding: `${Math.round(size * 0.07)}px ${Math.round(size * 0.16)}px`,
                borderRadius: `${2 + (h % 4)}px ${1 + (h % 5)}px ${3 + (h % 3)}px ${
                  2 + (h % 6)
                }px`,
                boxShadow: isAns
                  ? '0 0 0 2px rgba(28,42,74,0.34), 4px 5px 0 rgba(0,0,0,0.28)'
                  : '0 0 0 1.5px rgba(28,42,74,0.30), 3px 4px 0 rgba(0,0,0,0.22)',
              }}
            >
              {p}
            </span>
          );
    };
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? 90,
          top: clip.layout.y ?? 340,
          maxWidth: clip.layout.w ?? 1000,
          transformOrigin: 'left center',
          display: 'flex',
          flexDirection: 'column',
          gap: `${Math.round(size * 0.26)}px`,
        }}
      >
        {rows.map((row, r) => (
          <div
            key={r}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: `${Math.round(size * 0.22)}px`,
              // hàng đáp số thụt vào một nhịp — đọc ra ngay là "kết quả của hàng trên"
              paddingLeft: r > 0 ? size * 0.9 : 0,
            }}
          >
            {row.map((p) => cell(p, parts.indexOf(p)))}
          </div>
        ))}
      </div>
    );
  }

  // ── PAPERCUT-STAT: bảng số liệu, mỗi dòng `nhãn|số` ───────────────────────
  // Nhãn để trần (chỉ là chú thích), SỐ là ô giấy — số mới là thứ mắt phải bắt.
  // Cột số dùng `minWidth` để các dòng thẳng hàng phải; căn phải trong ô.
  // ── FLAT-STAT: bảng phẳng bo tròn cho khuôn ANIME (co-dai 2026-08-27) ─────────
  if (clip.preset === 'flat-stat') {
    const size = clip.fontSize ?? 50;
    const rows = clip.content.split('\n').filter((r) => r.trim());
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? 90,
          top: clip.layout.y ?? 200,
          maxWidth: clip.layout.w ?? 900,
          transformOrigin: 'left top',
          display: 'flex',
          flexDirection: 'column',
          gap: `${Math.round(size * 0.32)}px`,
        }}
      >
        {rows.map((row, i) => {
          const hot = row.trimStart().startsWith('*');
          const body = hot ? row.trimStart().slice(1) : row;
          const [label, val = ''] = body.split('|');
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: size * 0.34}}>
              <span style={{color: '#2B2A28', fontSize: size * 0.82, fontWeight: 800}}>
                {label.trim()}
              </span>
              {val.trim() && (
                <span
                  style={{
                    display: 'inline-block',
                    marginLeft: 'auto',
                    minWidth: size * 4.6,
                    textAlign: 'right',
                    background: hot ? clip.color : '#FFFFFF',
                    color: '#1A1A18',
                    fontSize: size,
                    padding: `${Math.round(size * 0.10)}px ${Math.round(size * 0.24)}px`,
                    borderRadius: `${Math.round(size * 0.28)}px`,
                    border: `${Math.max(2, Math.round(size * 0.05))}px solid #2B2A28`,
                    boxShadow: '4px 5px 0 rgba(43,42,40,0.18)',
                  }}
                >
                  {val.trim()}
                </span>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  if (clip.preset === 'papercut-stat') {
    const size = clip.fontSize ?? 50;
    const rows = clip.content.split('\n').filter((r) => r.trim());
    return (
      <div
        style={{
          ...base,
          left: clip.layout.x ?? 90,
          top: clip.layout.y ?? 200,
          maxWidth: clip.layout.w ?? 900,
          transformOrigin: 'left top',
          display: 'flex',
          flexDirection: 'column',
          gap: `${Math.round(size * 0.30)}px`,
        }}
      >
        {rows.map((row, i) => {
          // 🔴 Dòng được NHẤN phải chỉ định TƯỜNG MINH bằng "*" ở đầu dòng.
          // Quy tắc ngầm cũ ("dòng cuối tự nhấn") đúng cho bảng số liệu — dòng cuối là
          // kết luận — nhưng SAI ở bảng ◯✕: dòng cuối là điều PHỦ ĐỊNH, nhấn vàng làm nó
          // trông như đáp án đúng (đã dính thật ở scene 読み方 của nenkin-17-demo).
          const hot = row.trimStart().startsWith('*');
          let body = hot ? row.trimStart().slice(1) : row;
          // per-row colour (nenkin-18, 2026-08-30): a leading `#rrggbb|` colours THIS row's
          // value cell — one table can carry an axis palette (繰上げ=red / 繰下げ=green)
          // learned once and reused all video (りょう 970K pattern). Rows without a hex
          // prefix behave exactly as before, so older projects are untouched.
          let rowColor: string | null = null;
          const cm = body.match(/^\s*(#[0-9a-fA-F]{6})\|/);
          if (cm) {
            rowColor = cm[1];
            body = body.slice(cm[0].length);
          }
          const [label, val = ''] = body.split('|');
          const h = (i * 2654435761) % 1000;
          return (
            <div
              key={i}
              style={{display: 'flex', alignItems: 'center', gap: size * 0.34}}
            >
              <span
                style={{
                  color: '#1C2A4A',
                  fontSize: size * 0.82,
                  fontWeight: 800,
                  opacity: 0.9,
                }}
              >
                {label.trim()}
              </span>
              {val.trim() && (
                <span
                  style={{
                    display: 'inline-block',
                    marginLeft: 'auto',
                    minWidth: size * 4.6,
                    textAlign: 'right',
                    transform: `rotate(${((h % 5) - 2) * 0.7}deg)`,
                    background: rowColor ?? (hot ? clip.color : '#F7F2E6'),
                    // 🔴 MỰC CHỌN THEO ĐỘ SÁNG CỦA CHÍNH Ô, không theo việc ô ấy được tô
                    // bằng đường nào (sửa 2026-09-13, bắt ở still nenkin-23 f1500).
                    // Bản cũ chỉ đổi sang mực trắng khi có `rowColor`; dòng NHẤN (`*`) lại
                    // tô nền bằng `clip.color`, mà kênh nenkin truyền navy #1C2A4A ⇒ ra
                    // **navy trên navy, không đọc được** — đúng cái §2.1 audience-45plus
                    // gọi là "vừa trống vừa nhạt, tệ nhất với tệp 45+".
                    // Đo độ sáng nên chỉ đụng tới ô đang TỐI (vốn đã hỏng ở mọi project),
                    // ô kem #F7F2E6 giữ nguyên mực đen ⇒ không project nào đổi khác đi.
                    color: inkOn(rowColor ?? (hot ? clip.color : '#F7F2E6')),
                    fontSize: size,
                    padding: `${Math.round(size * 0.07)}px ${Math.round(size * 0.18)}px`,
                    borderRadius: `${2 + (h % 4)}px ${1 + (h % 5)}px ${3 + (h % 3)}px ${
                      2 + (h % 6)
                    }px`,
                    boxShadow:
                      '0 0 0 1.5px rgba(28,42,74,0.30), 3px 4px 0 rgba(0,0,0,0.22)',
                  }}
                >
                  {val.trim()}
                </span>
              )}
            </div>
          );
        })}
      </div>
    );
  }

  // ── PAPERCUT: mỗi KÝ TỰ là một mảnh giấy xé riêng ────────────────────────
  // Vì sao không dùng `textShadow` cho cả dòng: chữ cắt giấy thật thì mỗi mảnh có mép
  // riêng, nghiêng riêng, bóng riêng. Một cái bóng chung cho cả dòng đọc ra ngay là
  // "font phẳng + shadow". Nghiêng/lệch phải TIỀN ĐỊNH theo chỉ số ký tự (hash), không
  // random — nếu không mỗi frame Remotion render ra một góc khác ⇒ chữ rung lập bập.
  if (clip.preset === 'papercut' || clip.preset === 'papercut-punch') {
    const punchy = clip.preset === 'papercut-punch';
    const size = clip.fontSize ?? (punchy ? 62 : 78);
    const chars = Array.from(clip.content);
    const wrap: React.CSSProperties = {
      ...base,
      left: clip.layout.x ?? 90,
      top: clip.layout.y ?? (punchy ? undefined : 70),
      bottom: punchy && clip.layout.y == null ? 110 : undefined,
      maxWidth: clip.layout.w ?? 980,
      transformOrigin: punchy ? 'left bottom' : 'left center',
      display: 'flex',
      flexWrap: 'wrap',
      alignItems: 'flex-end',
      gap: `${Math.round(size * 0.055)}px`,
    };
    return (
      <div style={wrap}>
        {chars.map((ch, i) => {
          if (ch === ' ' || ch === '　') {
            return <span key={i} style={{width: size * 0.42}} />;
          }
          // hash tiền định: cùng ký tự + cùng vị trí ⇒ luôn cùng góc/lệch
          const h = (i * 2654435761) % 1000;
          const tilt = ((h % 7) - 3) * 0.9; // −2.7° … +2.7°
          const dy = ((Math.floor(h / 7) % 5) - 2) * (size * 0.018);
          const padX = Math.round(size * 0.11);
          const padY = Math.round(size * 0.05);
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                transform: `rotate(${tilt}deg) translateY(${dy}px)`,
                background: punchy ? '#1A1A18' : '#F7F2E6',
                color: punchy ? clip.color : '#1C2A4A',
                fontSize: size,
                lineHeight: 1.02,
                padding: `${padY}px ${padX}px`,
                // mép giấy xé: 4 góc bán kính lệch nhau, không phải bo tròn đều
                borderRadius: `${2 + (h % 4)}px ${1 + (h % 5)}px ${3 + (h % 3)}px ${
                  2 + (h % 6)
                }px`,
                // vành mực mảnh + bóng giấy thật (không phải textShadow của cả dòng)
                boxShadow: punchy
                  ? '3px 4px 0 rgba(0,0,0,0.34)'
                  : '0 0 0 1.5px rgba(28,42,74,0.30), 3px 4px 0 rgba(0,0,0,0.22)',
              }}
            >
              {ch}
            </span>
          );
        })}
      </div>
    );
  }

  let style: React.CSSProperties;
  if (clip.preset === 'tag') {
    style = {
      ...base,
      left: clip.layout.x ?? 90,
      top: clip.layout.y ?? 70,
      transformOrigin: 'left center',
      background: clip.color,
      color: '#111',
      padding: '14px 34px',
      fontSize: clip.fontSize ?? 74,
      boxShadow: '6px 8px 0 rgba(0,0,0,0.28)',
    };
  } else if (clip.preset === 'punch') {
    style = {
      ...base,
      left: clip.layout.x ?? 90,
      top: clip.layout.y ?? undefined,
      bottom: clip.layout.y == null ? 110 : undefined,
      maxWidth: clip.layout.w ?? 980,
      transformOrigin: 'left bottom',
      background: '#111',
      color: clip.color,
      padding: '18px 30px',
      fontSize: clip.fontSize ?? 56,
      lineHeight: 1.15,
      boxShadow: '8px 10px 0 rgba(0,0,0,0.25)',
    };
  } else {
    style = {
      ...base,
      left: clip.layout.x ?? 90,
      top: clip.layout.y ?? Math.round(height / 2),
      maxWidth: clip.layout.w,
      color: clip.color,
      fontSize: clip.fontSize ?? 60,
      lineHeight: 1.2,
      textShadow: '3px 4px 0 rgba(0,0,0,0.2)',
    };
  }

  return <div style={style}>{clip.content}</div>;
};
