// project.ts — the central contract of remotion-vox.
// A video = one project.json validated by ProjectSchema. The generic
// composition (VoxProject), the editor and every importer speak this shape.
// NEVER write state back into JSX — JSON is the single source of truth.

import {z} from 'zod';

// ---------------------------------------------------------------------------
// primitives
// ---------------------------------------------------------------------------

export const LayoutSchema = z.object({
  x: z.number().default(0),
  y: z.number().default(0),
  w: z.number().default(400),
  rotation: z.number().default(0),
  opacity: z.number().min(0).max(1).default(1),
});
export type Layout = z.infer<typeof LayoutSchema>;

// Layout OVERRIDE: every field truly optional (no auto-filled defaults).
// Used where presets/fullscreen supply the real defaults (text, footage).
export const LayoutOverrideSchema = z.object({
  x: z.number().optional(),
  y: z.number().optional(),
  w: z.number().optional(),
  h: z.number().optional(), // footage bands/boxes (split-screen)
  rotation: z.number().optional(),
  opacity: z.number().min(0).max(1).optional(),
});

export const EntranceSchema = z.object({
  // key into src/effects/entrances.ts registry; unknown keys fall back to 'rise'
  variant: z.string().default('rise'),
  delayFrames: z.number().int().min(0).default(0),
  params: z.record(z.string(), z.unknown()).default({}),
});
export type Entrance = z.infer<typeof EntranceSchema>;

export const IdleSchema = z.object({
  // continuous low-amplitude bob so cutouts never freeze (paper-collage rule)
  amp: z.number().default(5),
  phase: z.number().default(0),
});

const ClipBase = z.object({
  id: z.string(),
  from: z.number().int().min(0),
  durationInFrames: z.number().int().min(1),
});

// ---------------------------------------------------------------------------
// clip kinds (discriminated union)
// ---------------------------------------------------------------------------

export const BackgroundClipSchema = ClipBase.extend({
  kind: z.literal('background'),
  paper: z.string().nullable().default(null), // asset ref, e.g. "assets/paper.jpg"
  tint: z.string().default('#F2EDE4'),
  tintOpacity: z.number().min(0).max(1).default(0.55),
  grid: z.boolean().default(true),
  dots: z.boolean().default(true),
  splash: z.tuple([z.string(), z.string()]).nullable().default(null),
});

export const StickerClipSchema = ClipBase.extend({
  kind: z.literal('sticker'),
  asset: z.string(), // cutout PNG, relative ref
  layout: LayoutSchema,
  entrance: EntranceSchema.prefault({}),
  exit: EntranceSchema.nullable().default(null),
  idle: IdleSchema.prefault({}),
  shadow: z.enum(['lg', 'sm', 'none']).default('lg'),
});

