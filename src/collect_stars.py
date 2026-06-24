"""knowledge-ops · Phase 1 수집 — GitHub starred repos → data/raw/stars.json.

입력 단위: GitHub 사용자 1명의 star 1건 = 1행
출력: data/raw/stars.json (star 1건 = dict 1개)

설계:
- 표준 라이브러리만 사용(urllib). 추가 설치 불필요.
- 토큰은 선택: 환경변수 GITHUB_TOKEN 설정 시 rate limit↑ + private star 포함.
- starred_at 포함(application/vnd.github.star+json) → "별 찍고 방치한 기간" 분석용.
- 수집 단계는 원천을 그대로 담는다(계산값 금지).

실행:
    python src/collect_stars.py            # 기본 계정 apqp2378 공개 stars
    python src/collect_stars.py <username> # 다른 계정
    # 전체(비공개 포함)·rate limit 여유: GITHUB_TOKEN 환경변수 설정 후 실행
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

USER = sys.argv[1] if len(sys.argv) > 1 else "apqp2378"
OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "stars.json"
KEEP = [
    "full_name", "html_url", "description", "language", "topics",
    "stargazers_count", "forks_count", "open_issues_count",
    "pushed_at", "updated_at", "created_at", "archived",
]


def _req(url: str):
    """단일 페이지 GET. 단위: API 응답 1페이지."""
    headers = {
        "Accept": "application/vnd.github.star+json",
        "User-Agent": "knowledge-ops-collector",
    }
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def collect(user: str) -> list:
    """사용자 → star 행 리스트. 단위: 사용자 1명. 페이지네이션 끝까지."""
    rows, page = [], 1
    while True:
        url = f"https://api.github.com/users/{user}/starred?per_page=100&page={page}"
        batch = _req(url)
        if not batch:
            break
        for item in batch:
            repo = item.get("repo", item)  # star+json은 {starred_at, repo:{...}}
            row = {k: repo.get(k) for k in KEEP}
            row["starred_at"] = item.get("starred_at")
            rows.append(row)
        page += 1
    return rows


def main() -> None:
    rows = collect(USER)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"수집 {len(rows)}건 → {OUT}")


if __name__ == "__main__":
    main()
