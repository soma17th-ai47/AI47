from __future__ import annotations

from datetime import datetime

import pandas as pd
import yfinance as yf

from models.schema import PriceRecord, PriceStats

VOLUME_SPIKE_MULTIPLIER = 2.0
ABNORMAL_MOVE_THRESHOLD = 5.0  # %


def fetch_price_data(
    ticker: str, start_date: str, end_date: str
) -> tuple[list[PriceRecord], PriceStats, str, str]:
    """주가·거래량 조회. (prices, stats, company_name, sector) 반환."""
    info = yf.Ticker(ticker).info
    company_name: str = info.get("longName") or info.get("shortName") or ticker
    sector: str = info.get("sector") or ""

    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"주가 데이터 없음: {ticker} ({start_date} ~ {end_date})")

    df = df.copy()
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df["pct_change"] = df["Close"].pct_change() * 100
    df = df.dropna(subset=["Close"])

    avg_vol = float(df["Volume"].mean())
    spike_dates = [
        d.strftime("%Y-%m-%d")
        for d, v in zip(df.index, df["Volume"])
        if v >= avg_vol * VOLUME_SPIKE_MULTIPLIER
    ]

    records: list[PriceRecord] = []
    for idx, row in df.iterrows():
        records.append(
            PriceRecord(
                date=idx.date(),
                open=round(float(row["Open"]), 4),
                high=round(float(row["High"]), 4),
                low=round(float(row["Low"]), 4),
                close=round(float(row["Close"]), 4),
                volume=int(row["Volume"]),
                pct_change=round(float(row["pct_change"]) if not pd.isna(row["pct_change"]) else 0.0, 4),
            )
        )

    first_close = float(df["Close"].iloc[0])
    last_close = float(df["Close"].iloc[-1])
    period_pct = round((last_close - first_close) / first_close * 100, 2)

    daily_changes = df["pct_change"].dropna()
    stats = PriceStats(
        period_pct_change=period_pct,
        max_single_day_gain=round(float(daily_changes.max()), 2),
        max_single_day_loss=round(float(daily_changes.min()), 2),
        avg_volume=round(avg_vol, 0),
        volume_spike_dates=spike_dates,
        is_abnormal_move=bool(
            daily_changes.abs().max() >= ABNORMAL_MOVE_THRESHOLD
        ),
    )

    return records, stats, company_name, sector