export const TextClipSchema = ClipBase.extend({
  kind: z.literal('text'),
  content: z.string(),
  // papercut / papercut-punch: ADDED 2026-08-26 for the nenkin paper-collage look —
  // every glyph is its own torn cream paper tile (ink edge + real drop shadow + slight
  // per-glyph tilt), instead of flat type on a solid chip. Added as NEW values so the
  // three original presets (and the 15 projects using them) are untouched.
  // papercut-formula: "1,816億円 ÷ 182日 = 10億円" -> mỗi hạng là một ô giấy, toán tử để
  //   trần, hạng sau `=` được nhấn (nền vàng, to hơn). Số/công thức do FONT vẽ nên luôn
  //   sắc — không bao giờ nhờ ảnh AI vẽ số (kanji/số AI gen là nát nét).
  // papercut-stat: bảng số liệu, mỗi dòng `nhãn|số`, phân cách dòng bằng "\n".
  preset: z
    .enum([
      'tag',
      'punch',
      'plain',
      'papercut',
      'papercut-punch',
      'papercut-formula',
      'papercut-stat',
      // papercut-banner: MỘT DẢI giấy xé LIỀN (mép trên+dưới răng cưa) + chữ navy đậm in
      //   trên đó. Khác `papercut` (mỗi ký tự một ô rời) — đây là khuôn user chốt
      //   2026-08-26 lần 7 theo ảnh mẫu: chữ liền mạch trên một băng giấy.
      'papercut-banner',
      // flat-stat: bảng `nhãn|số` như papercut-stat nhưng ô PHẲNG bo tròn, không nghiêng,
      //   không mép giấy — cho kênh dùng ảnh ANIME (co-dai từ 2026-08-27). Thêm mới, không
      //   sửa papercut-stat để nenkin không đổi.
      'flat-stat',
      // telop: khuôn TELOP TOÀN KHUNG cho nenkin từ video 22 (user chốt 2026-09-07 theo
      //   video mẫu cùng ngách). 1–2 dòng CỰC TO đè lên footage full-bleed, chữ trắng
      //   viền đen dày (袋文字), và **một cụm bọc trong `{}` được đổi màu nhấn**
      //   (`{対象}` -> xanh). Xuống dòng bằng ký tự newline trong `content`.
      //   Khác `punch`/`tag` ở chỗ nó không
      //   có nền chip — nó là chữ trần trên ảnh, nên viền phải dày mới đọc được.
      'telop',
      // telop-gold: bien the "hoa la canh" cua telop — chu GRADIENT VANG (kim loai) +
      //   vien do-nau day + halo. Do tu ban mau khung 240s (「月額5,620円へ増額」). Dung cho
      //   scene DAT nhat (con so, tin vui); dung khap noi thi mat suc nhan.
      'telop-gold',
      // telop-band: BANNER TRANG chay het be ngang o dinh khung + chu den. Do tu ban mau
      //   khung 25s. Dung khi footage ben duoi qua nhieu chi tiet, chu tran khong doc noi.
      'telop-band',
      // yawa-*: kenh 人生哲学の夜話 (2026-10-01) — chu 明朝 hien dan, xem YawaText.tsx
      'yawa-chapter',
      'yawa-reveal',
      'yawa-chip',
      'yawa-keyword',
      'yawa-quote',
      'yawa-letter',
      // kin-*: kenh 他人の目を気にしない心理学 (2026-10-01) — chip/callout/出典/the so, chi fade, xem KinText.tsx
      'kin-chip',
      'kin-callout',
      'kin-source',
      'kin-stat',
      // tei-*: kenh 定年後のこころ研究室 (2026-10-01) — chu hien THEO LOI DOC, nhan mem, xem TeiText.tsx
      'tei-label',
      'tei-reveal',
    ])
    .default('plain'),
  color: z.string().default('#FFE01B'),
  // key into src/effects/textAnimations.ts registry
  animation: z.string().default('pop'),
  animationParams: z.record(z.string(), z.unknown()).default({}),
  layout: LayoutOverrideSchema.prefault({}), // preset supplies defaults
  fontSize: z.number().nullable().default(null),
});

export const FootageClipSchema = ClipBase.extend({
  kind: z.literal('video'), // full-bleed/boxed footage: mp4 OR still image
  asset: z.string(),
  trimStartFrames: z.number().int().min(0).default(0),
  fit: z.enum(['cover', 'contain']).default('cover'),
  layout: LayoutOverrideSchema.prefault({}), // empty = fullscreen
  // pan = slow drift · zoom-punch = fast beat-hit zoom (speed-ramp feel)
  motion: z.enum(['none', 'pan', 'zoom-punch']).default('none'),
  // đổi tốc độ (playbackRate cho video) · mặt nạ gương (lật ngang)
  speed: z.number().positive().default(1),
  mirror: z.boolean().default(false),
  volume: z.number().min(0).default(0),
  // frame (tuy chon, kinishinai 2026-10-02): khung con BO GOC + vien + bong do — nguoi dan "dung canh" anh ke chuyen
  // thay vi chiem ca man hinh (user: phan podcast "ghep cho co"). Khong khai = nhu cu.
  frame: z
    .object({
      radius: z.number().default(0),
      border: z.number().default(0),
      borderColor: z.string().default('#F6EEDE'),
      shadow: z.string().nullable().default(null),
    })
    .nullable()
    .default(null),
  // dissolve: overlap this clip with the previous one and fade it in
  fadeInFrames: z.number().int().min(0).default(0),
  // linear-mask reveal (CapCut 线性蒙版): wipe the clip in over N frames
  wipeInFrames: z.number().int().min(0).default(0),
  wipeDir: z.enum(['left', 'right', 'up', 'down']).default('left'),
  // curl reveal ("lật trang") — clip mới hiện dần theo một đường CHÉO, kèm dải sáng
  // ở mép và bóng đổ, đọc ra như trang giấy đang được lật. Khác `wipeIn` ở chỗ mép
  // là đường chéo + có rim sáng, nên nó không giống màn wipe phẳng của CapCut.
  // ⚠️ Đây là XẤP XỈ 2D: lật trang thật cần warp 3D (WebGL). Xem ghi chú trong
  //    Footage.tsx trước khi hứa với ai là "giống y bản mẫu".
  curlInFrames: z.number().int().min(0).default(0),
  curlDir: z.enum(['tl', 'tr', 'bl', 'br']).default('br'),
  // CapCut-style color filter (CSS filter units; all optional = no filter)
  filter: z
    .object({
      brightness: z.number().optional(), // 1 = neutral
      contrast: z.number().optional(), // 1 = neutral
      saturate: z.number().optional(), // 1 = neutral
      grayscale: z.number().optional(), // 0..1
      sepia: z.number().optional(), // 0..1
      blur: z.number().optional(), // px
    })
    .prefault({}),
});

