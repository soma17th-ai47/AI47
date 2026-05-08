from __future__ import annotations

import yfinance as yf

from models.schema import BenchmarkComparison

SECTOR_ETF_MAP: dict[str, str] = {
    "Technology": "XLK",
    "Healthcare": "XLV",
    "Financials": "XLF",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Energy": "XLE",
    "Industrials": "XLI",
    "Materials": "XLB",
    "Real Estate": "XLRE",
    "Utilities": "XLU",
    "Communication Services": "XLC",
}

SECTOR_PEERS_MAP: dict[str, list[str]] = {
    "Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK"],
    "Financials": ["JPM", "BAC", "WFC", "GS", "MS"],
    "Consumer Discretionary": ["AMZN", "TSLA", "HD", "NKE", "MCD"],
    "Consumer Staples": ["PG", "KO", "PEP", "WMT", "COST"],
    "Energy": ["XOM", "CVX", "COP", "EOG", "SLB"],
    "Industrials": ["GE", "HON", "CAT", "UPS", "BA"],
    "Materials": ["LIN", "APD", "SHW", "FCX", "NEM"],
    "Real Estate": ["PLD", "AMT", "EQIX", "SPG", "DLR"],
    "Utilities": ["NEE", "DUK", "SO", "D", "AEP"],
    "Communication Services": ["GOOGL", "META", "NFLX", "DIS", "CMCSA"],
}

MAX_PEERS = 3


def fetch_benchmark_data(
    ticker: str, sector: str, start_date: str, end_date: str
) -> tuple[list[BenchmarkComparison], list[str]]:
    """S&P500, 섹터 ETF, Peer 기업 수익률 비교. (benchmarks, peer_tickers) 반환."""
    targets: list[tuple[str, str]] = [("^GSPC", "S&P 500")]

    etf = SECTOR_ETF_MAP.get(sector)
    if etf:
        targets.append((etf, f"{sector} ETF ({etf})"))

    raw_peers = [t for t in SECTOR_PEERS_MAP.get(sector, []) if t.upper() != ticker.upper()]
    peer_tickers = raw_peers[:MAX_PEERS]
    for p in peer_tickers:
        targets.append((p, p))

    benchmarks: list[BenchmarkComparison] = []
    for sym, label in targets:
        try:
            df = yf.download(sym, start=start_date, end=end_date, progress=False, auto_adjust=True)
            if df.empty:
                continue
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            first = float(df["Close"].iloc[0])
            last = float(df["Close"].iloc[-1])
            pct = round((last - first) / first * 100, 2)
            benchmarks.append(BenchmarkComparison(ticker=sym, label=label, pct_change_period=pct))
        except Exception:
            continue

    return benchmarks, peer_tickers
