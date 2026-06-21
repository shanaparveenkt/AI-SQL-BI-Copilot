import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_insight(question, result_df):
    # Handle empty result
    if result_df is None or result_df.empty:
        return "No data available for analysis."

    prompt = f"""
You are a senior business analyst.

User Question:
{question}

Query Result (First 5 rows only):
{result_df.head(5).to_string()}

Analyze the data and provide:

1. Key Insights
2. Trends (if any)
3. Anomalies (if any)
4. Root Cause Analysis (if possible)

Rules:
- Keep response concise
- Professional BI style
- Business focused
- If data is insufficient for trends/anomalies, mention that clearly
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Insight generation failed: {str(e)}"

