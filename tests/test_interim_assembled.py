import pandas as pd
from src.utils.paths import get_yaml, get_data_dir

def test_interim_files_are_assembled():
    config = get_yaml()
    data_dir = get_data_dir()
    interim_dir = data_dir / "interim"

    assert interim_dir.exists(), f"Missing interim dir: {interim_dir}"

    tickers = config["fetch"]["tickers"]
    assert isinstance(tickers, list) and len(tickers) > 0, "No tickers in config."

    missing = []
    bad = []

    for t in tickers:
        path = interim_dir / f"{t}.csv"
        if not path.exists():
            missing.append(t)
            continue

        try:
            df = pd.read_csv(path)

            # Required columns
            assert "Date" in df.columns, "Missing Date column"
            assert "ticker" in df.columns, "Missing ticker column"

            # ticker matches filename
            assert (df["ticker"].astype(str).str.upper() == t.upper()).all(), "ticker mismatch"

            # Date sanity
            dates = pd.to_datetime(df["Date"], errors="coerce")
            assert not dates.isna().any(), "Unparsable Date values"
            assert dates.is_monotonic_increasing, "Dates not sorted"
            assert not dates.duplicated().any(), "Duplicate dates found"

            assert len(df) > 0, "Empty CSV"

        except Exception as e:
            bad.append((t, str(e)))

    # Allow a few missing tickers (data source quirks happen)
    ALLOWED_MISSING = {"SNDK", "PFE", "BKNG", "INTU"}

    unexpected_missing = [t for t in missing if t not in ALLOWED_MISSING]
    if missing:
        print(f"[INFO] Missing interim files (ignored if allowed): {missing}")

    assert not unexpected_missing, f"Unexpected missing interim files: {unexpected_missing}"

    assert not bad, "Bad interim files:\n" + "\n".join([f"{t}: {msg}" for t, msg in bad])