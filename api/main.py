from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

from orchestrator.graph import pipeline  # noqa: E402

app = FastAPI(title="AI47 주가 변동 분석 API")

DISCLAIMER = "본 분석은 참고용 정보이며, 투자 결정의 책임은 사용자에게 있습니다."


class AnalysisRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str


class AnalysisResponse(BaseModel):
    ticker: str
    collected_data: dict | None
    hypotheses: list[dict] | None
    report: dict | None
    errors: list[str]
    disclaimer: str


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(req: AnalysisRequest):
    initial_state = {
        "ticker": req.ticker.upper(),
        "start_date": req.start_date,
        "end_date": req.end_date,
        "collected_data": None,
        "hypotheses": None,
        "report": None,
        "errors": [],
    }

    try:
        result = pipeline.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    collected = result.get("collected_data")
    return AnalysisResponse(
        ticker=req.ticker.upper(),
        collected_data=collected.model_dump() if collected else None,
        hypotheses=result.get("hypotheses"),
        report=result.get("report"),
        errors=result.get("errors", []),
        disclaimer=DISCLAIMER,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
