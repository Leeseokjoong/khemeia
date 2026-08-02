#!/usr/bin/env python3
"""
원소 카드 배경 제거 — 흰 여백을 잘라내고 둥근 모서리를 투명하게.

Flow 결과물은 카드 주위에 흰 배경이 12~15px 남는다. 그대로 쓰면 어두운 카드
뷰어 위에 흰 테두리가 뜬다. 여기서 두 가지를 한다.

 1) 흰 여백을 실측해 잘라낸다 (카드마다 여백 폭이 0~27px로 제각각이라 고정값 금지)
 2) 모서리 둥글리기는 여기서 하지 않고 CSS border-radius 에 맡긴다.
    투명 PNG로 만들면 장당 850KB(12장 10MB)가 되는데, JPEG면 110KB로 끝나고
    화면에 보이는 결과는 같다.

  python tools/card_trim.py            # raw_card/ 전부 처리 → assets/card/
  python tools/card_trim.py rare       # raw_rare/ 전부 처리 → assets/card/rare_*.jpg
"""
import os, glob, sys
import numpy as np
from PIL import Image

OUT_W = 600          # 카드 뷰어가 최대 180px 폭이라 레티나까지 충분
WHITE = 245          # 이 이상이면 배경 흰색으로 본다


def trim_white(im):
    """흰 여백을 실측해 잘라낸다."""
    a = np.array(im.convert('RGB')).astype(int)
    notwhite = (a.min(axis=2) < WHITE)
    rows = np.where(notwhite.any(axis=1))[0]
    cols = np.where(notwhite.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return im, (0, 0, 0, 0)
    box = (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)
    margin = (rows[0], im.size[1] - rows[-1] - 1, cols[0], im.size[0] - cols[-1] - 1)
    return im.crop(box), margin


def process(src, dst):
    """흰 여백만 잘라 JPEG로 저장한다.

    모서리 둥글리기는 PNG 투명도가 아니라 CSS border-radius 로 한다.
    사진 같은 그림을 PNG로 저장하면 장당 850KB(12장 10MB)까지 부는데,
    JPEG면 110KB면 되고 결과는 화면상 동일하다.
    """
    im = Image.open(src)
    im, margin = trim_white(im)
    w, h = im.size
    im = im.convert('RGB').resize((OUT_W, round(h * OUT_W / w)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    im.save(dst, 'JPEG', quality=86, optimize=True, progressive=True)
    kb = os.path.getsize(dst) / 1024
    print('  %-20s %s  여백 상%d 하%d 좌%d 우%d  %6.1fKB'
          % (os.path.basename(dst), im.size, *margin, kb))


def make_thumb(src, dst, size=150):
    """손패용 썸네일 — 카드 중앙 삽화만 잘라낸다.

    손패 카드는 68px밖에 안 돼서 카드 전체를 넣으면 금테와 모서리 방패만 보이고
    그림이 뭉개진다. 가운데 삽화(마법진 안의 불꽃·결정 등)만 잘라 쓰면
    작은 크기에서도 무엇인지 알아볼 수 있다.
    """
    im, _ = trim_white(Image.open(src))
    w, h = im.size
    # 금박 테두리를 걷어낸 안쪽 영역. 세로는 위아래 방패를 피해 살짝 더 조인다.
    box = (int(w * .17), int(h * .20), int(w * .83), int(h * .80))
    im = im.crop(box).convert('RGB')
    # 손패 칸이 3:4 이므로 같은 비율로 맞춘다
    tw, th = size, round(size * 4 / 3)
    im = im.resize((tw, th), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=84, optimize=True)
    return os.path.getsize(dst) / 1024


def run_rare():
    """희귀 분자 카드 — 손패에만 쓰이므로 썸네일은 만들지 않는다.

    희귀 카드는 카드 상세 뷰어(showCard)에 뜨지 않고 손패에서만 보인다.
    손패는 겹쳐 들기 때문에 왼쪽 띠(=좌상단 분자식 방패)만 보이는데,
    그건 card_*.jpg 와 똑같이 background-position:left top 으로 해결된다.
    """
    files = sorted(glob.glob('raw_rare/rare_*'))
    if not files:
        raise SystemExit('raw_rare/ 에 카드가 없습니다')
    for f in files:
        key = os.path.basename(f).replace('rare_', '').rsplit('.', 1)[0]
        process(f, 'assets/card/rare_%s.jpg' % key)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'rare':
        run_rare()
        raise SystemExit
    files = sorted(glob.glob('raw_card/card_*'))
    if not files:
        raise SystemExit('raw_card/ 에 카드가 없습니다')
    tot = 0
    for f in files:
        el = os.path.basename(f).replace('card_', '').rsplit('.', 1)[0]
        process(f, 'assets/card/card_%s.jpg' % el)
        tot += make_thumb(f, 'assets/card/thumb_%s.jpg' % el)
    print('  썸네일 12종 합계 %.0fKB' % tot)
