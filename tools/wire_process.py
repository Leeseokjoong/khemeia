#!/usr/bin/env python3
"""
철사 테두리 후처리 — 밝기→알파 변환 + 슬라이스 실측.

Flow(Nano Banana 2)에서 뽑은 검은 배경 원본을 게임에서 쓸 투명 PNG로 바꾼다.
철사테두리_스펙.md 의 후처리 1~4단계를 그대로 구현했다.

  python tools/wire_process.py raw/wire_frost_raw.png assets/wire_frost.png

전체 일괄 처리:
  python tools/wire_process.py --batch raw/ assets/

원본은 '평평한 순수 검정 위에 빛나는 선' 이므로, 밝기가 곧 알파다.
검정(밝기 0) = 완전 투명, 빛나는 선(밝기 255) = 완전 불투명.
"""
import sys, os, glob
import numpy as np
from PIL import Image

# 이 아래 밝기는 배경 잡티로 보고 완전히 죽인다 (JPEG/생성 노이즈 제거)
# 낮게 잡는다 — 높이면 선 주변 은은한 발광이 통째로 날아가 선이 앙상해진다
FLOOR = 12
# 이 위 밝기는 완전 불투명으로 올린다 (선 중심이 반투명해지지 않게)
CEIL = 235
# 슬라이스 측정 시 '잉크가 있다'고 볼 알파 기준
INK = 32
# 슬라이스에 주는 여유 (선이 잘리지 않게)
SLICE_PAD = 12


def brightness_to_alpha(im):
    """밝기를 알파로. 색은 살리고 검정만 투명하게 만든다."""
    a = np.array(im.convert("RGBA")).astype(np.float32)
    rgb = a[..., :3]

    # 지각 밝기 (녹색 가중) — 단순 평균보다 선이 고르게 남는다
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]

    # FLOOR~CEIL 을 0~255 로 늘려서, 바닥 잡티는 죽이고 선은 진하게
    alpha = (lum - FLOOR) / (CEIL - FLOOR)
    alpha = np.clip(alpha, 0.0, 1.0) * 255.0

    # 색 복원: 알파가 곱해진 상태(검정과 섞인 상태)이므로 되나눠서
    # 반투명 가장자리가 탁한 회색이 되는 걸 막는다
    safe = np.maximum(alpha / 255.0, 1e-3)[..., None]
    rgb_un = np.clip(rgb / safe, 0, 255)

    # 채도 낮은 흰 잔재 제거(스펙 3단계): 밝기는 낮은데 색도 없는 픽셀은 배경 찌꺼기
    mx = rgb_un.max(axis=2)
    mn = rgb_un.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    residue = (sat < 0.15) & (lum < 70)
    alpha[residue] = 0.0

    out = np.dstack([rgb_un, alpha]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def measure_slice(im):
    """네 변에서 잉크가 끝나는 지점을 재서 border-image slice 값을 제안한다."""
    al = np.array(im)[..., 3]
    h, w = al.shape
    ink = al > INK

    rows = ink.mean(axis=1)
    cols = ink.mean(axis=0)

    def band_end(prof):
        """가장자리를 따라 흐르는 '주선'이 끝나는 지점.

        안쪽으로 뻗은 소용돌이는 일부러 뺀다. 잉크가 완전히 없어지는 곳까지
        슬라이스를 잡으면 모서리 조각이 너무 커져서, 패널이 작을 때 모서리
        장식만 보이고 변이 사라진다. 불철사(shipped slice=105)를 이 기준으로
        재면 107이 나온다 — 손으로 맞춘 값과 일치.
        """
        third = len(prof) // 3
        peak_i = int(np.argmax(prof[:third]))
        peak_v = float(prof[peak_i])
        thresh = peak_v * 0.25          # 주선 밀도의 1/4로 떨어지면 선이 끝난 것
        for i in range(peak_i, len(prof) // 2):
            if prof[i] <= thresh:
                return i
        return third

    ends = [
        band_end(rows),            # 위
        band_end(rows[::-1]),      # 아래
        band_end(cols),            # 왼쪽
        band_end(cols[::-1]),      # 오른쪽
    ]
    return max(ends) + SLICE_PAD, ends


def process(src, dst):
    im = Image.open(src)
    out = brightness_to_alpha(im)
    sl, ends = measure_slice(out)
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    kb = os.path.getsize(dst) / 1024
    print(f"{os.path.basename(dst):22s} {out.size[0]}x{out.size[1]}  "
          f"slice={sl:4d} (변별 끝: {ends})  {kb:7.1f}KB")
    return sl


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--batch":
        srcdir, dstdir = args[1], args[2]
        files = sorted(glob.glob(os.path.join(srcdir, "*.png")) +
                       glob.glob(os.path.join(srcdir, "*.jpg")))
        if not files:
            sys.exit(f"원본 없음: {srcdir}")
        for f in files:
            key = os.path.splitext(os.path.basename(f))[0]
            key = key.replace("_raw", "").replace("wire_", "")
            process(f, os.path.join(dstdir, f"wire_{key}.png"))
    elif len(args) == 2:
        process(args[0], args[1])
    else:
        sys.exit(__doc__)
