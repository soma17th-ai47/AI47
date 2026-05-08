# AI47 — 주가 변동 원인 분석 Agent

사용자가 주식 티커와 분석 기간을 입력하면, 해당 주가가 왜 움직였는지 원인 가설과 신뢰도를 설명해주는 AI Agent 서비스.

**팀:** 47조 (김대연, 김민석, 김진기, 박성준, 황채원)

---

## 구조

```
AI47/
├── agent/
│   ├── agent1/         # 데이터 수집
│   ├── agent2/         # 분석·가설 생성
│   └── agent3/         # 보고서 생성
├── orchestrator/       # 전체 파이프라인 연결
├── api/                # FastAPI 엔드포인트
├── models/             # Pydantic 스키마
└── docs/
    ├── interface.md    # Agent 간 데이터 계약 (필독)
    ├── data-sources.md # 사용 API 정보
    └── decisions.md    # 주요 결정 이유
```

---

## 시작하기

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어서 키 입력:

```env
OPENAI_API_KEY=sk-...       # Agent 2, 3에서 사용
NEWSAPI_KEY=...              # https://newsapi.org 에서 무료 발급
DATABASE_URL=postgresql://...  # Agent 3 DB 저장 시 필요
```

### 3. 서버 실행

```bash
uvicorn api.main:app --reload
```

- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

### 4. Agent 1 단독 테스트

```bash
python3 -m tests.run_agent1 AAPL 2026-04-01 2026-04-30
# python3 -m tests.run_agent1 {티커} {시작일} {종료일}
```

---

## API 사용법

### `POST /analyze`

```json
{
  "ticker": "AAPL",
  "start_date": "2026-04-01",
  "end_date": "2026-04-30"
}
```

```json
{
  "ticker": "AAPL",
  "collected_data": {
    "company_name": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "price_stats": {
      "period_pct_change": 10.35,
      "is_abnormal_move": false,
      ...
    },
    "benchmarks": [...],
    "news_articles": [...],
    "sec_filings": [...]
  },
  "hypotheses": null,
  "report": null,
  "errors": [],
  "disclaimer": "본 분석은 참고용 정보이며..."
}
```

---

## Agent 2, 3 구현 가이드

`docs/interface.md` 참고.

**Agent 2 노드 기본 구조:**

```python
from models.schema import AgentState

def your_node(state: AgentState) -> dict:
    collected = state["collected_data"]   # Agent 1 수집 결과
    # ... LLM 호출 ...
    return {"hypotheses": [...]}

# 에러 추가 시
    return {"errors": ["에러 메시지"]}    # 기존 errors에 append됨
```

**`orchestrator/graph.py`의 placeholder를 구현으로 교체:**

```python
# 현재 (placeholder)
def _agent2_placeholder(state: AgentState) -> dict:
    return {"hypotheses": []}

# 교체 후
from agent.agent2.graph import agent2_graph

def _run_agent2(state: AgentState) -> dict:
    result = agent2_graph.invoke(state)
    return {"hypotheses": result.get("hypotheses")}
```

---

## 데이터 소스 제약

| 소스 | 제약 |
|------|------|
| NewsAPI | 무료 플랜: 최근 30일 이내 기사만, 100 req/day |
| yfinance | 비공식 API, 15~20분 지연 |
| SEC EDGAR | 미국 기업 전용 |

상세 내용: `docs/data-sources.md`, `데이터_수집_한계_정리.md`

---

> 본 서비스는 참고용 정보 제공을 목적으로 하며, 투자 결정의 책임은 사용자에게 있습니다.
