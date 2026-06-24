# GitLab Handbook 구조 진단 — People/Hiring
### 페이지(노드)=82 · 내부링크(엣지)=202 · 측정 2026-06-24
> 구조지표는 전부 **결정적(재현가능)** · 출처 `data/interim/handbook_pages.csv`·`handbook_links.csv`.
> LLM/판단 분리: 아래 ⓥ 표시는 실제 페이지를 열어 **휴먼검증한 사례**(AI투명성).

## 핵심 발견 — "있지만 안 꺼내지는 지식"
- **orphan(들어오는 링크 0) 21건(25.6%)** · 완전 고립(in=out=0) 8건(9.8%) · stub(<100단어) 2건.
- 즉 People/Hiring 지식의 **1/4이 핸드북 내 링크로 소환되지 않는다** — 검색·내비게이션·온보딩 순간에 안 떠오름. 이 프로젝트 가설(저장된 지식이 결정 순간 소환 안 됨)이 **실제 조직 문서에서 데이터로 확인**됨.

## orphan인데 고가치 = "묻힌 자산" (콘텐츠는 충분, 연결이 끊김)
| 페이지 | 단어수 | in | 메모 |
|---|---|---|---|
| Candidate Experience Specialist Responsibilities | **20,058** | 0 | 채용 운영 전체를 담은 최대 문서가 무링크 |
| Anti-Harassment Policy | 5,674 | 0 | 정책인데 orphan → 컴플라이언스상 반드시 소환돼야 |
| Mentoring at GitLab | 2,727 | 0 | 온보딩/성장 핵심 |
| TaNewKi Tips (신입 가이드) | 2,554 | 0 | ⓥ 실제로 장비·문서·첫날·Okta 가이드 충실. **신입이 못 찾음** |
| Internal Hiring Process | 2,648 | 0 | 내부이동 프로세스 무링크 |
| Transitioning to a manager role | 1,135 | 0 | 신임 매니저 지식 단절 |

## 진입점 파손 (구조 안티패턴)
- **Time Off and Absence**(섹션 인덱스, 177단어, in=out=0 고립) ⓥ — 자식(Time-Off Types in=8 허브, Leave Types)을 **링크가 아닌 산문으로만** 언급 → 그래프·검색이 연결 못함. 콘텐츠는 있는데 진입로가 끊김.

## 허브 (소환 길목 — in-link 상위)
Hiring 핸드북(in 49), People Group(14), Time Off Types(8), Growth&Development(7), Guidance on Feedback(6), Career Development(6). → 소수 허브에 링크가 몰리고 나머지는 변두리.

## 온보딩 시나리오 — 문제→지식 소환 데모
"신입이 입사 첫 주 지식을 핸드북에서 소환"할 때, 핵심 페이지의 소환 가능성(인바운드 링크):

| 필요 지식 | 페이지 | 소환? |
|---|---|---|
| 신입 시작 가이드 | TaNewKi Tips | ❌ orphan(in 0) |
| 멘토링 | Mentoring | ❌ orphan |
| 매니저 전환 | Manager role | ❌ orphan |
| 휴가 진입점 | Time Off and Absence | ❌ 고립(in=out=0) |
| 온보딩 허브 | GitLab Onboarding | △ 약함(in 2) |

→ **온보딩 핵심 지식의 절반이 링크로 소환되지 않는다.** 문제는 "문서가 없다"가 아니라 **"연결이 없다"**.

## 그래서 무슨 결정 (의사결정 종료 · Q5)
1. **연결 보강 = 최우선·최저비용**: 위 묻힌 자산(TaNewKi·Mentoring·Internal Hiring·Coordinator·Anti-Harassment)을 허브(GitLab Onboarding·Hiring·People Group)에서 **인바운드 링크 추가**. 콘텐츠는 이미 충분 → 새로 쓰는 게 아니라 **이어주면** 즉시 소환됨. (가장 적은 노력으로 가장 큰 소환성 개선)
2. **진입점 수리**: Time Off and Absence 인덱스의 산문 참조를 실제 링크로 → 고립 해소.
3. **보강/통합(stub)**: Learning Initiatives(76단어·고립), People Business Partners(33단어) → 내용 보강 또는 상위로 통합.
4. **컴플라이언스 시급**: Anti-Harassment·Acceptable Use Policy가 orphan → 정책은 반드시 소환돼야 하므로 연결 1순위로 승격.

**검증(AI투명성):** orphan/고립은 링크 그래프에서 결정적으로 산출. 샘플 2건(TaNewKi Tips·Time Off 인덱스)을 실제로 열어 ⓥ 확인 — 전자는 풍부하지만 인바운드 0, 후자는 자식을 링크 아닌 산문으로 참조해 고립. 입증된 사례 위에서만 결론을 냈다.
