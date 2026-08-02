# 에셋 출처 및 라이선스 (스팀 상업 출시용)

> ⚠️ 스팀 출시 시 **모든 에셋이 상업 사용 가능**해야 합니다.
> 새 에셋을 추가할 때마다 이 파일에 출처·라이선스를 기록하세요.
> AI 생성물·폰트·음원·이미지 전부 포함.

## 1. 스킬 이펙트 (fx_*.png)
- **출처**: "Free Pixel Effects Pack" — CodeManu (David Silva) / DavitMasia
- **제작 툴**: Pixel FX Designer
- **라이선스**: **Public Domain** — 개인·상업 사용 모두 가능, 크레딧 불필요
  - README 원문: "This is a public domain asset, you can use it for both personal and commercial purposes. No credit required."
- **상태**: ✅ 상업 사용 OK
- **크레딧(선택)**: @DavitMasia, @CodeManuPro (Twitter) — 필수 아님, 예의상 표기 권장

## 2. 플레이어 캐릭터 (player_*.png)
- **출처**: 나노바나나(Google Gemini) AI 이미지 생성 → 배경 제거
- **라이선스**: ⚠️ **확인 필요** — Google Gemini 생성 이미지의 상업적 사용 약관 재확인
  - 일반적으로 Google은 Gemini 생성 콘텐츠의 상업 사용을 허용하나, 출시 전 최신 약관 확인 필수
  - 참고: AI 생성 이미지는 일부 국가에서 저작권 보호를 못 받을 수 있음(에셋을 남이 그대로 써도 막기 어려움) — 판매 자체엔 보통 문제없음
- **상태**: 🔶 출시 전 약관 재확인

## 3. 보스 일러스트 9종 (boss_*.png)
- **출처**: 나노바나나(Google Gemini) AI 생성 → 배경 제거 → 투명 여백 크롭
- **파일**: boss_ignis / boss_frost / boss_aquarion / boss_acid / boss_ferrum / boss_golem / boss_phantom / boss_lime / boss_dragon
- **라이선스**: ⚠️ 플레이어와 동일 (Gemini 상업 약관 출시 전 재확인)
- **상태**: ✅ 제작 완료, 🔶 약관 재확인 대상

## 3-2. 잡몹/배경 (미제작)
- **예정**: 나노바나나 생성 → 동일 라이선스 검토
- **상태**: ⬜ 미제작

## 4. 효과음 (SFX)
- **출처**: 코드 생성(Web Audio API 합성음) — 파일 없음
- **라이선스**: ✅ 자체 생성물, 문제 없음

## 4-2. 배경음악 (BGM, assets/bgm_*.mp3)
- **현재**: 미제작 (파일 없으면 무음 폴백)
- **예정 파일**: bgm_map / bgm_battle / bgm_boss / bgm_victory / bgm_defeat
- **⚠ 필수**: CC0 또는 상업 로열티프리만 사용. 받은 곡마다 아래에 기록:
  - _(예시)_ bgm_boss.mp3 — 출처: OpenGameArt "Epic Boss Battle" by ○○○, 라이선스: CC0 ✅
  - _(여기에 추가)_
- **상태**: ⬜ 미제작

## 5. 폰트
- **현재**: DungGeunMo(둥근모), Galmuri11 지정 → 없으면 시스템 monospace 폴백
- **라이선스 상태**:
  - Galmuri (하리보): SIL Open Font License — ✅ 상업 사용 가능
  - DungGeunMo(둥근모꼴): 개인·상업 무료(우아한형제들 계열 아님, 원저작자 확인 권장)
- **주의**: 스팀 배포판(Electron/Tauri)에는 폰트를 **직접 임베드**해야 함(사용자 PC에 없을 수 있음) → 임베드 시 라이선스가 재배포를 허용하는지 확인
- **상태**: 🔶 임베드 시 재확인

## 6. 게임 이름 / 브랜딩
- **가칭**: 케미컬 퀘스트 / Subrain Alchemist
- **주의**: 최종 타이틀 확정 시 **스팀·상표 검색**으로 기존 게임명 충돌 확인
- **상태**: ⬜ 미확정

---
_최종 수정: 2026-07-17_
