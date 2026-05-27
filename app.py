import streamlit as st
import pandas as pd
import joblib
import os

from src.data_cleaning import load_data, clean_data, detect_column_types
from src.kpi import get_kpis, get_top_value
from src.eda import get_group_summary
from src.chatbot import chatbot_response
from src.insights import generate_insights
from src.report_generator import create_report
from src.model_training import train_model

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 AI-Powered Business Analytics System")
st.markdown("**Upload any CSV dataset — everything updates automatically!**")

# ─────────────────────────────────────────────
# STEP 1: FILE UPLOAD (or use default)
# ─────────────────────────────────────────────
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")
else:
    df_raw = load_data("data/sales.csv")
    st.sidebar.info("Using default sample dataset (sales.csv)")

# ─────────────────────────────────────────────
# STEP 2: CLEAN DATA & DETECT COLUMNS
# ─────────────────────────────────────────────
df = clean_data(df_raw.copy())
numeric_cols, categorical_cols = detect_column_types(df)

# Show dataset preview
with st.expander("🔍 Preview Dataset"):
    st.dataframe(df.head(10))
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    col_info_n = ", ".join(numeric_cols) if numeric_cols else "None"
    col_info_c = ", ".join(categorical_cols) if categorical_cols else "None"
    st.write(f"**Numeric Columns:** {col_info_n}")
    st.write(f"**Categorical Columns:** {col_info_c}")

# ─────────────────────────────────────────────
# STEP 3: SIDEBAR FILTERS (AUTO-GENERATED)
# ─────────────────────────────────────────────
st.sidebar.header("🔧 Filters")

filtered_df = df.copy()

if categorical_cols:
    for cat_col in categorical_cols[:3]:  # Show up to 3 filters
        unique_vals = df[cat_col].unique().tolist()
        if len(unique_vals) <= 20:  # Only show filter if not too many unique values
            selected = st.sidebar.multiselect(
                f"Filter by {cat_col.replace('_',' ').title()}",
                options=unique_vals,
                default=unique_vals
            )
            if selected:
                filtered_df = filtered_df[filtered_df[cat_col].isin(selected)]
else:
    st.sidebar.write("No categorical columns found for filtering.")

st.sidebar.markdown(f"**Rows after filter:** {len(filtered_df)}")

# ─────────────────────────────────────────────
# STEP 4: KPI CARDS (AUTO-GENERATED)
# ─────────────────────────────────────────────
st.subheader("📈 Business KPIs")

if numeric_cols:
    kpis = get_kpis(filtered_df, numeric_cols)
    # Show max 4 KPI cards per row
    cols_to_show = list(kpis.items())[:4]
    kpi_cols = st.columns(len(cols_to_show))
    for i, (col_name, col_val) in enumerate(cols_to_show):
        kpi_cols[i].metric(
            label=col_name.replace('_', ' ').title(),
            value=f"{col_val:,.0f}"
        )
else:
    st.warning("No numeric columns found for KPIs.")

# ─────────────────────────────────────────────
# STEP 5: AUTO CHARTS (FOR ANY COLUMNS)
# ─────────────────────────────────────────────
st.subheader("📊 Auto Charts")

if categorical_cols and numeric_cols:
    # Let user pick what to plot
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        selected_cat = st.selectbox(
            "Group By (X-axis)",
            options=categorical_cols,
            index=0
        )

    with chart_col2:
        selected_num = st.selectbox(
            "Value Column (Y-axis)",
            options=numeric_cols,
            index=0
        )

    chart_data = get_group_summary(filtered_df, selected_cat, selected_num)
    if chart_data is not None and not chart_data.empty:
        st.bar_chart(chart_data)
    else:
        st.warning("Not enough data to plot chart.")

    # Second auto chart with next columns
    if len(categorical_cols) > 1 and len(numeric_cols) > 0:
        st.markdown("---")
        cat2 = categorical_cols[1] if len(categorical_cols) > 1 else categorical_cols[0]
        num2 = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
        st.write(f"**{cat2.replace('_',' ').title()} vs {num2.replace('_',' ').title()}**")
        chart_data2 = get_group_summary(filtered_df, cat2, num2)
        if chart_data2 is not None and not chart_data2.empty:
            st.bar_chart(chart_data2)

