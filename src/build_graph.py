"""knowledge-ops · Phase 2 — stars 코퍼스 → 지식그래프 + 문제→지식 소환.

입력: data/raw/stars.json (star 1건=1행)
출력(외부화·재현가능):
  - data/interim/graph_nodes.csv  (노드=도구 1개=1행)
  - data/interim/graph_edges.csv  (엣지=도구쌍 1개=1행, topic 공유)
  - outputs/graph_summary.md      (허브·클러스터·고립=공백 + 문제→소환 데모)

설계(CLAUDE.md):
- 표준 라이브러리만(사용자 PC 동일 실행). 계산값은 원천 topics에서만 파생.
- 노이즈/포크는 명시 제외(EDA 결정 반영). canonical 원본으로 라벨 정정.
- 분석단위 분리: 노드(도구)·엣지(topic 공유 관계)·소환(문제 1건) 함수 분리.

실행:
    python src/build_graph.py                 # data/raw/stars.json
    python src/build_graph.py <stars.json>    # 다른 경로
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "raw" / "stars.json"
NODES_OUT = ROOT / "data" / "interim" / "graph_nodes.csv"
EDGES_OUT = ROOT / "data" / "interim" / "graph_edges.csv"
MD_OUT = ROOT / "outputs" / "graph_summary.md"

# EDA 결정 반영: 노이즈/포크 제외, 비-canonical → 원본 라벨 정정
EXCLUDE = {"DietrichGebert/ponytail", "mdancho84/awesome-llm-apps", "marclamberti/airflow-ai-sdk"}
RELABEL = {
    "fivetran/great_expectations": "great-expectations/great_expectations",
    "Data-Centric-AI-Community/fg-data-profiling": "ydataai/ydata-profiling",
    "SQLMesh/sqlmesh": "TobikoData/sqlmesh",
}
DOMAIN = {
    "데이터분석": ["pandas-dev/pandas", "pola-rs/polars", "duckdb/duckdb", "dbt-labs/dbt-core",
              "TobikoData/sqlmesh", "great-expectations/great_expectations", "ydataai/ydata-profiling"],
    "시각화·BI": ["streamlit/streamlit", "plotly/plotly.py", "mwaskom/seaborn", "apache/superset",
               "metabase/metabase", "evidence-dev/evidence"],
    "AI·LLM·RAG": ["huggingface/transformers", "langchain-ai/langchain", "run-llama/llama_index",
                 "vllm-project/vllm", "mem0ai/mem0", "HKUDS/LightRAG", "microsoft/graphrag",
                 "getzep/graphiti", "Tencent/WeKnora"],
    "비즈니스·인과": ["uber/causalml", "recommenders-team/recommenders", "facebook/prophet",
                "statsmodels/statsmodels", "pymc-labs/pymc-marketing", "py-why/EconML"],
}
EDGE_MIN = 2  # 엣지 성립 최소 공유 topic 수(노이즈 억제)


def load_nodes(rows: list) -> dict:
    """stars 행 → 노드 dict{full_name: {...}}. 단위: 코퍼스 1개. 제외/라벨 정정 반영."""
    name2domain = {n: d for d, names in DOMAIN.items() for n in names}
    nodes = {}
    for r in rows:
        fn = r.get("full_name")
        if fn in EXCLUDE:
            continue
        fn = RELABEL.get(fn, fn)
        nodes[fn] = {
            "full_name": fn,
            "domain": name2domain.get(fn, "(미분류)"),
            "language": r.get("language") or "",
            "stars": r.get("stargazers_count") or 0,
            "topics": set(r.get("topics") or []),
        }
    return nodes


def build_edges(nodes: dict) -> list:
    """노드 → 엣지 리스트. 단위: 도구쌍 1개. 공유 topic ≥ EDGE_MIN."""
    edges = []
    for a, b in combinations(sorted(nodes), 2):
        shared = nodes[a]["topics"] & nodes[b]["topics"]
        if len(shared) >= EDGE_MIN:
            edges.append({"source": a, "target": b, "weight": len(shared),
                          "shared_topics": "|".join(sorted(shared))})
    return edges


def degrees(nodes: dict, edges: list) -> dict:
    """엣지 → 노드별 차수(연결 수). 단위: 그래프 1개. 고립=공백 신호."""
    deg = {n: 0 for n in nodes}
    for e in edges:
        deg[e["source"]] += 1
        deg[e["target"]] += 1
    return deg


def summon(nodes: dict, query_topics: set, top: int = 8) -> list:
    """문제(topic 집합) → 소환 도구 랭킹. 단위: 문제 시나리오 1건.
    점수 = 노드 topics ∩ 질의 topics 개수. 적용 순서는 도메인 파이프라인 순."""
    order = {"데이터분석": 0, "시각화·BI": 3, "AI·LLM·RAG": 2, "비즈니스·인과": 1, "(미분류)": 4}
    scored = []
    for n, d in nodes.items():
        hit = d["topics"] & query_topics
        if hit:
            scored.append((len(hit), d["domain"], n, sorted(hit)))
    scored.sort(key=lambda x: (-x[0], order.get(x[1], 9)))
    return scored[:top]


def main() -> None:
    if not SRC.exists() or SRC.stat().st_size <= 2:
        raise SystemExit(f"데이터 없음: {SRC} (먼저 python src/collect_stars.py)")
    rows = json.loads(SRC.read_text(encoding="utf-8"))
    nodes = load_nodes(rows)
    edges = build_edges(nodes)
    deg = degrees(nodes, edges)

    NODES_OUT.parent.mkdir(parents=True, exist_ok=True)
    with NODES_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["full_name", "domain", "language", "stars", "degree", "n_topics"])
        for n, d in sorted(nodes.items(), key=lambda kv: -deg[kv[0]]):
            w.writerow([n, d["domain"], d["language"], d["stars"], deg[n], len(d["topics"])])
    with EDGES_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["source", "target", "weight", "shared_topics"])
        for e in sorted(edges, key=lambda e: -e["weight"]):
            w.writerow([e["source"], e["target"], e["weight"], e["shared_topics"]])

    # 문제→소환 데모 시나리오 (이커머스 포트폴리오 직결)
    scenario = "이커머스 리뷰 감성분석 파이프라인 구축"
    q = {"data-analysis", "data-science", "nlp", "machine-learning", "eda",
         "exploratory-data-analysis", "data-visualization", "statistics", "data-quality"}
    hits = summon(nodes, q)

    isolated = sorted([n for n in nodes if deg[n] == 0])
    hubs = sorted(nodes, key=lambda n: -deg[n])[:5]
    dom_count = Counter(d["domain"] for d in nodes.values())

    L = [f"# 지식그래프 요약 — knowledge-ops Phase 2",
         f"### N(노드)={len(nodes)} · 엣지={len(edges)} (공유 topic≥{EDGE_MIN}) · 출처 {SRC.name}\n",
         "> 노이즈/포크 3건 제외, 비-canonical 3건 원본 라벨 정정(EDA 결정 반영).\n",
         "## 1. 도메인 구성", *[f"- {k}: {v}" for k, v in dom_count.most_common()], "",
         "## 2. 허브 (degree 상위 — 소환 길목)",
         *[f"- {n} (deg {deg[n]}, {nodes[n]['domain']})" for n in hubs], "",
         "## 3. 고립 노드 (degree 0 = 위상적 공백/사일로)",
         f"- {', '.join(isolated) if isolated else '없음'}", "",
         f"## 4. 문제→지식 소환 데모 — \"{scenario}\"",
         f"질의 topic: {', '.join(sorted(q))}\n",
         "| 순위 | 도구 | 도메인 | 매칭 topic |", "|---|---|---|---|"]
    for i, (sc, dom, n, hit) in enumerate(hits, 1):
        L.append(f"| {i} | {n} | {dom} | {', '.join(hit)} ({sc}) |")
    L += ["",
          "**적용 순서(파이프라인)**: 데이터분석(수집·전처리·품질) → 비즈니스·인과(지표·검정) "
          "→ AI·LLM(모델·NLP) → 시각화·BI(전달).",
          "**소환된 공백 메모**: 감성분석 전용 한국어 NLP·실험설계(A/B)·MMM은 코퍼스에 부족 "
          "→ 보강 우선순위(EDA 결정 4번)와 일치."]
    MD_OUT.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ {NODES_OUT.name}, {EDGES_OUT.name}, {MD_OUT.name} 저장")


if __name__ == "__main__":
    main()
