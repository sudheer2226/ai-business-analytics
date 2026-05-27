def generate_insights(df, numeric_cols, categorical_cols):
    """
    Automatically generate business insights for ANY dataset.
    Works by finding top and bottom values across all columns.
    """
    insights = []

    for cat in categorical_cols[:2]:  # Use first 2 categorical columns
        for num in numeric_cols[:2]:  # Use first 2 numeric columns
            try:
                top = df.groupby(cat)[num].sum().idxmax()
                top_val = df.groupby(cat)[num].sum().max()
                bottom = df.groupby(cat)[num].sum().idxmin()
                bottom_val = df.groupby(cat)[num].sum().min()

                insights.append(
                    f"✅ Top {cat.replace('_',' ').title()} by {num.replace('_',' ').title()}: "
                    f"{top} ({top_val:,.0f})"
                )
                insights.append(
                    f"⚠️ Weakest {cat.replace('_',' ').title()} by {num.replace('_',' ').title()}: "
                    f"{bottom} ({bottom_val:,.0f})"
                )
            except Exception:
                continue

    # General recommendation
    if insights:
        insights.append(
            "💡 Recommendation: Focus marketing efforts on weaker segments and "
            "replicate strategies from top-performing areas."
        )
    else:
        insights.append("No insights could be generated. Please check your dataset.")

    return "\n".join(insights)
