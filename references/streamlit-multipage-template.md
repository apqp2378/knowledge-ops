# Streamlit 멀티페이지 앱 — 재사용 템플릿 레퍼런스
### 출처: SeolMuah/streamlit-multipage-app(+app2) 구조 파악 · 정리 2026-06-24

> **성격:** knowledge-ops 코퍼스(성숙한 외부 도구) 대상 아님 → star 안 함. 본인 대시보드 포트폴리오용 **개인 재사용 템플릿**으로 캡처.
> 아래 app.py 골격은 문서화된 구조 + 표준 Streamlit API로 **재구성**한 것(원본 코드 그대로 아님). 최신 패턴만 검증해 담음.

## 1. 파일 구조
```
streamlit-multipage-app/
├── app.py                     # 진입점 (st.navigation)
├── requirements.txt
├── .streamlit/
│   ├── secrets.toml           # 실제 API 키 (gitignore!)
│   └── secrets.example.toml   # 키 템플릿(공유용)
├── data/
│   └── california_housing.csv
├── model/
│   └── iris_model.joblib      # 사전학습 모델
└── pages/
    ├── data_analysis.py       # @st.fragment
    ├── visualization.py       # @st.fragment
    ├── ml_prediction.py       # RandomForest 붓꽃 예측
    └── gemini_chatbot.py      # Gemini + YouTube 도구
```

## 2. 핵심 패턴 (이게 배울 점)

**`st.navigation` + `st.Page` (신 멀티페이지 API).** 예전 `pages/` 자동탐색 방식과 달리 페이지를 **그룹·제목·아이콘으로 명시 제어**한다. app.py 한 곳에서 라우팅을 정의:

```python
# app.py
import streamlit as st

pages = {
    "데이터": [
        st.Page("pages/data_analysis.py", title="데이터 분석", icon="📊"),
        st.Page("pages/visualization.py", title="시각화", icon="📈"),
    ],
    "AI": [
        st.Page("pages/ml_prediction.py", title="ML 예측", icon="🌸"),
        st.Page("pages/gemini_chatbot.py", title="Gemini 챗봇", icon="💬"),
    ],
}
st.navigation(pages).run()
```

**`@st.fragment` (부분 리렌더).** 위젯 하나 바꿀 때 페이지 전체가 아니라 해당 조각만 다시 실행 → 무거운 분석·차트에서 체감 성능↑:

```python
@st.fragment
def filter_panel(df):
    rng = st.slider("가격대", 0.0, 5.0, (0.0, 5.0))
    st.dataframe(df[df.price.between(*rng)])   # 슬라이더만 움직여도 이 조각만 갱신
```

**`secrets.toml` 키 관리.** 코드에 키 하드코딩 금지. `.streamlit/secrets.toml`에 두고 `st.secrets["GEMINI_API_KEY"]`로 접근. 저장소엔 `secrets.example.toml`(빈 템플릿)만 커밋, 실제 파일은 `.gitignore`.

```toml
# .streamlit/secrets.example.toml
GEMINI_API_KEY = ""
GEMINI_MODEL   = ""
YOUTUBE_API_KEY = ""
```

## 3. 실행 & 배포
```bash
pip install -r requirements.txt
cp .streamlit/secrets.example.toml .streamlit/secrets.toml   # 키 입력
streamlit run app.py
```
배포: repo를 GitHub에 push → share.streamlit.io에서 앱 생성 → **Settings > Secrets**에 키 입력(파일 대신 클라우드가 주입).

## 4. 응용 메모 (knowledge-ops/포트폴리오)
- 데이터분석·시각화·ML·LLM챗봇을 **한 앱의 페이지 그룹**으로 묶는 구성 = 분석가 포트폴리오 데모에 적합.
- 이 패턴 위에 본인 도메인(이커머스 리뷰 감성분석 등)을 얹으면 됨.
- 키 관리(secrets) + example 템플릿 분리 = "민감정보 평문 보관 금지"(CLAUDE.md 권한 원칙)와도 일치.
