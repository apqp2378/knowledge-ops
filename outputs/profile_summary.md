# stars 코퍼스 프로파일 EDA — knowledge-ops Phase 1
### 측정 기준일 2026-06-24 · N=29 · 출처 `data/raw/stars.json` (GitHub API, 재현가능)

> 분석단위: star 1건 = 1행. 도메인 라벨은 분석가가 부여 후 **29건 전수 눈검증**(LLM 일괄분류 아님 — CLAUDE.md AI투명성).

## 1. 도메인 커버리지 (편중·공백)
| 도메인 | 건수 | 비중 |
|---|---|---|
| AI·LLM·RAG | 9 | **31.0%** |
| 데이터분석 실무 | 7 | 24.1% |
| 시각화·대시보드 | 6 | 20.7% |
| 이커머스·비즈니스·인과 | 4 | **13.8%** |
| 노이즈/재검토 | 3 | 10.3% |

**편중**: AI·LLM 쪽이 가장 두텁고(노이즈 3건도 전부 AI계열 → 실질 41%), **이커머스·비즈니스·인과가 가장 얕음(14%)**. 추천했던 pymc-marketing·EconML 등 인과/마케팅 도구가 빠져 공백.

## 2. 지식그래프/RAG 클러스터 (프로젝트 주제 정합)
topics에 `rag/graph` 계열 보유 **7건**: getzep/graphiti, Tencent/WeKnora, microsoft/graphrag, mem0ai/mem0, HKUDS/LightRAG, run-llama/llama_index, langchain-ai/langchain. → 코퍼스에서 가장 밀집한 하위 클러스터가 이 프로젝트(지식그래프)의 주제와 정확히 일치.

## 3. 언어 분포
Python 20(69%), JavaScript 2, Rust 2(polars·미해당), Go 1(WeKnora), Clojure 1(metabase), TypeScript 1(superset), C++ 1(duckdb), (none) 1. → Python 중심에 고성능/BI 도구가 다언어로 섞임.

## 4. topic 허브 (상위 12)
llm(9), rag(7), python(5), analytics(5), data-visualization(5), agents(4), data-analysis(4), data-science(4), machine-learning(4), business-intelligence(4), ai(3), ai-agents(3). → `llm`·`rag`가 최상위 허브 = 편중 재확인.

## 5. 성숙도·신선도·결측
- 별 분포: <1k 2건 · 1k–10k 3건 · 10k–50k 17건 · 50k+ 7건 (중앙값 27,779). → **대부분 매우 성숙**.
- 마지막 push 90일+ 정체: 4건 (awesome-llm-apps, airflow-ai-sdk, evidence, seaborn). archived: **0건**.
- 결측: language 1건(awesome-llm-apps), topics 2건(awesome-llm-apps, airflow-ai-sdk).
- `starred_at` 전부 2026-06-24(동일자) → **방치기간 지표는 의미 없음**(신규 코퍼스. D-010에서 예고한 대로 페인 초점이 '방치'에서 '커버리지'로 이동).

## 6. 중복·노이즈 (폐기/교체 후보)
- **노벨티**: `DietrichGebert/ponytail` — 풍자 repo(yagni·claude-code-plugin), 분석 코퍼스와 무관.
- **포크(원본 아님)**: `mdancho84/awesome-llm-apps`(7별·결측, 도구 아닌 '리스트'), `marclamberti/airflow-ai-sdk`(1별·결측).
- **비-canonical**: `fivetran/great_expectations`, `Data-Centric-AI-Community/fg-data-profiling`.
- → 이 5건이 결측·저신뢰·정체의 대부분을 차지. 나머지 24건은 깨끗·성숙.

---

## 그래서 무슨 결정 (의사결정 종료)
> 본질은 "방치 페인 입증"이 아니라 **쌓인 지식을 그래프로 구조화 → 문제 순간 소환·적용 + 공백/중복 진단 → 정리·보강 결정**이다.

1. **진단(Q1·Q4)**: 코퍼스가 AI·LLM·RAG에 편중(31%, 노이즈 포함 실질 41%), **이커머스·비즈니스·인과는 공백(14%)**. rag/graph 클러스터(7건)가 최밀집 = 그래프 분석의 핵심 축.
2. **폐기(Q5)**: `ponytail` 제거(완료) → 코퍼스 28건.
3. **교체**: fork 2개(awesome-llm-apps, airflow-ai-sdk) → 원본 또는 제거 / `great_expectations`·`ydata-profiling`을 canonical 원본으로.
4. **보강 1순위(공백)**: 이커머스·비즈니스·인과 — `pymc-labs/pymc-marketing`, `py-why/EconML`, 실험설계(A/B). 이커머스 포트폴리오 직결로 ROI 최고.
5. **핵심 차별 산출물(Q2) = 문제→지식 소환 매핑**: Phase 2에서 노드(도구)–엣지(topic·use-case 공유) 그래프 구축 후, 시나리오(예 "이커머스 리뷰 감성분석 파이프라인 구축")를 넣으면 그래프가 소환하는 도구·적용 순서를 출력.
