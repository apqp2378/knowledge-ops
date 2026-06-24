# 지식그래프 요약 — knowledge-ops Phase 2
### N(노드)=28 · 엣지=80 (공유 topic≥2) · 출처 stars.json

> 노이즈/포크 3건 제외, 비-canonical 3건 원본 라벨 정정(EDA 결정 반영).

## 1. 도메인 구성
- AI·LLM·RAG: 9
- 데이터분석: 7
- 비즈니스·인과: 6
- 시각화·BI: 6

## 2. 허브 (degree 상위 — 소환 길목)
- ydataai/ydata-profiling (deg 11, 데이터분석)
- recommenders-team/recommenders (deg 11, 비즈니스·인과)
- apache/superset (deg 11, 시각화·BI)
- streamlit/streamlit (deg 10, 시각화·BI)
- langchain-ai/langchain (deg 9, AI·LLM·RAG)

## 3. 고립 노드 (degree 0 = 위상적 공백/사일로)
- pola-rs/polars

## 4. 문제→지식 소환 데모 — "이커머스 리뷰 감성분석 파이프라인 구축"
질의 topic: data-analysis, data-quality, data-science, data-visualization, eda, exploratory-data-analysis, machine-learning, nlp, statistics

| 순위 | 도구 | 도메인 | 매칭 topic |
|---|---|---|---|
| 1 | ydataai/ydata-profiling | 데이터분석 | data-analysis, data-quality, data-science, eda, exploratory-data-analysis, machine-learning, statistics (7) |
| 2 | great-expectations/great_expectations | 데이터분석 | data-quality, data-science, eda, exploratory-data-analysis (4) |
| 3 | streamlit/streamlit | 시각화·BI | data-analysis, data-science, data-visualization, machine-learning (4) |
| 4 | statsmodels/statsmodels | 비즈니스·인과 | data-analysis, data-science, statistics (3) |
| 5 | evidence-dev/evidence | 시각화·BI | data-science, data-visualization, exploratory-data-analysis (3) |
| 6 | apache/superset | 시각화·BI | data-analysis, data-science, data-visualization (3) |
| 7 | pandas-dev/pandas | 데이터분석 | data-analysis, data-science (2) |
| 8 | recommenders-team/recommenders | 비즈니스·인과 | data-science, machine-learning (2) |

**적용 순서(파이프라인)**: 데이터분석(수집·전처리·품질) → 비즈니스·인과(지표·검정) → AI·LLM(모델·NLP) → 시각화·BI(전달).
**소환된 공백 메모**: 감성분석 전용 한국어 NLP·실험설계(A/B)·MMM은 코퍼스에 부족 → 보강 우선순위(EDA 결정 4번)와 일치.