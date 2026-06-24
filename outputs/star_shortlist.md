# 시드 star 후보 — knowledge-ops 코퍼스 구축용
### 작성 2026-06-24 · 현재 기준 웹검증 완료 · 26개 후보(4도메인)

> **쓰는 법:** 전부 찍지 말 것. **"내 비즈니스 문제에 진짜 쓸 것 같은가?"**로 본인이 골라 별을 찍는다.
> (큐레이션 = AI가 후보 제시 / 선택 = 본인 판단. CLAUDE.md AI투명성·진정성 원칙.)
> 목표 규모 20~30개. 별 찍는 법: repo 페이지 우측 상단 **Star** 클릭. 내 목록은 github.com/apqp2378?tab=stars.

---

## A. 데이터 분석 실무
| repo | 왜 (별 찍을 이유) |
|---|---|
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | DataFrame 표준. 분석가 기본기 |
| [pola-rs/polars](https://github.com/pola-rs/polars) | Rust 기반 고속 DataFrame, 대용량 멀티스레드 (pandas 대안) |
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | 인프로세스 OLAP — 로컬 파일에 서버 없이 SQL |
| [dbt-labs/dbt-core](https://github.com/dbt-labs/dbt-core) | SQL 변환·테스트·문서화의 업계 표준 |
| [TobikoData/sqlmesh](https://github.com/TobikoData/sqlmesh) | dbt 대안. 컬럼 레벨 lineage·CI/CD (신흥) |
| [great-expectations/great_expectations](https://github.com/great-expectations/great_expectations) | 데이터 품질을 테스트로 검증 |
| [ydataai/ydata-profiling](https://github.com/ydataai/ydata-profiling) | 1줄 EDA 자동 프로파일링 — **이 프로젝트 EDA와 직결** |

## B. 시각화·대시보드
| repo | 왜 |
|---|---|
| [streamlit/streamlit](https://github.com/streamlit/streamlit) | Python만으로 데이터앱·대시보드 |
| [plotly/plotly.py](https://github.com/plotly/plotly.py) | 인터랙티브 차트 표준 |
| [mwaskom/seaborn](https://github.com/mwaskom/seaborn) | 통계 시각화(논문급 정적 차트) |
| [apache/superset](https://github.com/apache/superset) | 엔터프라이즈 BI 대시보드 |
| [metabase/metabase](https://github.com/metabase/metabase) | 비기술자용 셀프서비스 BI |
| [evidence-dev/evidence](https://github.com/evidence-dev/evidence) | SQL+Markdown 코드기반 BI — **재현성, 이 프로젝트 철학과 일치** |

## C. AI·LLM (차별점)
| repo | 왜 |
|---|---|
| [huggingface/transformers](https://github.com/huggingface/transformers) | LLM/모델 라이브러리 표준 |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | LLM 오케스트레이션·에이전트 |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 문서 인덱싱·RAG 데이터 프레임워크 |
| [ollama/ollama](https://github.com/ollama/ollama) | 로컬 LLM 구동 |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) | 고속 LLM 추론 서빙 |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 지식그래프 기반 RAG — **이 프로젝트 '지식그래프'와 직결** |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | AI 에이전트 메모리 레이어 |

## D. 이커머스·비즈니스 분석
| repo | 왜 |
|---|---|
| [uber/causalml](https://github.com/uber/causalml) | 업리프트 모델링·인과추론(마케팅 타겟팅) |
| [py-why/EconML](https://github.com/py-why/EconML) | 이중기계학습 기반 처리효과 추정 |
| [pymc-labs/pymc-marketing](https://github.com/pymc-labs/pymc-marketing) | 미디어믹스(MMM)·CLV 마케팅 분석 |
| [recommenders-team/recommenders](https://github.com/recommenders-team/recommenders) | 추천시스템 베스트프랙티스 |
| [facebook/prophet](https://github.com/facebook/prophet) | 수요·매출 시계열 예측 |
| [statsmodels/statsmodels](https://github.com/statsmodels/statsmodels) | A/B테스트·회귀 등 통계 검정 |

---

### 다음 단계
1. 위에서 **본인 문제에 맞는 것 위주로 20~30개 별 찍기** (도메인별 고루 섞으면 나중 공백 진단이 의미 있어짐).
2. `python src/collect_stars.py` 실행 → `data/raw/stars.json` 생성.
3. 제가 `profile_stars.py`로 커버리지 EDA(도메인·언어·topic 분포, 공백·중복, 성숙도) 수행 → "그래서 무슨 결정" 보고.
