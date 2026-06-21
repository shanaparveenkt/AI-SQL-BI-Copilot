from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

password = quote_plus("Password@123")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost/shopsphere"
)

files = [
    ("data/products.csv", "products"),
    ("data/sellers.csv", "sellers"),
    ("data/orders.csv", "orders"),
    ("data/order_items.csv", "order_items"),
    ("data/payments.csv", "payments"),
    ("data/reviews.csv", "reviews"),
    ("data/delivery.csv", "delivery"),
    ("data/fact_sales.csv", "fact_sales")
]

for file_name, table_name in files:
    print(f"Loading {file_name}...")
    df = pd.read_csv(file_name)
    df.to_sql(table_name, con=engine, if_exists="append", index=False)
    print(f"{table_name} loaded successfully!")

print("All datasets loaded successfully!")