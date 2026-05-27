# 🚀 AI-Powered Business Analytics System
## Works with ANY CSV Dataset Automatically!

---

## What This Project Does
- Upload ANY CSV file → everything updates automatically
- Auto-detects all columns (numeric, categorical)
- Auto-generates KPIs, charts, filters, insights
- ML model you can train on any numeric columns
- Chatbot answers questions about your data
- Generates business report automatically

---

## How to Run

### Step 1 — Install libraries
```
pip install -r requirements.txt
```

### Step 2 — Train default model (only once)
```
python train_once.py
```

### Step 3 — Run the app
```
streamlit run app.py
```

### Step 4 — Open browser
Go to: http://localhost:8501

---

## How to Use with a New Dataset
1. Run the app: `streamlit run app.py`
2. Click "Browse files" in the sidebar
3. Upload your CSV file
4. Everything — filters, KPIs, charts, insights — updates automatically!

---

## Technologies Used
- Python, Pandas, NumPy
- Streamlit (Dashboard)
- Scikit-learn (ML)
- Joblib (Model saving)

---

## Project Structure
```
ai_business_analytics/
├── app.py                  ← Main dashboard (run this)
├── train_once.py           ← Run once to train default model
├── requirements.txt        ← Install these
├── model.pkl               ← Saved ML model
├── data/
│   └── sales.csv           ← Default sample dataset
├── src/
│   ├── data_cleaning.py    ← Auto column detection
│   ├── kpi.py              ← Auto KPI calculation
│   ├── eda.py              ← Auto chart data
│   ├── model_training.py   ← Auto ML training
│   ├── chatbot.py          ← Auto chatbot
│   ├── insights.py         ← Auto insights
│   └── report_generator.py ← Auto report
└── reports/
    └── business_report.txt ← Generated report
```
