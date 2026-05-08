from __future__ import annotations

from agent.agent1.tools.benchmark import fetch_benchmark_data
from models.schema import AgentState


def collect_benchmark_node(state: AgentState) -> dict:
    """벤치마크·섹터ETF·Peer 비교 노드. 실패해도 파이프라인 계속."""
    collected = state["collected_data"]
    warnings: list[str] = []

    try:
        benchmarks, peer_tickers = fetch_benchmark_data(
            ticker=collected.ticker,
            sector=collected.sector or "",
            start_date=str(collected.start_date),
            end_date=str(collected.end_date),
        )
        collected.benchmarks = benchmarks
        collected.peer_tickers = peer_tickers
    except Exception as e:
        warnings.append(f"벤치마크 수집 실패: {e}")

    if warnings:
        collected.data_quality_warnings.extend(warnings)

    return {"collected_data": collected}