else:
    st.warning("Need both categorical and numeric columns to generate charts.")

# ─────────────────────────────────────────────
# STEP 6: AI INSIGHTS (AUTO)
# ─────────────────────────────────────────────
st.subheader("🤖 AI Insights")

if numeric_cols and categorical_cols:
    insight_text = generate_insights(filtered_df, numeric_cols, categorical_cols)
    st.success(insight_text)
else:
    st.info("Need both numeric and categorical columns to generate insights.")

# ─────────────────────────────────────────────
# STEP 7: ML PREDICTION (AUTO)
# ─────────────────────────────────────────────
st.subheader("🔮 ML Sales Prediction")

if len(numeric_cols) >= 2:
    st.markdown("Select feature columns (inputs) and target column (what to predict):")

    pred_col1, pred_col2 = st.columns(2)

    with pred_col1:
        feature_cols = st.multiselect(
            "Feature Columns (X - inputs)",
            options=numeric_cols,
            default=numeric_cols[:-1] if len(numeric_cols) > 1 else numeric_cols
        )

    with pred_col2:
        target_col = st.selectbox(
            "Target Column (Y - predict)",
            options=numeric_cols,
            index=len(numeric_cols) - 1
        )

    if feature_cols and target_col and target_col not in feature_cols:
        if st.button("🏋️ Train Model"):
            with st.spinner("Training model..."):
                model, score, feat, tgt = train_model(filtered_df, feature_cols, target_col)
            if model:
                st.success(f"✅ Model trained! R² Score: {score}")
                st.session_state['model'] = model
                st.session_state['feature_cols'] = feat
                st.session_state['target_col'] = tgt
            else:
                st.error("Model training failed. Try different columns.")

        # Prediction inputs
        if 'model' in st.session_state:
            st.markdown("**Enter values to predict:**")
            input_vals = {}
            inp_cols = st.columns(len(st.session_state['feature_cols']))
            for i, fc in enumerate(st.session_state['feature_cols']):
                col_min = float(filtered_df[fc].min())
                col_max = float(filtered_df[fc].max())
                col_mean = float(filtered_df[fc].mean())
                input_vals[fc] = inp_cols[i].number_input(
                    fc.replace('_', ' ').title(),
                    value=col_mean,
                    min_value=col_min,
                    max_value=col_max * 10
                )

            input_row = [[input_vals[fc] for fc in st.session_state['feature_cols']]]
            prediction = st.session_state['model'].predict(input_row)
            tgt_name = st.session_state['target_col'].replace('_', ' ').title()
            st.info(f"🎯 Predicted {tgt_name}: **{prediction[0]:,.2f}**")
    else:
        st.warning("Select feature columns and a different target column.")
else:
    # Auto-train with existing model.pkl if available
    if os.path.exists('model.pkl'):
        st.info("Default model loaded. Upload a dataset and select columns to retrain.")
    else:
        st.warning("Need at least 2 numeric columns for ML prediction.")

# ─────────────────────────────────────────────
# STEP 8: CHATBOT (AUTO)
# ─────────────────────────────────────────────
st.subheader("💬 Ask Your Data")
st.markdown("Ask questions about your dataset in plain English!")

question = st.text_input("Type your question here...", placeholder="e.g. total revenue, top region, average profit")

if question:
    response = chatbot_response(question, filtered_df, numeric_cols, categorical_cols)
    st.write(f"🤖 **Answer:** {response}")

# ─────────────────────────────────────────────
# STEP 9: REPORT GENERATOR (AUTO)
# ─────────────────────────────────────────────
st.subheader("📄 Generate Business Report")

if st.button("📥 Generate Full Report"):
    if numeric_cols:
        report = create_report(filtered_df, numeric_cols, categorical_cols)
        st.text(report)
        st.success("✅ Report also saved to reports/business_report.txt")
    else:
        st.warning("No numeric columns found. Cannot generate report.")

st.markdown("---")
st.caption("AI-Powered Business Analytics System | Upload any CSV and get instant insights!")
