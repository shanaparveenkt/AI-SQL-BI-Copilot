import streamlit as st
from sql_agent import generate_sql
from database import run_query
from query_validator import validate_sql
from insight_generator import generate_insight
from bi_agent import create_chart, get_kpis
from forecast_agent import forecast_revenue
from recommendation_agent import generate_recommendations

def is_raw_sql(user_input):
    sql_keywords = ["SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY"]

    user_upper = user_input.upper()

    return any(keyword in user_upper for keyword in sql_keywords)


st.set_page_config(
    page_title="AI SQL BI Copilot",
    layout="wide"
)

st.title("AI SQL BI Copilot")
st.caption("AI-Powered Business Intelligence & Forecasting Platform")



question = st.text_input("Ask a business question:")

st.markdown("""
### Query Guidelines
- Use natural language for best results
- Raw SQL is also supported

Examples:
- Show total revenue by city
- Show top 5 products by revenue
- Show monthly revenue trend
""")

if st.button("Run Query"):
    if is_raw_sql(question):
        sql_query = question
    else:
        sql_query = generate_sql(question)

    with st.expander("View Generated SQL"):
        st.code(sql_query, language="sql")

    is_valid, message = validate_sql(sql_query)

    if not is_valid:
        st.error(message)

    else:
        result, error = run_query(sql_query)

        if error:
            st.error(error)

        else:
            st.subheader("Results")
            st.dataframe(result)

            # Executive Summary
            st.subheader("Executive Summary")
            st.info(f"""
Query processed successfully.

Business question analyzed:
{question}

AI agents completed:
✔ Query Agent
✔ BI Agent
✔ Analysis Agent
✔ Recommendation Agent
            """)

            # KPI Cards
            st.subheader("KPI Dashboard")
            kpis = get_kpis(result)

            if kpis:
                total_value, avg_value, max_value = kpis

                col1, col2, col3 = st.columns(3)
                col1.metric("Total", total_value)
                col2.metric("Average", avg_value)
                col3.metric("Maximum", max_value)

            # BI Chart
            st.subheader("Visual Analytics")
            fig = create_chart(result)
            if fig:
                st.plotly_chart(fig)

            # Analysis
            insight = generate_insight(question, result)
            st.subheader("AI Business Insights")
            st.write(insight)

            # Recommendations
            recommendations = generate_recommendations(question, result)
            st.subheader("Strategic Recommendations")
            st.write(recommendations)

            # Forecast
            if "month" in result.columns and "revenue" in result.columns:
                forecast_df, forecast_fig = forecast_revenue(result)

                if forecast_df is not None:
                    st.subheader("Revenue Forecast Report")
                    st.dataframe(forecast_df)

                    if forecast_fig:
                        st.plotly_chart(forecast_fig)