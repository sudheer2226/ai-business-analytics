import os
from src.insights import generate_insights

def create_report(df, numeric_cols, categorical_cols):
    """Generate a business report automatically for any dataset"""

    os.makedirs('reports', exist_ok=True)

    lines = []
    lines.append("=" * 50)
    lines.append("         AI-POWERED BUSINESS REPORT")
    lines.append("=" * 50)
    lines.append(f"\nTotal Records: {len(df)}")
    lines.append(f"Columns: {', '.join(df.columns.tolist())}\n")

    lines.append("-" * 50)
    lines.append("KEY METRICS SUMMARY")
    lines.append("-" * 50)
    for col in numeric_cols:
        lines.append(f"Total {col.replace('_',' ').title()}: {df[col].sum():,.2f}")
        lines.append(f"Average {col.replace('_',' ').title()}: {df[col].mean():,.2f}")
        lines.append(f"Max {col.replace('_',' ').title()}: {df[col].max():,.2f}")
        lines.append("")

    lines.append("-" * 50)
    lines.append("AI INSIGHTS")
    lines.append("-" * 50)
    insights = generate_insights(df, numeric_cols, categorical_cols)
    lines.append(insights)

    report = "\n".join(lines)

    with open('reports/business_report.txt', 'w') as f:
        f.write(report)

    return report
