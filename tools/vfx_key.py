# -*- coding: utf-8 -*-
"""
검은 배경 VFX 이미지를 알파 PNG로 키잉한다.

Flow 는 '연속된 애니메이션 프레임'을 못 만든다 → 한 장을 코드로 확대·회전·페이드시키고,
x4 로 뽑은 4장은 **발동할 때마다 무작위로 고르는 변형**으로 쓴다(프레임 아님).

  python tools/vfx_key.py flame        # ~/Downloads/vfx_flame_1..4.png → assets/fx/
"""
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # cp949 콘솔에서도 깨지지 않게
from PIL import Image
import numpy as np

def key_one(src, dst, size=384):
    a = np.array(Image.open(src).convert('RGB')).astype(float)
    H, W = a.shape[:2]
    a[int(H*0.86):, int(W*0.86):] = 0          # 우하단 워터마크 제거
    lum = a.max(axis=2)
    alpha = np.clip((lum-14)/(150-14), 0, 1)**0.85 * 255
    im = Image.fromarray(np.dstack([a, alpha]).astype('uint8'), 'RGBA')
    m = np.array(im)[:, :, 3] > 6
    ys, xs = np.where(m)
    if not len(xs): return False
    im = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
    s = max(im.size)
    sq = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    sq.paste(im, ((s-im.width)//2, (s-im.height)//2))
    # 📦 384px + 128색 팔레트로 굽는다. RGBA 512px(553KB) 대비 **1/9(64KB)** 인데
    #    배경 위에 screen 합성해 나란히 비교해도 차이가 안 보인다(2026-08-03 실측).
    #    이펙트 8종 × 변형 4장 = 32장이라 용량이 그대로면 16MB, 줄이면 2MB.
    r = sq.resize((size, size), Image.LANCZOS)
    r.quantize(colors=128, method=Image.FASTOCTREE).save(dst, optimize=True)
    return True

if __name__ == '__main__':
    kind = sys.argv[1]
    D = os.path.join(os.path.expanduser('~'), 'Downloads')
    out = 'assets/fx'
    os.makedirs(out, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(D, 'vfx_%s_*.png' % kind))):
        i = os.path.basename(f).rsplit('_', 1)[1].split('.')[0]
        dst = os.path.join(out, 'vfx_%s_%s.png' % (kind, i))
        if key_one(f, dst):
            n += 1
            print('  ✔ %-22s %.0fKB' % (os.path.basename(dst), os.path.getsize(dst)/1024))
    # 단일본 폴백도 1번으로 만들어 둔다
    one = os.path.join(out, 'vfx_%s_1.png' % kind)
    if os.path.exists(one):
        Image.open(one).save(os.path.join(out, 'vfx_%s.png' % kind), optimize=True)
        print('  ✔ vfx_%s.png (폴백)' % kind)
    print('%s — %d장 처리' % (kind, n))
