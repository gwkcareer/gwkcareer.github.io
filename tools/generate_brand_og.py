#!/usr/bin/env python3
# 블로그 대표 OG 이미지 생성 — 시안 B (크림 카드, 1200x630)
import os
from PIL import Image, ImageDraw, ImageFont

BLOG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT    = os.path.join(BLOG_ROOT, 'assets', 'img', 'og-brand.png')
AVATAR    = os.path.join(BLOG_ROOT, 'assets', 'img', '에비츄우.jpg')

W, H = 1200, 630

BG      = (253, 248, 244)
BORDER  = (232, 216, 204)
GRAD_S  = (201, 124,  74)
GRAD_M  = (232, 168, 124)
GRAD_E  = (245, 200, 160)
TITLE_C = (61,  43,  31)
ROLE_C  = (201, 124,  74)

FONT_CANDIDATES = [
    'C:/Windows/Fonts/malgunbd.ttf',
    'C:/Windows/Fonts/malgun.ttf',
    'C:/Windows/Fonts/gulim.ttc',
    '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
]

def find_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("폰트를 찾을 수 없습니다")

def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient_bar(draw):
    for x in range(W):
        t = x / (W - 1)
        c = lerp(GRAD_S, GRAD_M, t * 2) if t < 0.5 else lerp(GRAD_M, GRAD_E, (t - 0.5) * 2)
        draw.line([(x, 0), (x, 7)], fill=c)

def deco_circle(img):
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    cx, cy, radius = W - 100, H - 100, 180
    for r in range(radius, 0, -3):
        t = r / radius
        alpha = 0 if t > 0.7 else int(20 * (1 - t / 0.7))
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*GRAD_S, alpha))
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

def circle_avatar(path, size):
    ava  = Image.open(path).convert('RGBA').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    out  = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(ava, (0, 0), mask)
    return out

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    font_path = find_font()

    img  = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 테두리
    draw.rectangle([0, 0, W - 1, H - 1], outline=BORDER, width=3)

    # 상단 그라디언트 바
    gradient_bar(draw)

    # 아바타 (240px)
    AVA_SIZE  = 240
    AVA_X     = 120
    AVA_Y     = (H - AVA_SIZE) // 2

    if os.path.exists(AVATAR):
        ava = circle_avatar(AVATAR, AVA_SIZE)
        img.paste(ava, (AVA_X, AVA_Y), ava)
        draw = ImageDraw.Draw(img)
        draw.ellipse([AVA_X, AVA_Y, AVA_X + AVA_SIZE, AVA_Y + AVA_SIZE],
                     outline=BORDER, width=5)

    # 텍스트 영역
    TEXT_X = AVA_X + AVA_SIZE + 80

    f_name = ImageFont.truetype(font_path, 72)
    f_role = ImageFont.truetype(font_path, 32)

    name = '기록하자 에비츄우'
    role = 'BACKEND DEVELOPER'

    name_h = draw.textbbox((0, 0), name, font=f_name)[3]
    role_h = draw.textbbox((0, 0), role, font=f_role)[3]
    gap    = 24
    group_h = name_h + gap + role_h

    name_y = (H - group_h) // 2
    role_y = name_y + name_h + gap

    draw.text((TEXT_X, name_y), name, font=f_name, fill=TITLE_C)
    draw.text((TEXT_X, role_y), role, font=f_role, fill=ROLE_C)

    img = deco_circle(img)
    img.save(OUTPUT)
    print(f"저장 완료: {OUTPUT}")

if __name__ == '__main__':
    main()
