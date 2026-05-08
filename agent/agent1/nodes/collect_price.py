from __future__ import annotations

from datetime import datetime, timezone

from agent.agent1.tools.price import fetch_price_data
from models.schema import AgentState, CollectedData


def collect_price_node(state: AgentState) -> dict:
    """주가·거래량 조회 노드. 실패 시 파이프라인 중단."""
    ticker = state["ticker"]
    start_date = state["start_date"]
    end_date = state["end_date"]

    prices, stats, company_name, sector = fetch_price_data(ticker, start_date, end_date)

    collected = CollectedData(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        company_name=company_name,
        sector=sector,
        prices=prices,
        price_stats=stats,
        collected_at=datetime.now(timezone.utc).isoformat(),
    )

    return {"collected_data": collected}
