def chatbot_response(question, df, numeric_cols, categorical_cols):
    """
    Smart chatbot that understands any dataset automatically.
    It checks column names from the uploaded dataset.
    """
    question = question.lower().strip()

    # --- TOTAL of any numeric column ---
    for col in numeric_cols:
        if col in question or col.replace('_', ' ') in question:
            total = df[col].sum()
            return f"Total {col.replace('_',' ').title()} is: {total:,.2f}"

    # --- TOP item in any category ---
    if 'top' in question or 'highest' in question or 'best' in question or 'maximum' in question:
        for cat in categorical_cols:
            if cat in question or cat.replace('_', ' ') in question:
                for num in numeric_cols:
                    if num in question or num.replace('_', ' ') in question:
                        top = df.groupby(cat)[num].sum().idxmax()
                        return f"Top {cat} by {num} is: {top}"
                # If no numeric mentioned, use first numeric column
                if numeric_cols:
                    top = df.groupby(cat)[numeric_cols[0]].sum().idxmax()
                    return f"Top {cat} by {numeric_cols[0]} is: {top}"

    # --- WORST / WEAKEST item ---
    if 'weak' in question or 'worst' in question or 'lowest' in question or 'minimum' in question:
        for cat in categorical_cols:
            if cat in question or cat.replace('_', ' ') in question:
                if numeric_cols:
                    worst = df.groupby(cat)[numeric_cols[0]].sum().idxmin()
                    return f"Weakest {cat} by {numeric_cols[0]} is: {worst}"

    # --- COUNT of rows ---
    if 'count' in question or 'how many' in question or 'total rows' in question:
        return f"Total records in dataset: {len(df)}"

    # --- LIST columns ---
    if 'column' in question or 'feature' in question or 'what data' in question:
        all_cols = list(df.columns)
        return f"Dataset has these columns: {', '.join(all_cols)}"

    # --- Average of any numeric column ---
    if 'average' in question or 'mean' in question or 'avg' in question:
        for col in numeric_cols:
            if col in question or col.replace('_', ' ') in question:
                avg = df[col].mean()
                return f"Average {col.replace('_',' ').title()} is: {avg:,.2f}"

    # --- Default helpful response ---
    hint_nums = ', '.join([c.replace('_',' ') for c in numeric_cols[:3]])
    hint_cats = ', '.join([c.replace('_',' ') for c in categorical_cols[:3]])
    return (
        f"I didn't understand that. Try asking about:\n"
        f"- 'total {hint_nums}'\n"
        f"- 'top {hint_cats}'\n"
        f"- 'weak {hint_cats}'\n"
        f"- 'average {hint_nums}'\n"
        f"- 'how many rows'"
    )
