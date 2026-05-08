from __future__ import annotations

import operator
from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


class PriceRecord(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    pct_change: float


class BenchmarkComparison(BaseModel):
    ticker: str
    label: str
    pct_change_period: float


class NewsArticle(BaseModel):
    title: str
    source: str
    published_at: str
    url: str
    summary: Optional[str] = None


class SECFiling(BaseModel):
    form_type: str
    filed_at: str
    description: str
    url: str


class PriceStats(BaseModel):
    period_pct_change: float
    max_single_day_gain: float
    max_single_day_loss: float
    avg_volume: float
    volume_spike_dates: list[str]
    is_abnormal_move: bool


class CollectedData(BaseModel):
    ticker: str
    start_date: date
    end_date: date
    company_name: Optional[str] = None
    sector: Optional[str] = None

    prices: list[PriceRecord] = []
    price_stats: Optional[PriceStats] = None

    benchmarks: list[BenchmarkComparison] = []
    peer_tickers: list[str] = []

    news_articles: list[NewsArticle] = []
    sec_filings: list[SECFiling] = []

    collected_at: str = ""
    data_quality_warnings: list[str] = []


class AgentState(TypedDict):
    ticker: str
    start_date: str
    end_date: str
    collected_data: Optional[CollectedData]
    hypotheses: Optional[list[dict]]
    report: Optional[dict]
    errors: Annotated[list[str], operator.add]
