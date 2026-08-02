#!/usr/bin/env bash
# 효과음 후처리 — 앞뒤 무음 제거 → loudnorm -16 LUFS → 96kbps mp3
#
#   bash tools/sfx_process.sh raw_sfx/ assets/
#
# 일레븐랩스에서 받은 파일 이름을 최종 이름 그대로 두면 (extract.mp3 → sfx_extract.mp3)
# 알아서 sfx_ 접두사를 붙인다. 이미 sfx_ 로 시작하면 그대로 쓴다.
#
# 무음 제거를 먼저 하는 이유: 일레븐랩스 결과물은 앞에 100~300ms 정적이 붙는데,
# 그대로 두면 게임에서 타격 순간과 소리가 어긋나 반응이 굼뜨게 느껴진다.
set -euo pipefail

SRC="${1:?원본 폴더를 지정하세요}"
DST="${2:?출력 폴더를 지정하세요}"
mkdir -p "$DST"

# -50dB 이하를 무음으로 보고 앞/뒤를 잘라낸다 (areverse 로 뒤쪽도 같은 처리)
TRIM="silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0:detection=peak"
NORM="loudnorm=I=-16:TP=-1.5:LRA=11"

shopt -s nullglob
found=0
for f in "$SRC"/*.mp3 "$SRC"/*.wav; do
  found=1
  base="$(basename "${f%.*}")"
  [[ "$base" == sfx_* ]] || base="sfx_${base}"
  out="$DST/${base}.mp3"

  ffmpeg -hide_banner -loglevel error -y -i "$f" \
    -af "${TRIM},areverse,${TRIM},areverse,${NORM}" \
    -ar 44100 -b:a 96k "$out"

  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out")
  kb=$(( $(stat -c%s "$out") / 1024 ))
  printf '%-20s %5.2fs %4dKB\n' "$(basename "$out")" "$dur" "$kb"
done

[[ $found -eq 1 ]] || { echo "원본 없음: $SRC"; exit 1; }
echo "완료 — game.html 은 파일만 있으면 자동으로 집어간다 (SFX_NAMES, game.html:1634)"
