#!/usr/bin/env python3
"""
스킬 이펙트 스프라이트시트 생성기.

기존 fx_H2O.png(눈송이가 회전·확산하는 86프레임 가로 스트립)와 같은 형식으로
아직 없는 분자들의 시트를 만든다. Flow 같은 이미지 생성기는 '연속된 애니메이션
프레임'을 못 만들기 때문에 절차적으로 그리는 쪽이 맞다.

형식: 100px 정사각 프레임을 가로로 이어붙인 PNG (프레임 수 = 가로/세로).
      game.html 의 playFxSheet() 가 이 규칙으로 재생한다.

  python tools/fx_sheet.py            # 없는 것만 전부 생성
  python tools/fx_sheet.py NaCl       # 하나만
"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont

SIZE   = 100          # 프레임 한 변
FRAMES = 48           # 프레임 수 (기존 86보다 적지만 재생시간은 코드가 1초로 정규화)
FONT   = 'C:/Windows/Fonts/seguisym.ttf'

# 분자별 글리프와 색. 화학적 인상에 맞춰 고른다.
#   글리프는 Segoe UI Symbol 에 있는 것만 쓴다(이모지는 컬러라 색 지정이 안 먹는다).
SPEC = {
    # 염기 — 미끌한 물방울 느낌, 청록
    'NaOH':   dict(glyph='●', colors=[(150,255,220),(90,220,255),(255,255,255)], spin=+1),
    'CaOH2':  dict(glyph='●', colors=[(170,255,210),(120,230,255),(255,255,255)], spin=+1),
    # 산 — 날카로운 마름모, 연두/노랑
    'H2SO4':  dict(glyph='◆', colors=[(210,255,120),(255,240,130),(255,255,255)], spin=-1),
    # 기체 — 흐릿한 원, 옅은 색
    'NH3':    dict(glyph='○', colors=[(190,230,255),(220,255,240),(255,255,255)], spin=+1),
    # 염 — 각진 결정, 흰색 계열에 포인트 색
    'NaCl':   dict(glyph='◇', colors=[(255,255,255),(220,240,255),(190,220,255)], spin=+1),
    'CaCO3':  dict(glyph='◇', colors=[(255,250,235),(235,220,190),(255,255,255)], spin=-1),
    'NaNO3':  dict(glyph='◇', colors=[(255,255,255),(255,240,200),(230,230,255)], spin=+1),
    'Na2SO4': dict(glyph='◇', colors=[(255,255,255),(230,235,255),(200,215,245)], spin=-1),
    'BaSO4':  dict(glyph='◆', colors=[(255,255,255),(245,245,250),(215,225,240)], spin=+1),
    'CaCl2':  dict(glyph='◇', colors=[(255,245,225),(255,255,255),(225,240,255)], spin=-1),
    'MgCl2':  dict(glyph='◇', colors=[(240,255,255),(255,255,255),(205,235,255)], spin=+1),
    'KCl':    dict(glyph='◇', colors=[(245,235,255),(255,255,255),(215,200,255)], spin=-1),
}


def make_sheet(key, spec, seed=None):
    random.seed(seed if seed is not None else hash(key) & 0xffff)
    font_big = ImageFont.truetype(FONT, 26)
    font_sm  = ImageFont.truetype(FONT, 16)

    # 입자를 링 위에 배치한다. 프레임이 진행되면 링이 커지고 회전하며 옅어진다.
    N = 14
    parts = []
    for i in range(N):
        parts.append(dict(
            ang   = random.uniform(0, math.tau),
            rad0  = random.uniform(4, 14),
            speed = random.uniform(0.9, 1.6),
            big   = random.random() < 0.55,
            col   = random.choice(spec['colors']),
            wob   = random.uniform(0, math.tau),
        ))

    sheet = Image.new('RGBA', (SIZE * FRAMES, SIZE), (0, 0, 0, 0))
    for f in range(FRAMES):
        t = f / (FRAMES - 1)                      # 0 → 1
        frame = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        d = ImageDraw.Draw(frame)
        # 앞부분은 터지듯 빠르게, 뒤로 갈수록 느리게 퍼진다
        ease = 1 - (1 - t) ** 2
        for p in parts:
            rad = p['rad0'] + ease * 34 * p['speed']
            ang = p['ang'] + spec['spin'] * ease * 2.2 + math.sin(t * 6 + p['wob']) * .25
            x = SIZE / 2 + math.cos(ang) * rad
            y = SIZE / 2 + math.sin(ang) * rad
            # 등장은 즉시, 퇴장은 서서히
            a = 255 if t < .12 else int(255 * max(0.0, 1 - (t - .12) / .88) ** 1.3)
            if a <= 4:
                continue
            fnt = font_big if p['big'] else font_sm
            d.text((x, y), spec['glyph'], font=fnt, anchor='mm',
                   fill=(*p['col'], a))
        sheet.paste(frame, (f * SIZE, 0))
    return sheet


if __name__ == '__main__':
    want = sys.argv[1:] or list(SPEC)
    os.makedirs('assets/fx', exist_ok=True)
    for key in want:
        if key not in SPEC:
            print('알 수 없는 키:', key); continue
        out = 'assets/fx/fx_%s.png' % key
        make_sheet(key, SPEC[key]).save(out, 'PNG', optimize=True)
        kb = os.path.getsize(out) / 1024
        print('  fx_%-8s %d프레임  %6.1fKB' % (key, FRAMES, kb))
