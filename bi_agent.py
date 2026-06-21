import plotly.express as px
import pandas as pd


def create_chart(df):
    if df is None or df.empty:
        return None

    if len(df.columns) < 2:
        return None

    numeric_cols = df.select_dtypes(include=["number"]).columns
    non_numeric_cols = df.select_dtypes(exclude=["number"]).columns

    if len(numeric_cols) == 0 or len(non_numeric_cols) == 0:
        return None

    x_col = non_numeric_cols[0]
    y_col = numeric_cols[0]

    try:
        x_name = str(x_col).lower()

        # Line chart for time-based columns
        if "date" in x_name or "month" in x_name or "year" in x_name:
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} Trend"
            )

        # Pie chart for small category sets
        elif len(df) <= 5:
            fig = px.pie(
                df,
                names=x_col,
                values=y_col,
                title=f"{y_col} Distribution"
            )

        # Default bar chart
        else:
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} by {x_col}"
            )

        return fig

    except Exception:
        return None
    

def get_kpis(df):
    if df is None or df.empty:
        return None

    try:
        numeric_cols = []

        for col in df.columns:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                numeric_cols.append(col)

        if len(numeric_cols) == 0:
            return None

        metric_col = numeric_cols[0]
        df[metric_col] = pd.to_numeric(df[metric_col], errors="coerce")

        total_value = round(df[metric_col].sum(), 2)
        avg_value = round(df[metric_col].mean(), 2)
        max_value = round(df[metric_col].max(), 2)

        return total_value, avg_value, max_value

    except Exception as e:
        print("KPI Error:", e)
        return None