// ---------------------------------------------------------------------------
// fx — lop trang tri "hoa la canh" (dong xu bay, sparkle, mui ten phat sang...)
// Ban mau BAKE nhung thu nay vao anh AI. Minh KHONG the: Veo khong dat duoc mui ten
// dung cho, va no khong viet duoc chu. Nen lop nay do REMOTION ve — doi lai thi no
// DONG that (xu bay, tia quay), sac net tuyet doi, va sua duoc ma khong phai gen lai.
// 🔴 MOI thu ngau nhien phai TIEN DINH theo (seed, index) — Remotion render tung frame
//    doc lap nen `Math.random()` = hat nhay lung tung moi frame.
export const FxClipSchema = ClipBase.extend({
  kind: z.literal('fx'),
  variant: z.enum([
    'coins',    // dong xu vang bay len + xoay
    'sparkle',  // sao 4 canh lap lanh
    'arrow',    // mui ten lon do->vang, ve dan roi giu, co glow
    'rays',     // 集中線 tia tu tam, quay cham
    'glow',     // quang sang vang toa ra tu mot diem
    'confetti', // giay mau roi (tin vui)
    // ── hai variant CANH BAO, them 2026-09-07 ──────────────────────────────
    // Ly do ra doi: nho Veo lam "vat phat sang do" thi no TO DO BAN TAY (nhin ra
    // tay bi son/bong, khong ra anh sang) — do tren clip task_005. Hieu ung canh
    // bao phai do REMOTION ve, dung nguyen tac "Veo lo nguoi + boi canh".
    'vignette', // quang toi mau o RIA khung, tho theo nhip — khong cham vao nguoi
    'stampx',   // dau X do dap xuong giua khung roi rung nhe
    // ── ba variant EM cho yawa (2026-10-01): khong pulse, khong nhay ─────────
    'dust',      // bui sang/bokeh troi len cham, mo
    'vignette-soft', // vien toi CO DINH (khong tho)
    'grain',     // hat phim rat nhe
  ]),
  density: z.number().int().min(1).max(60).default(14),
  color: z.string().default('#FFC83A'),
  seed: z.number().int().default(1),
  // vung hoat dong (phan tram khung): mac dinh full
  area: z
    .object({
      x: z.number().default(0),
      y: z.number().default(0),
      w: z.number().default(100),
      h: z.number().default(100),
    })
    .prefault({}),
  opacity: z.number().min(0).max(1).default(1),
  fadeInFrames: z.number().int().min(0).default(8),
  fadeOutFrames: z.number().int().min(0).default(10),
  // rieng 'arrow': huong + do nghieng
  dir: z.enum(['up', 'upright', 'right', 'down']).default('upright'),
});

export const AudioClipSchema = ClipBase.extend({
  kind: z.literal('audio'),
  asset: z.string(), // "assets/voice.wav" or shared "sfx/pop.wav"
  volume: z.number().min(0).default(1),
  trimStartFrames: z.number().int().min(0).default(0),
});

export const ClipSchema = z.discriminatedUnion('kind', [
  BackgroundClipSchema,
  StickerClipSchema,
  TextClipSchema,
  FootageClipSchema,
  FxClipSchema,
  AudioClipSchema,
]);
export type Clip = z.infer<typeof ClipSchema>;

// ---------------------------------------------------------------------------
// tracks — array order = z-order (first track renders at the bottom)
// ---------------------------------------------------------------------------

export const TrackTypeSchema = z.enum([
  'background',
  'video',
  'sticker',
  'text',
  'fx',
  'audio',
  'caption',
]);

export const TrackSchema = z.object({
  id: z.string(),
  name: z.string(),
  type: TrackTypeSchema,
  muted: z.boolean().default(false),
  hidden: z.boolean().default(false),
  locked: z.boolean().default(false),
  clips: z.array(ClipSchema).default([]),
});
export type Track = z.infer<typeof TrackSchema>;

// ---------------------------------------------------------------------------
// captions — word-level for karaoke, line-level = clean subs.srt source
// ---------------------------------------------------------------------------

export const CaptionWordSchema = z.object({
  text: z.string(),
  startMs: z.number(),
  endMs: z.number(),
  lineIndex: z.number().int(),
});

export const CaptionLineSchema = z.object({
  text: z.string(),
  startMs: z.number(),
  endMs: z.number(),
});

