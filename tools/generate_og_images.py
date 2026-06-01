#!/usr/bin/env python3
# OG 이미지 생성 — 시안 1 (크림 카드 + 브라운 그라디언트)
# HTML 시안(600×315)을 정확히 2배 스케일: 1200×630
import sys, os, json, glob
from PIL import Image, ImageDraw, ImageFont

# Bold 계열 우선 탐색 (시안 font-weight: 800 대응)
FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Bold.otf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf',
    '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
]

def find_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            print(f"[OG] font: {path}", flush=True)
            return path
    found = (glob.glob('/usr/share/fonts/**/*CJK*Bold*', recursive=True) +
             glob.glob('/usr/share/fonts/**/*CJK*', recursive=True) +
             glob.glob('/usr/share/fonts/**/*anum*Bold*', recursive=True) +
             glob.glob('/usr/share/fonts/**/*anum*', recursive=True))
    ttf = [f for f in found if f.endswith(('.ttf', '.otf', '.ttc'))]
    if ttf:
        print(f"[OG] fallback font: {ttf[0]}", flush=True)
        return ttf[0]
    raise FileNotFoundError("한글 폰트 없음")

# ── 캔버스 (HTML 600×315 × 2배) ──────────────────────────────────────────────
W, H = 1200, 630

# ── 색상 (HTML 시안 그대로) ───────────────────────────────────────────────────
BG      = (253, 248, 244)   # #fdf8f4
BORDER  = (232, 216, 204)   # #e8d8cc
GRAD_S  = (201, 124,  74)   # #c97c4a  gradient start
GRAD_M  = (232, 168, 124)   # #e8a87c  gradient mid
GRAD_E  = (245, 200, 160)   # #f5c8a0  gradient end
CHIP_C  = '#c97c4a'
TITLE_C = '#3d2b1f'
NAME_C  = '#5a3e30'
URL_C   = '#c0a898'
DATE_C  = '#c0a898'
AVA_BG  = (245, 237, 232)   # #f5ede8
AVA_BD  = (217, 200, 184)   # #d9c8b8

# ── 레이아웃 수치 (HTML px × 2) ──────────────────────────────────────────────
PAD_X   = 96   # 48px × 2
PAD_Y   = 88   # 44px × 2
BAR_H   = 8    # 4px × 2  (accent gradient bar)
BORDER_W= 3    # 1.5px × 2

# typography (HTML px × 2)
SZ_CHIP  = 24  # 12px × 2
SZ_TITLE = 68  # 34px × 2
SZ_NAME  = 28  # 14px × 2
SZ_URL   = 24  # 12px × 2
SZ_DATE  = 26  # 13px × 2

LH_TITLE = int(SZ_TITLE * 1.35)  # line-height: 1.35 → 91px
MT_TITLE = 28  # margin-top 14px × 2

AVA_D    = 76  # 38px × 2 (avatar diameter)
AVA_BD_W = 4   # 2px × 2
AVA_GAP  = 24  # gap 12px × 2

# ── 유틸 ─────────────────────────────────────────────────────────────────────
def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient_bar(draw):
    """상단 그라디언트 바: #c97c4a → #e8a87c → #f5c8a0"""
    for x in range(W):
        t = x / (W - 1)
        c = lerp(GRAD_S, GRAD_M, t * 2) if t < 0.5 else lerp(GRAD_M, GRAD_E, (t - 0.5) * 2)
        draw.line([(x, 0), (x, BAR_H - 1)], fill=c)

