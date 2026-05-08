# Architecture Decision Records

핵심 결정 사항과 그 이유를 기록. 같은 논의를 반복하지 않기 위함.

---

## ADR-001 · Agent 파이프라인 언어: Python + LangGraph

**결정:** Agent 파이프라인은 Python 3.11 + LangGraph로 구현한다.

**이유:** 멘토님이 LangGraph 기반 구현을 명시적으로 요구. LangGraph는 Python 전용 프레임워크이므로 파이프라인 언어는 Python이 된다.

**대안:** TypeScript 기반 LangChain.js → LangGraph가 Python 전용이므로 제외.

**영향:** Next.js는 프론트엔드 + API 게이트웨이 역할만 담당. 실제 분석 로직은 별도 Python FastAPI 서버로 분리.

---

## ADR-002 · 데이터 수집 전략: 온디맨드 (요청 시 수집)

**결정:** 사전에 데이터를 저장하지 않고, 분석 요청이 들어올 때 API를 호출해 수집한다.

**이유:** MVP 범위에서 스케줄러·캐시·DB 스키마 설계까지 추가하는 것은 과도한 복잡도. 요청 → 수집 → 분석 → 반환의 단순한 흐름이 데모 목적에 적합하다.

**대안:** 사전 수집 후 DB 저장 → 별도 파이프라인 필요, MVP 범위 초과.

**영향:** 동일 종목·기간 요청 시 매번 외부 API를 호출. 응답 속도가 느릴 수 있으나 MVP에서는 허용.

---

## ADR-003 · 주가 데이터 소스: yfinance

**결정:** 주가·거래량·벤치마크 데이터는 `yfinance` 라이브러리를 사용한다.

**이유:** 무료, API 키 불필요, OHLCV + 기업 메타(sector, industry) 동시 제공. MVP 범위인 미국 주식을 충분히 커버.

**대안:** Alpha Vantage, Polygon.io → 무료 플랜 rate limit 제약이 더 엄격하거나 유료.

**영향:** yfinance는 비공식 API 기반이므로 Yahoo Finance 정책 변경 시 중단 가능. MVP 한정으로 수용.

---

## ADR-004 · 팀원 코드 미수신 대응: 인터페이스 기반 독립 구현

**결정:** 팀원 구현물(Agent 2, 3)을 받지 못한 상태에서 `docs/interface.md`의 스키마를 기준으로 Agent 1을 독립 구현한다.

**이유:** 코드 공유를 기다리면 일정이 지연됨. Agent 1 출력 스키마(`CollectedData`)를 먼저 확정하면 팀원과 나중에 연동 가능.

**대안:** 팀원 코드 수신 후 구현 시작 → 일정 리스크.

**영향:** 연동 시 `CollectedData` 스키마가 계약 기준. 팀원이 스키마 변경을 요청하면 `interface.md`를 먼저 수정하고 구현에 반영.

---

## 변경 이력

| 날짜 | 내용 | 작성자 |
|------|------|--------|
| 2026-05-08 | 초안 작성 (ADR 001~004) | 김진기 |
