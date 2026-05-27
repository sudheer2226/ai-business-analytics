import pandas as pd

def load_data(filepath):
    """Load any CSV file automatically"""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Clean data automatically"""
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)
    # Convert column names to lowercase and strip spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def detect_column_types(df):
    """
    Automatically detect which columns are:
    - numeric (revenue, profit, sales, quantity, etc.)
    - categorical (region, product, category, etc.)
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    return numeric_cols, categorical_cols
