"""knowledge-ops · Phase 1 프로파일 EDA — data/raw/stars.json → 분포 요약.

목적: "저장만 해두고 안 쓰는" 페인이 데이터로 보이는지 확인한다.
입력 단위: star 1건 = 1행(dict). 그래프/관계는 다루지 않는다(Phase 2).
출력: 콘솔 요약 + outputs/profile_summary.md (측정값만, 해석/결정은 분석 보고에서).

설계(CLAUDE.md):
- 표준 라이브러리만(추가 설치 불필요, 사용자 PC에서도 동일 실행).
- 계산값은 원천(starred_at/pushed_at 등)에서만 파생, 추정·보간 없음.
- 모든 지표는 "측정 기준일(run date)"을 명시해 재현 가능.

실행:
    python src/profile_stars.py
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "stars.json"
OUT = ROOT / "outputs" / "profile_summary.md"
NOW = datetime.now(timezone.utc)
TOP_N = 20


def _parse_dt(s):
    """ISO8601(…Z) → aware datetime. 단위: 타임스탬프 1개. 실패 시 None."""
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def _age_days(s):
    """타임스탬프 → 측정 기준일까지 경과일(int). 단위: 타임스탬프 1개."""
    dt = _parse_dt(s)
    return None if dt is None else (NOW - dt).days


def _pct(part, whole):
    return 0.0 if not whole else round(100 * part / whole, 1)


def _quantiles(vals):
    """정렬 리스트 → (p25, p50, p75). 단위: 숫자 리스트 1개."""
    if not vals:
        return (None, None, None)
    xs = sorted(vals)
    def q(p):
        i = max(0, min(len(xs) - 1, int(round(p * (len(xs) - 1)))))
        return xs[i]
    return (q(0.25), q(0.50), q(0.75))


def _buckets(days):
    """경과일 리스트 → 구간별 건수. 단위: 경과일 리스트 1개."""
    b = {"<30": 0, "30-90": 0, "90-180": 0, "180-365": 0, "365+": 0}
    for d in days:
        if d < 30: b["<30"] += 1
        elif d < 90: b["30-90"] += 1
        elif d < 180: b["90-180"] += 1
        elif d < 365: b["180-365"] += 1
        else: b["365+"] += 1
    return b


def profile(rows: list) -> dict:
    """star 행 리스트 → 프로파일 지표 dict. 단위: 코퍼스 1개(전체 star)."""
    n = len(rows)

    # 언어 분포 (None → "(none)")
    langs = Counter((r.get("language") or "(none)") for r in rows)

    # topic 분포 (리스트 평탄화) + topic 보유 여부
    topics = Counter()
    has_topics = 0
    for r in rows:
        ts = r.get("topics") or []
        if ts:
            has_topics += 1
        topics.update(ts)

    # 결측률 (= "못 찾음" 신호: 메타가 비어 검색·식별이 어려움)
    miss_desc = sum(1 for r in rows if not (r.get("description") or "").strip())
    miss_lang = sum(1 for r in rows if not r.get("language"))
    miss_topic = n - has_topics

    # 방치기간: starred_at 기준 경과일 (= "저장하고 안 봄"의 직접 신호)
    star_age = [d for d in (_age_days(r.get("starred_at")) for r in rows) if d is not None]
    star_age_missing = n - len(star_age)
    sa_q = _quantiles(star_age)
    sa_buckets = _buckets(star_age)
    neglected_180 = sum(1 for d in star_age if d >= 180)
    neglected_365 = sum(1 for d in star_age if d >= 365)

    # 노후/죽은 저장: pushed_at 기준 경과일 + archived
    push_age = [d for d in (_age_days(r.get("pushed_at")) for r in rows) if d is not None]
    pa_q = _quantiles(push_age)
    stale_365 = sum(1 for d in push_age if d >= 365)
    stale_730 = sum(1 for d in push_age if d >= 730)
    archived = sum(1 for r in rows if r.get("archived"))

    return {
        "n": n,
        "run_date": NOW.strftime("%Y-%m-%d"),
        "langs": langs,
        "topics": topics,
        "has_topics": has_topics,
        "miss": {"description": miss_desc, "language": miss_lang, "topics": miss_topic},
        "star_age": {"q": sa_q, "buckets": sa_buckets, "missing": star_age_missing,
                     "neglected_180": neglected_180, "neglected_365": neglected_365},
        "push_age": {"q": pa_q, "stale_365": stale_365, "stale_730": stale_730},
        "archived": archived,
    }


def render_md(p: dict) -> str:
    n = p["n"]
    L = []
    L.append(f"# stars 프로파일 요약 (측정 기준일 {p['run_date']})\n")
    L.append(f"- 총 star: **{n}건** · 측정값만 기재(해석·결정은 분석 보고).\n")

    L.append("## 방치기간 (starred_at 기준 경과일)")
    sa = p["star_age"]
    if sa["q"][1] is not None:
        L.append(f"- 경과일 p25/중앙/p75: **{sa['q'][0]} / {sa['q'][1]} / {sa['q'][2]}일**")
    L.append(f"- 180일+ 방치: **{sa['neglected_180']}건 ({_pct(sa['neglected_180'], n)}%)** · "
             f"365일+ 방치: **{sa['neglected_365']}건 ({_pct(sa['neglected_365'], n)}%)**")
    L.append(f"- 구간 분포: {sa['buckets']}")
    if sa["missing"]:
        L.append(f"- starred_at 결측: {sa['missing']}건")
    L.append("")

    L.append("## 결측률 (메타 공백 = '못 찾음' 신호)")
    m = p["miss"]
    L.append(f"- description 없음: **{m['description']}건 ({_pct(m['description'], n)}%)**")
    L.append(f"- topics 없음: **{m['topics']}건 ({_pct(m['topics'], n)}%)**")
    L.append(f"- language 없음: **{m['language']}건 ({_pct(m['language'], n)}%)**")
    L.append("")

    L.append("## 노후/죽은 저장 (pushed_at 기준 + archived)")
    pa = p["push_age"]
    if pa["q"][1] is not None:
        L.append(f"- 마지막 push 경과일 p25/중앙/p75: **{pa['q'][0]} / {pa['q'][1]} / {pa['q'][2]}일**")
    L.append(f"- 1년+ 정체: **{pa['stale_365']}건 ({_pct(pa['stale_365'], n)}%)** · "
             f"2년+ 정체: **{pa['stale_730']}건 ({_pct(pa['stale_730'], n)}%)**")
    L.append(f"- archived 저장소: **{p['archived']}건 ({_pct(p['archived'], n)}%)**")
    L.append("")

    L.append(f"## 언어 분포 (상위 {TOP_N})")
    for lang, c in p["langs"].most_common(TOP_N):
        L.append(f"- {lang}: {c} ({_pct(c, n)}%)")
    L.append("")

    L.append(f"## topic 분포 (상위 {TOP_N}) · topic 보유 {p['has_topics']}/{n}건")
    for t, c in p["topics"].most_common(TOP_N):
        L.append(f"- {t}: {c}")
    L.append("")
    return "\n".join(L)


def main() -> None:
    if not SRC.exists() or SRC.stat().st_size <= 2:
        raise SystemExit(f"수집 데이터 없음: {SRC} (먼저 python src/collect_stars.py 실행)")
    rows = json.loads(SRC.read_text(encoding="utf-8"))
    p = profile(rows)
    md = render_md(p)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md, encoding="utf-8")
    print(md)
    print(f"\n→ 저장: {OUT}")


if __name__ == "__main__":
    main()
