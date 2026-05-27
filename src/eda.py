def get_group_summary(df, group_col, value_col):
    """
    Group any column by any value column automatically.
    Example: group by 'region' and sum 'revenue'
    """
    try:
        return df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    except Exception:
        return None
