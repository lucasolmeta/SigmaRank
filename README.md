<p align="center">
  <img src="https://github.com/user-attachments/assets/9856e2be-279a-4340-b34e-27f61da4450f" alt="whiteLogo" width="200"/>
</p>

# 📈 MrktMove

**MrktMove** is a real-time machine learning system that predicts how much a stock will change tomorrow using regression models. It can be run at any time, by anyone at real time to predict returns in real time.

---

## 🧠 Project Summary

- **Goal:** Predict the **magnitude of next-day stock returns**
- **Model Type:** Regression (Gradient Boost)

---

## 🧱 Project Structure

```
MrktMove/
│
├── main.py                # Runs entire daily pipeline (fetch → preprocess → predict)
├── config.py              # Store ticker list
│
├── data/
│   ├── fetch.py           # Pulls historical OHLCV data from yfinance
│   ├── preprocess.py      # Builds features + return targets
│   ├── by_stock/          # Stores per-ticker training data
│   │   ├── TICKER.csv     # Features and returns for a given ticker
│
├── model/
│   ├── model.py           # Regression model training/prediction
│   ├── visualize.py       # Plots predicted returns
│
├── README.md              # This file
```

---

## ⚙️ How It Works

1. Run `main.py` daily before market opens.
2. Fetch the latest data up to yesterday’s close.
3. Predict next-day return for each stock.

---

## 🧠 Model Details

- **Model type:** Regression (not classification)
- **Output:** Predicted next-day % return  
  \[
  r_{t+1} = \frac{\text{Close}_{t+1} - \text{Close}_t}{\text{Close}_t}
  \]
- **Modeling tool:** `XGBRegressor`

---

## 📦 Dependencies

- Python 3.8+
- `pandas`
- `yfinance`
- `ta` (technical indicators)
- `xgboost`

Install everything:
```bash
pip install -r requirements.txt
