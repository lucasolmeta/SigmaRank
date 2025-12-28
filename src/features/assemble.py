
import os
import pandas as pd
from src.utils.paths import get_yaml, get_data_dir

config = get_yaml()
DATA_DIR = get_data_dir()

def main():
    """
    Assembles final feature sets from interim data files.
    Adds ticker identifier and ensures feature consistency.
    """
    # Part 1: Basic Setup - Get tickers and check directory
    tickers = config['fetch']['tickers']
    interim_dir = DATA_DIR / 'interim'

    # FOR NOW only use tickers that actually have interim files
    available = [t for t in tickers if (interim_dir / f'{t}.csv').exists()]
    missing = [t for t in tickers if t not in available]

    if missing:
        print(f"x Ingoring missing interim tickers: {missing}")

    tickers = available
    
    if not interim_dir.exists():
        print(f"✗ Directory {interim_dir} does not exist")
        print("  Run build_features.py first to create feature files")
        return
    
    print(f"Assembling features for {len(tickers)} tickers...")
    print()
    
    # Part 2: First pass - Identify all available features across all tickers
    all_features = set()
    
    for ticker in tickers:
        file_path = interim_dir / f'{ticker}.csv'
        
        if not file_path.exists():
            print(f"⚠ {ticker}.csv not found in interim/, skipping...")
            continue
        
        try:
            df = pd.read_csv(file_path)
            all_features.update(df.columns)
        except Exception as e:
            print(f"✗ Error reading {ticker}.csv: {e}")
            continue
    
    # Get all feature columns (excluding Date which we'll handle separately)
    feature_cols = sorted([col for col in all_features if col != 'Date'])
    
    print(f"Identified {len(feature_cols)} feature columns:")
    print(f"  Features: {', '.join(feature_cols[:10])}{'...' if len(feature_cols) > 10 else ''}")
    print()
    
    # Part 3: Second pass - Process each ticker file and add ticker identifier
    processed_count = 0
    
    for ticker in tickers:
        file_path = interim_dir / f'{ticker}.csv'
        
        if not file_path.exists():
            continue
        
        try:
            # Read the interim data
            df = pd.read_csv(file_path)
            
            # Ensure Date is datetime format
            df['Date'] = pd.to_datetime(df['Date'])
            # De-duplicate on Date (keep the last row)
            df = df.sort_values("Date").drop_duplicates(subset=["Date"], keep="last").reset_index(drop=True)
            
            # Add ticker identifier column (this is a new column!)
            df['ticker'] = ticker
            
            # Get all columns after adding ticker
            all_cols = list(df.columns)
            
            # Define desired column order: Date, ticker, target, then all other features
            core_cols = ['Date', 'ticker']
            
            # Add target_daily_return if it exists (it's our prediction target)
            if 'target_daily_return' in all_cols:
                core_cols.append('target_daily_return')
            
            # Get remaining columns (excluding the ones we've already ordered)
            other_cols = [col for col in all_cols if col not in core_cols]
            other_cols = sorted(other_cols)  # Sort for consistency
            
            # Final column order: core columns first, then sorted remaining columns
            final_cols = core_cols + other_cols
            
            # Reorder dataframe to match desired column order
            df_final = df[final_cols].copy()
            
            # Save back to interim with assembled features
            df_final.to_csv(file_path, index=False)
            
            processed_count += 1
            if processed_count % 10 == 0:
                print(f"  Processed {processed_count}/{len(tickers)} tickers...")
                
        except Exception as e:
            print(f"✗ Error processing {ticker}.csv: {e}")
            continue

if __name__ == '__main__':
    main()
