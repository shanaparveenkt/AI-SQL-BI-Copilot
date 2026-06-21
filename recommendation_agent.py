import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_recommendations(question, result_df):
    if result_df is None or result_df.empty:
        return "No data available for recommendations."

    prompt = f"""
You are a senior business strategy consultant.

User Question:
{question}

Query Result (First 5 rows only):
{result_df.head(5).to_string()}

Provide actionable business recommendations.

Rules:
- Focus on practical business actions
- Keep recommendations short and clear
- Give 3 to 5 recommendations
- Professional style
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Recommendation generation failed: {str(e)}"