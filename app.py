from sql_agent import generate_sql
from database import run_query
from query_validator import validate_sql
from insight_generator import generate_insight


def is_raw_sql(user_input):
    sql_keywords = ["SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY"]

    user_upper = user_input.upper()

    return any(keyword in user_upper for keyword in sql_keywords)


question = input("Ask your question: ")

if is_raw_sql(question):
    sql_query = question
else:
    sql_query = generate_sql(question)

print("\nGenerated SQL:")
print(sql_query)

is_valid, message = validate_sql(sql_query)

if not is_valid:
    print(f"\nQuery Blocked: {message}")

else:
    result, error = run_query(sql_query)

    if error:
        print("\nSQL Execution Error:")
        print(error)

    else:
        print("\nResults:")
        print(result)

        insight = generate_insight(question, result)

        print("\nAnalysis Agent Output:")
        print(insight)