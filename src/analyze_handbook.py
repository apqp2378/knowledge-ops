"""knowledge-ops · Phase 3 — 조직 코퍼스(GitLab Handbook) 구조 진단.

입력: 핸드북 마크다운 루트(예: data/raw/handbook/content/handbook)
출력(외부화·재현가능):
  - data/interim/handbook_pages.csv  (페이지=노드 1개=1행)
  - data/interim/handbook_links.csv  (내부 링크=엣지 1개=1행)
  - outputs/handbook_diagnosis.md    (공백·사일로·중복·최신성 + 결정)

설계(CLAUDE.md):
- 표준 라이브러리만. 구조 지표는 전부 결정적(LLM 아님) → 방어 가능한 진짜 숫자.
- 분석단위: 페이지 1건=1행 / 링크 1건=1행. 개념추출(LLM)은 별도 샘플 단계.
- 지표는 '상대 비교·의사결정 보조'(절대 점수 아님 — KoD 운영지표 원칙).

실행(knowledge-ops 루트에서):
    python src/analyze_handbook.py data/raw/handbook/content/handbook
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/raw/handbook/content/handbook")
PAGES_OUT = ROOT / "data" / "interim" / "handbook_pages.csv"
LINKS_OUT = ROOT / "data" / "interim" / "handbook_links.csv"
MD_OUT = ROOT / "outputs" / "handbook_diagnosis.md"
STUB_WORDS = 100  # 이하 = stub(미완/공백 후보)
LINK_RE = re.compile(r"\]\(([^)\s]+)")
FM_TITLE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.M)
H1 = re.compile(r"^#\s+(.+)$", re.M)


def find_repo(p: Path) -> Path:
    for d in [p.resolve(), *p.resolve().parents]:
        if (d / ".git").exists():
            return d
    return p.resolve()


def url_slug(md_path: Path, content_root: Path) -> str:
    """파일 → Hugo URL 경로(/handbook/.../). 단위: 페이지 1개. 매칭 키."""
    rel = md_path.relative_to(content_root).as_posix()
    rel = re.sub(r"(_index)?\.md$", "", rel).rstrip("/")
    return "/handbook/" + rel if rel else "/handbook"


def strip_md(text: str) -> str:
    text = re.sub(r"^---.*?---", "", text, count=1, flags=re.S)  # frontmatter
    text = re.sub(r"```.*?```", " ", text, flags=re.S)            # code blocks
    text = re.sub(r"[#*_>`\-\|]", " ", text)
    return text


def last_modified(repo: Path, rel_root: str) -> dict:
    """git log 1회 → {파일경로: 최근수정일}. 단위: 코퍼스 1개.
    대용량 partial clone에선 히스토리 순회가 느려 best-effort(타임아웃)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", "--no-renames", "--pretty=format:@%cs",
             "--name-only", "--", rel_root],
            capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return {}
    dates, cur = {}, None
    for line in out.splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line.strip() and cur:
            dates.setdefault(line.strip(), cur)  # 최신(첫 등장)만
    return dates


