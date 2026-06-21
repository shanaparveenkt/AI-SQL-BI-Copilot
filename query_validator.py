FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]

def validate_sql(query):
    query_upper = query.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False, f"Unsafe SQL detected: {keyword}"

    if not query_upper.strip().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    return True, "Safe Query"