export const CaptionsSchema = z.object({
  source: z
    .enum(['none', 'voicevox-mora', 'whisper', 'srt-interpolated'])
    .default('none'),
  style: z.string().default('outline'), // preset name (per-channel template)
  enabled: z.boolean().default(true),
  fontSize: z.number().default(44), // px at 1080p
  lines: z.array(CaptionLineSchema).default([]),
  words: z.array(CaptionWordSchema).default([]),
});

// ---------------------------------------------------------------------------
// theme — overrides on top of templates/<channel>.json
// ---------------------------------------------------------------------------

export const ThemeSchema = z.object({
  palette: z
    .object({
      bgTop: z.string().default('#2A3A58'),
      bgBottom: z.string().default('#182236'),
      accent: z.string().default('#FFD700'),
    })
    .prefault({}),
  fontFamily: z
    .string()
    .default('"Yu Gothic", "Meiryo", Arial Black, sans-serif'),
  canvasColor: z.string().default('#F2EDE4'),
});

// ---------------------------------------------------------------------------
// project root
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// brand — lop nhan dien dan CUNG moi frame (logo goc / mascot / nut dang ky).
// Ban mau co du 3 thu nay o 100% frame. Khai o ROOT chu khong phai tung clip:
// khai tung clip thi 1 video = them ~113 clip rac vao timeline.
// ⚠️ `null` mac dinh => 15 project cu KHONG doi gi.
// ---------------------------------------------------------------------------
export const BrandSchema = z.object({
  logo: z.string().nullable().default(null),      // PNG goc TREN-PHAI
  mascot: z.string().nullable().default(null),    // PNG cutout goc DUOI-PHAI (tu the mac dinh)
  // mascotPoses: doi tu the theo moc giay — mascot "chuyen dong" that su, khong chi bob.
  // [{atSec, asset}] — tu the co hieu luc tu atSec toi moc sau.
  mascotPoses: z
    .array(z.object({atSec: z.number().min(0), asset: z.string()}))
    .default([]),
  // mascotVideo: WebM VP9 CO ALPHA (mascot dong). Uu tien hon `mascot`/`mascotPoses`.
  // mp4 KHONG mang duoc alpha -> dan vao la mot cai hop den o goc man.
  mascotVideo: z.string().nullable().default(null),
  mascotVideoFrames: z.number().int().min(1).default(240),
  mascotH: z.number().default(300),
  logoH: z.number().default(120),
  subscribe: z.boolean().default(false),          // nut SUBSCRIBE animate goc DUOI-TRAI
  // dat lech len de khong dam vao phu de (phu de cao ~110px o day khung)
  bottomOffset: z.number().default(24),
  // subscribeBottom: le day RIENG cho nut SUBSCRIBE. `null` = dung `bottomOffset`.
  // 🔴 Vi sao phai tach (them 2026-09-10, nenkin 22): mascot va SUBSCRIBE dung CHUNG
  //    `bottomOffset`, nen ha nut xuong la ha luon mascot. Hai thu o hai goc khac nhau,
  //    va khe trong duoi chung khac nhau: mascot phai tranh timestamp cua YouTube o goc
  //    DUOI-PHAI, con SUBSCRIBE (duoi-TRAI) chi phai tranh dai phu de.
  //    Them dang nullable nen 15 project cu khong doi mot pixel.
  subscribeBottom: z.number().nullable().default(null),
});

export const SceneMarkerSchema = z.object({
  id: z.string(),
  atFrame: z.number().int().min(0),
  label: z.string().default(''),
});

export const ProjectSchema = z.object({
  version: z.literal(1),
  meta: z.object({
    name: z.string(), // folder name under projects/ and public/projects/
    channel: z.string().nullable().default(null),
    templateRef: z.string().nullable().default(null),
    fps: z.number().int().min(1).default(30),
    width: z.number().int().min(16).default(1920),
    height: z.number().int().min(16).default(1080),
    createdAt: z.string().default(''),
    modifiedAt: z.string().default(''),
  }),
  timeline: z.object({
    durationInFrames: z.number().int().min(1),
  }),
  sceneMarkers: z.array(SceneMarkerSchema).default([]),
  tracks: z.array(TrackSchema).default([]),
  captions: CaptionsSchema.prefault({}),
  theme: ThemeSchema.prefault({}),
  brand: BrandSchema.nullable().default(null),
});
export type Project = z.infer<typeof ProjectSchema>;

// Parse with a readable error message (used by server, editor and renderer).
export const parseProject = (data: unknown): Project => {
  const res = ProjectSchema.safeParse(data);
  if (!res.success) {
    const issues = res.error.issues
      .slice(0, 5)
      .map((i) => `${i.path.join('.')}: ${i.message}`)
      .join(' | ');
    throw new Error(`project.json invalid: ${issues}`);
  }
  return res.data;
};
