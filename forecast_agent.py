import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px


def forecast_revenue(df):
    if df is None or df.empty:
        return None, None

    df = df.copy()
    df["month_index"] = range(len(df))

    X = df[["month_index"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    future_months = pd.DataFrame({
        "month_index": [len(df), len(df)+1, len(df)+2]
    })

    predictions = model.predict(future_months)

    forecast_df = pd.DataFrame({
        "month": ["Next Month", "Month +2", "Month +3"],
        "predicted_revenue": predictions
    })

    fig = px.line(
        forecast_df,
        x="month",
        y="predicted_revenue",
        title="Revenue Forecast"
    )

    return forecast_df, fig