def main() -> None:
    if not CONTENT.exists():
        raise SystemExit(f"핸드북 경로 없음: {CONTENT}")
    repo = find_repo(CONTENT)
    mds = sorted(CONTENT.rglob("*.md"))
    if not mds:
        raise SystemExit(f"마크다운 없음: {CONTENT}")
    rel_root = CONTENT.resolve().relative_to(repo).as_posix()
    mtimes = last_modified(repo, rel_root) if "--git" in sys.argv else {}  # 기본 OFF(대용량 repo)

    pages, slug2path = {}, {}
    for m in mds:
        raw = m.read_text(encoding="utf-8", errors="ignore")
        slug = url_slug(m, CONTENT)
        title_m = FM_TITLE.search(raw) or H1.search(raw)
        words = strip_md(raw).split()
        links = LINK_RE.findall(raw)
        internal = [l for l in links if l.startswith("/handbook") or (not l.startswith(("http", "#", "mailto")) and "handbook" in l)]
        ext = [l for l in links if l.startswith("http")]
        relkey = m.resolve().relative_to(repo).as_posix()
        pages[slug] = {
            "slug": slug,
            "title": (title_m.group(1).strip() if title_m else m.stem),
            "section": m.relative_to(CONTENT).parts[0],
            "words": len(words),
            "n_internal_links": len(internal),
            "n_external_links": len(ext),
            "last_modified": mtimes.get(relkey, ""),
            "_internal": internal,
        }
        slug2path[slug] = slug

    # 엣지: 내부 링크 → 페이지 매칭(범위 내 해석)
    edges, indeg, outdeg = [], Counter(), Counter()
    for slug, p in pages.items():
        for l in p["_internal"]:
            tgt = "/handbook/" + l.split("/handbook/")[-1].strip("/") if "/handbook" in l else None
            if tgt and tgt in pages and tgt != slug:
                edges.append((slug, tgt))
                outdeg[slug] += 1
                indeg[tgt] += 1

    n = len(pages)
    stubs = [s for s, p in pages.items() if p["words"] < STUB_WORDS]
    isolated = [s for s in pages if indeg[s] == 0 and outdeg[s] == 0]
    orphans = [s for s in pages if indeg[s] == 0]  # 들어오는 링크 없음(소환 안 됨)
    hubs = sorted(pages, key=lambda s: -indeg[s])[:8]
    title_dup = [t for t, c in Counter(p["title"].lower() for p in pages.values()).items() if c > 1]
    dated = [p["last_modified"] for p in pages.values() if p["last_modified"]]
    stale_2026 = [s for s, p in pages.items() if p["last_modified"] and p["last_modified"] < "2025-06-24"]

    PAGES_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PAGES_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["slug", "title", "section", "words", "in_links", "out_links", "n_external", "last_modified"])
        for s, p in sorted(pages.items(), key=lambda kv: -indeg[kv[0]]):
            w.writerow([s, p["title"], p["section"], p["words"], indeg[s], outdeg[s], p["n_external_links"], p["last_modified"]])
    with LINKS_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["source", "target"]); w.writerows(edges)

    def pct(x): return round(100 * x / n, 1) if n else 0
    L = [f"# GitLab Handbook 구조 진단 — People/Hiring",
         f"### 페이지(노드)={n} · 내부링크(엣지)={len(edges)} · 측정 2026-06-24 (구조지표=결정적)\n",
         "## 1. 섹션 구성",
         *[f"- {sec}: {c}" for sec, c in Counter(p['section'] for p in pages.values()).most_common()], "",
         "## 2. 공백 (stub = 내용 빈약, 의사결정에 못 씀)",
         f"- {STUB_WORDS}단어 미만 stub: **{len(stubs)}건 ({pct(len(stubs))}%)**", "",
         "## 3. 사일로 (소환 안 되는 페이지)",
         f"- 완전 고립(in=out=0): **{len(isolated)}건 ({pct(len(isolated))}%)**",
         f"- orphan(들어오는 링크 0 = 검색·소환 경로 없음): **{len(orphans)}건 ({pct(len(orphans))}%)**", "",
         "## 4. 허브 (in-link 상위 = 소환 길목)",
         *[f"- {pages[s]['title']} (in {indeg[s]}) — {s}" for s in hubs], "",
         "## 5. 최신성",
         (f"- 최종수정 1년+ 경과(2025-06-24 이전): **{len(stale_2026)}건 ({pct(len(stale_2026))}%)** · 날짜확보 {len(dated)}/{n}"
          if dated else "- git 최신성 분석 생략(대용량 partial clone; `--git` 옵션으로 활성화)"),
         (f"- 중복 제목 {len(title_dup)}종" if title_dup else "- 중복 제목 없음"), "",
         "## 6. 그래서 무슨 결정 (의사결정 종료)",
         "- **문서화 우선순위**: orphan + stub 교집합 = 소환 안 되는데 내용도 빈약 → 최우선 보강/통합.",
         "- **통합(중복)**: 중복 제목·동일 use-case 페이지 → 병합 후보.",
         "- **폐기/갱신**: 1년+ 미수정 + orphan → 폐기 또는 갱신 검토.",
         "- (다음) 온보딩 시나리오 문제→지식 소환 데모 + LLM 개념추출 샘플 검증으로 보강."]
    MD_OUT.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ {PAGES_OUT.name}, {LINKS_OUT.name}, {MD_OUT.name} 저장")


if __name__ == "__main__":
    main()
