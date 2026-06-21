from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

password = quote_plus("Password@123")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost/shopsphere"
)

def run_query(query):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()

            return pd.DataFrame(rows, columns=columns), None

    except Exception as e:
        return None, str(e)