def deco_circle(img):
    """우하단 은은한 원: rgba(201,124,74,0.08), right:-60 bottom:-60, 320×320"""
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # center = (W - 60 - 160, H - 60 - 160) → (W-220+160, H-220+160) = (W-60, H-60) 잠깐
    # HTML: right:-30px, bottom:-30px → right edge at card_right+30, bottom edge at card_bottom+30
    # With width=160px: left=card_right+30-160=W-130, top=H-130
    # center = (W-130+80, H-130+80) = (W-50, H-50)  (at 2x: W-100, H-100)
    cx, cy, radius = W - 100, H - 100, 160  # radius = 160px (half of 320px)
    for r in range(radius, 0, -3):
        t = r / radius
        # radial-gradient: rgba(201,124,74,0.08) at 0% → transparent at 70%
        if t > 0.7:
            alpha = 0
        else:
            alpha = int(20 * (1 - t / 0.7))
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*GRAD_S, alpha))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ── 메인 렌더 ─────────────────────────────────────────────────────────────────
def render_og(title, tags, date, output_path):
    font_path = find_font()
    img  = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 테두리 (border: 1.5px solid #e8d8cc)
    draw.rectangle([0, 0, W - 1, H - 1], outline=BORDER, width=BORDER_W)

    # 상단 그라디언트 바
    gradient_bar(draw)

    # ── 상단 콘텐츠 ──
    f_chip  = ImageFont.truetype(font_path, SZ_CHIP)
    f_title = ImageFont.truetype(font_path, SZ_TITLE)

    # 칩+제목 그룹 높이 계산
    chip_h  = draw.textbbox((0, 0), tags or '#', font=f_chip)[3]
    lines   = wrap_text(draw, title, f_title, W - PAD_X * 2)
    n_lines = min(len(lines), 2)
    group_h = chip_h + MT_TITLE + LH_TITLE * n_lines

    # 수직 위치: 사용 가능 공간의 38% 지점에 그룹 배치 (짧은 제목도 쏠리지 않게)
    footer_top = H - PAD_Y - AVA_D  # 466px
    avail = footer_top - BAR_H      # 458px
    y = BAR_H + max(int((avail - group_h) * 0.38), PAD_Y - BAR_H)

    # 칩(태그)
    if tags:
        draw.text((PAD_X, y), tags, font=f_chip, fill=CHIP_C)

    # 제목
    title_y = y + chip_h + MT_TITLE
    for line in lines[:2]:
        draw.text((PAD_X, title_y), line, font=f_title, fill=TITLE_C)
        title_y += LH_TITLE

    # ── 푸터 (bottom of content area) ──

    # 아바타 (38px×2=76px circle, border 2px×2=4px)
    ax, ay = PAD_X, footer_top
    draw.ellipse([ax, ay, ax + AVA_D, ay + AVA_D], fill=AVA_BG)  # 배경

    avatar_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assets', 'img', '에비츄우.jpg')
    if os.path.exists(avatar_path):
        ava  = Image.open(avatar_path).convert('RGBA').resize((AVA_D, AVA_D), Image.LANCZOS)
        mask = Image.new('L', (AVA_D, AVA_D), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, AVA_D, AVA_D], fill=255)
        img.paste(ava, (ax, ay), mask)
        draw = ImageDraw.Draw(img)
    # border는 paste 이후에 덮어서 그려야 깔끔하게 나옴
    draw.ellipse([ax, ay, ax + AVA_D, ay + AVA_D], outline=AVA_BD, width=AVA_BD_W)

    # 이름 + URL (14px×2=28px / 12px×2=24px, gap 12px×2=24px from avatar)
    f_name = ImageFont.truetype(font_path, SZ_NAME)
    f_url  = ImageFont.truetype(font_path, SZ_URL)
    tx = PAD_X + AVA_D + AVA_GAP

    name_h  = draw.textbbox((0, 0), '기', font=f_name)[3]
    url_h   = draw.textbbox((0, 0), '기', font=f_url)[3]
    group_h = name_h + 4 + url_h
    ty = footer_top + (AVA_D - group_h) // 2  # 아바타 안에서 수직 중앙

    draw.text((tx, ty),              '기록하자 에비츄우',   font=f_name, fill=NAME_C)
    draw.text((tx, ty + name_h + 4), 'gwkcareer.github.io', font=f_url,  fill=URL_C)

    # 날짜 (13px×2=26px, 우측 정렬, 아바타 수직 중앙)
    if date:
        f_date  = ImageFont.truetype(font_path, SZ_DATE)
        date_w  = draw.textbbox((0, 0), date, font=f_date)[2]
        date_h  = draw.textbbox((0, 0), date, font=f_date)[3]
        draw.text(
            (W - PAD_X - date_w, footer_top + (AVA_D - date_h) // 2),
            date, font=f_date, fill=DATE_C)

    # 우하단 데코 원 (rgba(201,124,74,0.08))
    img = deco_circle(img)

    img.save(output_path)
    print(f"[OG] saved: {output_path}", flush=True)

if __name__ == '__main__':
    data = json.loads(sys.argv[1])
    render_og(data['title'], data['tags'], data['date'], data['output_path'])
