def get_kpis(df, numeric_cols):
    """
    Automatically calculate KPIs for any numeric columns found in the dataset.
    Returns a dictionary of {column_name: total_value}
    """
    kpis = {}
    for col in numeric_cols:
        kpis[col] = df[col].sum()
    return kpis

def get_top_value(df, group_col, value_col):
    """Find the top item in any column by any value column"""
    try:
        return df.groupby(group_col)[value_col].sum().idxmax()
    except Exception:
        return "N/A"
