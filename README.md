<p align="center">
  <img src="https://github.com/user-attachments/assets/9856e2be-279a-4340-b34e-27f61da4450f" alt="whiteLogo" width="200"/>
</p>

# 📈 MrktMove

**MrktMove** is a real-time machine learning system that predicts how much a stock will change during the next trading day using regression. It can be run at any time, by anyone to predict returns in real time. 

---

# ⚠️ Disclaimer

**Use at your own risk. Returns are never guaranteed and investing involves risk! Buy recommendations come with no assurance and you assume all risk as your own.**

---

## 🧠 Project Summary

- **Goal:** Predict the **magnitude of next-day stock returns** and use it to make **curated stock recommendations**
- **Model Type:** Regression (Gradient Boost)

---

## 🧱 Project Structure

```
MrktMove/
│
├── main.py                          # Runs entire daily pipeline (fetch → preprocess → predict → evaluate → log results)
├── config.py                        # Store ticker list
│
├── data/
│   ├── fetch.py                     # Pulls historical OHLCV data from yfinance
│   ├── preprocess.py                # Builds features + return targets
│   ├── by_stock/                    # Stores per-ticker training data
│       ├── TICKER.csv               # Features and returns for a given ticker
│
├── model/
│   ├── model.py                     # Regression model training/prediction
│   ├── evaluate.py                  # Result evaluations
│   ├── visualize.py                 # Plots predicted returns
│
├── predictions/
│   ├── YYYY-MM-DD-predictions.csv   # Daily prediction file
│
├── results/
│   ├── YYYY-MM-DD-results.csv       # Daily results file
│   ├── daily-results.csv            # Result logs by day
│
├── README.md                        # This file
```

---

## ⚙️ How It Works

1. Run `main.py` daily before market opens.
2. Fetch the latest data up to yesterday’s close.
3. Predict next-day return for each stock.
4. Store predictions and results in dedicated '-.csv' files.

---

## 🧠 Model Details

- **Model type:** Regression
- **Output:** Predicted next-day % return
- **Modeling tool:** `XGBRegressor`

---

## 📦 Dependencies

- Python 3.8+
- `pandas`
- `yfinance`
- `ta` (technical indicators)
- `xgboost`
- `sci-kit learn`
- `numpy`
- `joblib`

Install everything:
```bash

pip install -r requirements.txt





