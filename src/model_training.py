import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib

def train_model(df, feature_cols, target_col):
    """
    Train ML model automatically with any feature columns and target column.
    feature_cols = list of numeric columns to use as input (X)
    target_col   = the column you want to predict (y)
    """
    try:
        X = df[feature_cols]
        y = df[target_col]

        # Need at least 4 rows for splitting
        if len(df) < 4:
            model = LinearRegression()
            model.fit(X, y)
            joblib.dump(model, 'model.pkl')
            return model, 0.0, feature_cols, target_col

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = LinearRegression()
        model.fit(X_train, y_train)

        score = r2_score(y_test, model.predict(X_test)) if len(X_test) > 0 else 0.0

        joblib.dump(model, 'model.pkl')
        return model, round(score, 2), feature_cols, target_col

    except Exception as e:
        return None, 0.0, feature_cols, target_col
